"""Download/cache S3 files via multi-threading."""

# import tensorflow as tf  # Please do not import tensorflow here. Many scripts which do not use TF
# will be hurt by this import.
import os
import asyncio
import aiohttp
from tqdm.auto import tqdm

from mt import tp, pd, ctx, path, concurrency, logg, aio, traceback
from mt.base import http, filetype

from .s3 import (
    as_https_url,
    as_s3cmd_url,
    cache_asyn,
    cache_localpath,
    get_default_s3_profile,
    create_context_vars,
    run_main,
)

from .clujdc import in_clujdc


__all__ = [
    "get_s3url_y23",
    "remove_invalid_url",
    "inspect_images",
    "remove_images",
    "cache_files_asyn",
    "cache_files",
    "cache_filesizes",
]


def get_s3url_y23(image_id: int, thumb: bool = False) -> str:
    """Returns the s3url of an image id, based on the y23 format."""
    s = f"s3://ml_images/M{image_id // 1000000}/K{image_id // 1000}/"
    if thumb:
        s += f"thumb{image_id}.jpg"
    else:
        s += f"image{image_id}.jpg"

    return s


def remove_invalid_url(
    df: pd.DataFrame,
    field_name: str,
    id_field_name: tp.Optional[str] = None,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Removes rows of a dataframe where the given field contains an invalid url.

    Parameters
    ----------
    df : pandas.DataFrame
        the dataframe to operate on
    field_name : str
        name of a field of the dataframe for url inspection
    id_field_name : str
        name of a id field in case we have found some missing urls
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    pandas.DataFrame
        output dataframe where some rows with an invalid url are removed
    """
    s = ~df[field_name].str.contains("://")
    cnt = s.sum()
    if cnt == 0:
        return df

    if logger:
        df2 = df[s]
        with logger.scoped_warn(
            "Removed {} records where field '{}' is invalid".format(cnt, field_name),
            curly=False,
        ):
            if id_field_name is None:
                logger.warn(df2[[field_name]])
            else:
                df2 = df2[[id_field_name, field_name]].reset_index(drop=True)
                logger.warn(df2)

    df = df[~s]
    return df


def inspect_images(
    df: pd.DataFrame,
    check_image_header: bool = False,
    use_thumbnails: bool = False,
    file_mode=0o664,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Downloads all images locally and determines the image file type for each image, asynchronously.

    Parameters
    ----------
    df : pandas.DataFrame
        A dataframe columns `['url', 'width', 'height']` whose index represents the image ids.
    check_image_header : bool
        whether or not to check the image header. This step will slow down the speed substantially.
    use_thumbnails : bool
        whether the thumbnail urls (True) or the image urls (False) are provided in the dataframe
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    df : pandas.DataFrame(columns=['status', 'local_filepath'])
        A dataframe with the same index as `df` where for each image record we have the inspection
        status in `{'ok', 'remote_corrupted', 'local_corrupted'}` and the local filepath

    Notes
    -----
    This function combines the power of multiprocessing and asyncio. It shines when you have
    millions of files to inspect.
    """

    if in_clujdc:
        gid = os.getgid()
        if gid != 100:
            msg = f"You are caching images in an ML server. Your GID must be 100, but {gid} is given."
            raise OSError(msg)

    def func(x):
        if "://" in x:
            return as_s3cmd_url(x)
        if logger:
            logger.warn(f"Url '{x}' is invalid.")
        return None

    # df = df[df.index.drop_duplicates()]
    df["src_s3cmd_url"] = df["url"].apply(func)
    df["s3cmd_url"] = [
        get_s3url_y23(int(x), thumb=use_thumbnails) for x in df.index.tolist()
    ]

    num_files = len(df)
    logg.warn(f"Checking {num_files} files.", logger=logger)

    async def process(
        i, df, use_thumbnails: bool = False, context_vars: dict = {}, logger=None
    ):
        row = df.iloc[i]
        idx = int(row.name)
        s3cmd_url = row["s3cmd_url"]
        local_filepath = cache_localpath(s3cmd_url)
        local_dirpath = path.dirname(local_filepath)
        await path.make_dirs_asyn(local_dirpath, context_vars=context_vars)

        image_str = "thumbnail" if use_thumbnails else "image"
        for trial_id in range(2):
            if not await path.exists_asyn(local_filepath, context_vars=context_vars):
                src_s3cmd_url = row["src_s3cmd_url"]
                if src_s3cmd_url is None:  # no remote file
                    logg.warn(
                        f"No remote url found for {image_str} id {idx}.", logger=logger
                    )
                    return (idx, "remote_corrupted", local_filepath)

                logg.info(f"Pulling {image_str} id {idx}.", logger=logger)
                url = as_https_url(src_s3cmd_url)
                try:
                    content = await http.download(url, context_vars=context_vars)
                except aiohttp.client_exceptions.ServerDisconnectedError:
                    await asyncio.sleep(10)
                    raise
                if len(content) == 0:
                    msg = f"Empty downloaded content {image_str} id {idx}."
                    logg.warn(msg, logger=logger)
                    return (idx, "remote_corrupted", local_filepath)

                if not filetype.filetype.is_image(content):
                    msg = f"Corrupted downloaded content {image_str} id {idx}."
                    logg.warn(msg, logger=logger)
                    if trial_id < 1:
                        logg.warn("Retrying...", logger=logger)
                        continue
                    else:
                        return (idx, "remote_corrupted", local_filepath)

                try:
                    await aio.write_binary(
                        local_filepath,
                        content,
                        file_mode=file_mode,
                        context_vars=context_vars,
                    )
                except PermissionError as e:
                    raise traceback.LogicError(
                        "Unable to create file due to lack of permissions. You may need sudo to set the folder ownership properly.",
                        debug={"local_filepath": local_filepath},
                        causing_error=e,
                    )

            filesize = path.getsize(local_filepath)
            if filesize == 0:
                await path.remove_asyn(local_filepath, context_vars=context_vars)
                msg = f"Image file with id {idx} is empty and has been removed."
                logg.warn(msg, logger=logger)
                return (idx, "local_corrupted", local_filepath)

            if check_image_header and not await filetype.is_image_asyn(
                local_filepath, context_vars=context_vars
            ):
                await path.remove_asyn(local_filepath, context_vars=context_vars)
                msg = f"Image file with id {idx} has an invalid image header and has been removed."
                logg.warn(msg, logger=logger)
                return (idx, "local_corrupted", local_filepath)

            break

        return (idx, "ok", local_filepath)

    iterator = range(num_files)
    if logger is not None:
        iterator = tqdm(iterator, total=num_files, unit="file")
    iterator = concurrency.asyn_pmap(
        process,
        iterator,
        asyn_func_args=(df,),
        asyn_func_kwargs={"use_thumbnails": use_thumbnails, "logger": logger},
        cvc_func=create_context_vars,
        cvc_func_kwargs={"asyn": True},
    )

    df2 = pd.DataFrame(data=iterator, columns=["id", "status", "local_filepath"])
    df2 = df2.set_index("id", drop=True)
    if df.index.name is not None:
        df2.index.name = df.index.name
    return df2


def remove_images(
    s, block_size=100, logger: tp.Optional[logg.IndentedLoggerAdapter] = None
) -> int:
    """Downloads all images from the cache.

    Parameters
    ----------
    s : pandas.Series
        A list of images localpaths, s3cmd urls or http/https urls
    block_size : int
        number of files to process in each block of tasks
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    int
        the actual number of images removed

    Notes
    -----
    This function uses parallel processing to remove as quickly as possible.
    """
    if not isinstance(s, pd.Series):
        raise ValueError(
            "Expecting input to be a pandas.Series, receiving '{}'".format(s.__class__)
        )

    def as_localpath(x):
        if "://" in x:  # need to convert
            if x.startswith("http"):
                x = as_s3cmd_url(x)
            x = cache_localpath(x)
        return x

    l_paths = s.apply(as_localpath).drop_duplicates().tolist()

    num_files = len(l_paths)
    num_blocks = (len(l_paths) + block_size - 1) // block_size

    def cache_block(blk_id):
        if blk_id >= num_blocks:
            return None

        i_start = blk_id * block_size
        i_end = min((blk_id + 1) * block_size, num_files)

        n_removed = 0
        for i in range(i_start, i_end):
            localpath = l_paths[i]
            if not path.exists(localpath):
                continue
            path.remove(localpath)
            path.remove(localpath + ".immeta")
            n_removed += 1

        return (blk_id, n_removed)

    cnt = 0
    with concurrency.WorkIterator(cache_block, logger=logger) as caching_iterator:
        bar = None if logger is None else tqdm(total=num_files, unit="file")
        result_list = [None] * num_files
        missing_list = []
        for blk_id in range(num_blocks):
            _, n_removed = next(caching_iterator)
            cnt += n_removed
            if bar:
                bar.update(n_removed)
        if bar:
            bar.close()

    return cnt


async def cache_files_asyn(
    s: pd.Series,
    verbose_check: bool = True,
    file_mode: int = 0o664,
    context_vars: dict = {},
    profile=None,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """An asyn function that downloads all files locally and asynchronously.

    The files that are new will be set with given permissions.

    Parameters
    ----------
    s : pandas.Series
        A list of urls
    verbose_check : bool
        If True, check for modification timestamp as well. Otherwise, check for local existence only.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
    profile : str, optional
        one of the profiles specified in the AWS credentials file. The default is used if None is
        given.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    df : pandas.DataFrame(columns=['s3cmd_url', 'local_filepath'])
        A dataframe containing the corresponding list of s3cmd urls, list of local_filepaths.

    Notes
    -----
    This function combines the power of multiprocessing and asyncio. It shines when you have
    millions of files to inspect.
    """

    if not isinstance(s, pd.Series):
        raise ValueError(
            "Expecting input to be a pandas.Series, receiving '{}'".format(s.__class__)
        )

    def func(x):
        if "://" in x:
            return as_s3cmd_url(x)
        if logger:
            logger.warn("Url '{}' is invalid.".format(x))
        return None

    df = s.to_frame("url")
    df["s3cmd_url"] = df["url"].apply(func)
    null_cnt = df["s3cmd_url"].isnull().sum()
    s3cmd_urls = df["s3cmd_url"].dropna().drop_duplicates().tolist()
    if null_cnt > 0:
        if logger:
            logger.warn("Removed {} invalid urls.".format(null_cnt))

    num_files = len(s3cmd_urls)
    if logger:
        logger.warn("Checking {} files.".format(num_files))

    async def process(i, context_vars: dict = {}):
        try:
            s3cmd_url = s3cmd_urls[i]
            local_filepath = cache_localpath(s3cmd_url)
            if not path.exists(local_filepath):
                if logger is not None:
                    logger.info("Pulling {}".format(s3cmd_url))
                await cache_asyn(
                    s3cmd_url,
                    verbose_check=verbose_check,
                    file_mode=file_mode,
                    context_vars=context_vars,
                    logger=logger,
                )
            return s3cmd_url, local_filepath
        except (KeyboardInterrupt, asyncio.CancelledError):
            raise
        except:
            if logger:
                with logger.scoped_warning(
                    "Skipped file #{} '{}'".format(i, s3cmd_url), curly=False
                ):
                    logger.warn_last_exception()
            return None

    cnt = 0
    with (
        tqdm(total=num_files, unit="file") if logger is not None else ctx.nullcontext()
    ) as progress_bar:
        result_list = []
        async for result in concurrency.asyn_work_generator(
            process,
            num_works=num_files,
            profile=get_default_s3_profile(),
            debug_logger=logger,
            max_concurrency=256,
            num_processes=14,
            timeout=3600,
        ):
            s3cmd_url = s3cmd_urls[result[1]]
            if result[0] == "task_returned":
                result = result[2]
                if result is None:
                    if logger:
                        logger.info("Skipped inspecting '{}'.".format(s3cmd_url))
                else:
                    result_list.append(result)
                    if logger:
                        progress_bar.update()
                    cnt += 1
            elif result[0] == "task_cancelled":
                if logger:
                    logger.info("Cancelled inspecting '{}'.".format(s3cmd_url))
            elif result[0] == "task_raised":
                if logger:
                    with logger.scoped_warn(
                        "Inspecting '{}'".format(s3cmd_url), curly=False
                    ):
                        logger.warn(
                            "Skipped due to exception: {}".format(repr(result[1]))
                        )
                        logger.warn("Tracestack:\n{}".format(result[2]))
            else:
                raise RuntimeError("Unknown result type: {}".format(result))

    if cnt < num_files:
        if logger:
            logger.warn("Skipped {}/{} files.".format(num_files - cnt, cnt))

    # post-processing
    df2 = pd.DataFrame(
        columns=[
            "s3cmd_url",
            "local_filepath",
        ],
        data=result_list,
    )
    return df.join(df2.set_index("s3cmd_url", drop=True), on="s3cmd_url").drop(
        ["url"], axis=1
    )


def cache_files(
    s: pd.Series,
    verbose_check: bool = True,
    file_mode=0o664,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Downloads all files locally and asynchronously.

    This is a wrapper of :func:`cache_files_asyn` that provides the default asynchronous
    profile.

    The files that are new will be set with given permissions.

    Parameters
    ----------
    s : pandas.Series
        A list of urls
    verbose_check : bool
        If True, check for modification timestamp as well. Otherwise, check for local existence only.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    df : pandas.DataFrame(columns=['s3cmd_url', 'local_filepath'])
        A dataframe containing the corresponding list of s3cmd urls, list of local_filepaths.

    Notes
    -----
    This function combines the power of multiprocessing and asyncio. It shines when you have
    millions of files to inspect.
    """

    return run_main(
        cache_files_asyn,
        s,
        asyn=True,
        verbose_check=verbose_check,
        file_mode=file_mode,
        profile=get_default_s3_profile,
        logger=logger,
    )


def cache_filesizes(
    s: pd.Series, missing="warn", logger: tp.Optional[logg.IndentedLoggerAdapter] = None
) -> pd.DataFrame:
    """Obtain the filesize of every cachable url on the given series.

    Each url must be either or a https url that has been downloaded to an local filepath.

    Parameters
    ----------
    s : pandas.Series
        A list of cachable urls
    missing : {'raise', 'warn'}
        behaviour when missing filepaths are detected. 'raise' means a ValueError is raised.
        'warn' means some warning messages are printed (if the logger is available) and the
        filesize is set to 0.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    df : pandas.DataFrame(index='url', columns=['filesize'])
        A dataframe indexed by the distinct urls from the series. It has one column representing
        the list of corresponding filesizes. The user is supposed to join the dataframe back to
        their data.
    """

    l_urls = s.drop_duplicates().tolist()
    n_urls = len(l_urls)
    l_filesizes = []
    if logger:
        logger.info("Gathering {} filesizes...".format(n_urls))
    with (
        tqdm(total=n_urls, unit="file") if logger is not None else ctx.nullcontext()
    ) as progress_bar:
        for url in l_urls:
            try:
                if url.startswith("http"):
                    url = as_s3cmd_url(url)
                filepath = cache_localpath(url)
                filesize = path.getsize(filepath)
            except:
                if missing == "raise":
                    raise
                if logger:
                    logger.warn_last_exception()
                    logger.warn("The filesize has been reset to 0.")
            l_filesizes.append(filesize)
            if logger:
                progress_bar.update()

    df = pd.DataFrame(index=l_urls, data={"filesize": l_filesizes})
    return df
