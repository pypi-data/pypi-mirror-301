import tempfile as _tmp
from botocore.exceptions import ClientError
import asyncio

from mt import tp, pd, path, aio, logg
from mt.base import http, s3

from . import home_dirpath, on_winnow_edge
from .cache_folder import CacheFolderManager

from tzlocal import get_localzone
from time import mktime


__all__ = [
    "get_default_s3_profile",
    "create_context_vars",
    "run_main",
    "split",
    "download_s3_asyn",
    "download_s3",
    "cache_asyn",
    "cache",
    "cache_localpath",
    "is_s3cmd_url",
    "expand_s3cmd_url",
    "contract_s3cmd_url",
    "as_s3cmd_url",
    "as_https_url",
    "exists",
    "upload",
    "list_objects",
    "prepare_filepath2key_map",
    "put_files",
    "sync_to_s3",
]


def get_default_s3_profile():
    """Gets the default S3 profile, adjusting the profile to 'wml' or 'winnow' if they exist. Otherwise, use the default profile provided in the aws credentials."""
    sess = s3.get_session(asyn=False)

    for profile_name in ["wml", "winnow"]:
        if profile_name in sess.available_profiles:
            return profile_name

    return None


def create_context_vars(asyn: bool = False):
    """An asynchronous context manager that creates a dictionary of context variables for running functions in this module.

    Parameters
    ----------
    asyn : bool
        whether the functions within the context are to be invoked asynchronously or synchronously

    Returns
    -------
    context_vars : dict
        dictionary of context variables to run the functions in this module. These include
        's3_client' and 'http_session'.
    """
    return s3.create_context_vars(profile=get_default_s3_profile(), asyn=asyn)


def run_main(main_func, *args, asyn: bool = True, **kwargs):
    """Runs a main, asyn function that accepts 'context_vars' keyword argument.

    The 'context_vars' keyword argument is created automatically for the main function.

    Parameters
    ----------
    main_func : function
        a main function which is also an asyn function
    args : list
        positional arguments to be passed as-is to the main function
    asyn : bool
        whether the function is to be invoked asynchronously or synchronously
    kwargs : dict
        keyword arguments to be passed as-is to the main function

    Returns
    -------
    object
        whatever the function returns
    """

    async def f(main_func, *args, asyn: bool = True, **kwargs):
        async with create_context_vars(asyn=asyn) as context_vars:
            return await main_func(*args, context_vars=context_vars, **kwargs)

    if asyn:
        return asyncio.run(f(main_func, *args, **kwargs))
    return aio.srun(f, main_func, *args, **kwargs)


def _create_default_context_vars():
    session = s3.get_session(profile=get_default_s3_profile(), asyn=False)
    config = s3.botocore.config.Config(max_pool_connections=20)
    s3_client = session.client("s3", config=config)
    return {"async": False, "s3_client": s3_client, "http_session": None}


default_context_vars = _create_default_context_vars()


s3buckets = {
    "ml": "e5251f96e0164a19b3cd12c7a0b3174a",
    "im": "c76a090f-0e84-44f4-98bf-fe0469e163cd",
    "waste": "vision-waste-image-final-prod",
    "goods": "vision-ml-datasets",
}


def split(s3cmd_url):
    """Splits an s3cmd_url into bucket name and bucket path/object.

    Parameters
    ----------
    s3cmd_url : str
        an s3cmd url, e.g. starting with `s3://`, `im://` or `ml://`

    Returns
    -------
    bucket_name : str
        bucket name
    bucket_path : str
        path within the bucket that leads to to an S3 object
    """
    if s3cmd_url.startswith("ml://"):
        bucket_name = "e5251f96e0164a19b3cd12c7a0b3174a"
        delimiter = "/"
        bucket_path = s3cmd_url[5:]
    elif s3cmd_url.startswith("im://"):
        bucket_name = "c76a090f-0e84-44f4-98bf-fe0469e163cd"
        delimiter = "/"
        bucket_path = s3cmd_url[5:]
    elif s3cmd_url.startswith("s3://"):
        bucket_name, delimiter, bucket_path = s3cmd_url[5:].partition("/")
    elif s3cmd_url.startswith("waste://"):
        bucket_name = "vision-waste-image-final-prod"
        delimiter = "/"
        bucket_path = s3cmd_url[8:]
    elif s3cmd_url.startswith("goods://"):
        bucket_name = "vision-ml-datasets"
        delimiter = "/"
        bucket_path = s3cmd_url[8:]
    else:
        raise ValueError(
            "Expected a s3cmd url, which starts with 's3://', 'ml://', 'im://' or 'goods://', but "
            "receiving '{}' instead.".format(s3cmd_url)
        )
    if not delimiter:  # no '/' found
        raise ValueError(
            "Unable to parse s3cmd url '{}', no bucket found.".format(s3cmd_url)
        )
    return bucket_name, bucket_path


async def download_s3_asyn(
    s3cmd_url,
    local_path=None,
    new_only=False,
    file_mode=0o664,
    context_vars: dict = {},
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """An asyn function that downloads a s3cmd url to a local file given by local_path.

    Parameters
    ----------
    s3cmd_url : str
        URL specified by `s3cmd`
    local_path : str
        Path to a local file or local directory. If it is None, a local temporary directory is
        generated. Then, if it is is a folder, the downloaded file is saved into the folder, and
        the returned path is the path to the file. If it is a file, the downloaded url is saved
        into the file, overwriting if necessary.
    new_only : bool
        whether to download only if local file does not exist or is older than the one in S3.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
        Variable 's3_client' must exist and hold an enter-result of an async with statement
        invoking :func:`mt.base.s3.create_s3_client`.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging

    Returns
    -------
    file_path : str
        path to the downloaded file, or raise an Exception if not successful.
    """

    # parse s3cmd_url
    bucket_name, bucket_path = split(s3cmd_url)
    strict_s3cmd_url = s3.join(bucket_name, bucket_path)

    # get local file name
    bucket_dirname, bucket_basename = path.split("/" + bucket_path)

    # parse local_path
    if local_path is None:
        local_path = _tmp.gettempdir()
        local_path = path.join(local_path, bucket_basename)
    elif path.isdir(local_path):
        local_path = path.join(local_path, bucket_basename)

    # make sure the base directories are available
    await path.make_dirs_asyn(path.dirname(local_path), context_vars=context_vars)

    try:
        try:
            # get remote mtime
            url_info = await s3.list_object_info(
                strict_s3cmd_url, context_vars=context_vars
            )
        except:
            msg = "Exception caught trying to get the mtime of s3url '{}'".format(
                strict_s3cmd_url
            )
            logg.warn(msg, logger=logger)
            raise
        if url_info is None:
            raise IOError("S3 object not found: '{}'".format(s3cmd_url))
        remote_mtime = url_info["LastModified"]
        # MT-NOTE: source of AttributeError: 'NoneType' object has no attribute 'total_seconds'
        remote_mtime = pd.Timestamp(remote_mtime).tz_convert(get_localzone())
        remote_mtime = mktime(remote_mtime.timetuple())

        # check if it is ok to download
        ok = True
        if new_only and path.exists(local_path):
            try:
                local_mtime = path.getmtime(local_path)
                if remote_mtime <= local_mtime:
                    ok = False
                    if logger:
                        logger.debug(
                            "Remote file '{}' is older than local file '{}': {} seconds <= {} "
                            "seconds.".format(s3cmd_url, remote_mtime, local_mtime)
                        )
            except:
                pass

        # download file
        if ok:
            data = await s3.get_object(
                strict_s3cmd_url, show_progress=False, context_vars=context_vars
            )
            tmp_path = local_path + ".mttmp"
            await aio.write_binary(tmp_path, data, context_vars=context_vars)
            await path.rename_asyn(
                tmp_path, local_path, context_vars=context_vars, overwrite=True
            )
            path.utime(local_path, (remote_mtime, remote_mtime))
            if file_mode:  # chmod
                path.chmod(local_path, file_mode)

            cache.download_count += 1
            if cache.download_count >= 1024:
                if cache.folder_manager is not None:
                    cache.folder_manager.regulate(logger=logger)
                cache.download_count = 0
            if logger:
                logger.debug("Downloaded: {}".format(s3cmd_url))
    except:
        if not path.exists(local_path):
            raise

        if logger:
            logger.warn_last_exception()
            logger.warn("Ignored the above exception because the local file exists:")
            logger.warn("  Filepath: {}".format(local_path))

    return local_path


# @deprecated_func("2.2", suggested_func="download_s3_asyn", docstring_prefix="    ")
def download_s3(
    s3cmd_url,
    local_path=None,
    new_only=False,
    file_mode=0o664,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """Downloads a s3cmd url to a local file given by local_path.

    Parameters
    ----------
    s3cmd_url : str
        URL specified by `s3cmd`
    local_path : str
        Path to a local file or local directory. If it is None, a local temporary directory is
        generated. Then, if it is is a folder, the downloaded file is saved into the folder, and
        the returned path is the path to the file. If it is a file, the downloaded url is saved
        into the file, overwriting if necessary.
    new_only : bool
        whether to download only if local file does not exist or is older than the one in S3.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging

    Returns
    -------
    file_path : str
        path to the downloaded file, or raise an Exception if not successful.
    """

    return aio.srun(
        download_s3_asyn,
        s3cmd_url,
        local_path=local_path,
        new_only=new_only,
        file_mode=file_mode,
        extra_context_vars=default_context_vars,
        logger=logger,
    )


def cache_localpath(url):
    """Returns the desired local filepath for a given s3cmd url or http/https url.

    Parameters
    ----------
    url : str
        URL specified by `s3cmd` or its https/http equivalent

    Returns
    -------
    local_filepath : str
        path to local file that has been downloaded & sync'ed to the remote S3 file.

    Raises
    ------
    NotImplementedError
        if the folder manager does not exist, e.g. on Winnow edge devices
    """
    if cache.folder_manager is None:
        raise NotImplementedError("No cache folder manager implemented.")

    s3cmd_url = as_s3cmd_url(url)
    bucket_name, bucket_path = split(s3cmd_url)
    path_parts = [bucket_name] + bucket_path.split("/")

    local_filepath = path.join(cache.folder_manager.cache_dirpath, *path_parts).replace(
        ":", "_"
    )  # to avoid colon on Windows
    return local_filepath


async def cache_asyn(
    s3cmd_url,
    verbose_check: bool = True,
    file_mode: int = 0o664,
    context_vars: dict = {},
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """An asyn function that caches a file from S3 locally.

    Parameters
    ----------
    s3cmd_url : str
        URL specified by s3cmd or its https/http equivalent
    verbose_check : bool
        If True, check for modification timestamp as well. Otherwise, check for local existence only.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
        Variable 's3_client' must exist and hold an enter-result of an async with statement
        invoking :func:`mt.base.s3.create_s3_client`. In asynchronous mode, variable
        'http_session' must exist and hold an enter-result of an async with statement invoking
        :func:`mt.base.http.create_http_session`. You can use
        :func:`wml.core.s3.create_context_vars` to create a dictionary like this.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging

    Returns
    -------
    local_filepath : str
        path to local file that has been downloaded & sync'ed to the remote S3 file.

    Notes
    -----
    If the remote file is from our image S3 bucket, the local file does not exist and no verbose
    check is required, the remote file will be downloaded via https instead of s3 for faster speed
    and to save data transfer cost.
    """
    s3cmd_url = as_s3cmd_url(s3cmd_url)
    local_filepath = cache_localpath(s3cmd_url)

    if not verbose_check and path.exists(local_filepath):
        return local_filepath

    await path.make_dirs_asyn(path.dirname(local_filepath), context_vars=context_vars)

    if not path.exists(local_filepath):
        if cache.folder_manager is not None:
            # attempt to download from the cache server
            try:
                res = cache.folder_manager.get_file_from_cache_server(
                    local_filepath, file_mode=file_mode, logger=logger
                )
                if logger:
                    logger.debug("Sftp-get ({} bytes): {}".format(res, s3cmd_url))
                return local_filepath
            except:
                pass

        if not verbose_check and (
            s3cmd_url.startswith("im://")
            or s3cmd_url.startswith("waste://")
            or s3cmd_url.startswith("ml://web/")
            or s3cmd_url.startswith("s3://e5251f96e0164a19b3cd12c7a0b3174a/web/")
        ):  # special download case: download from https instead
            await http.download_and_chmod(
                as_https_url(s3cmd_url),
                local_filepath,
                file_mode=file_mode,
                context_vars=context_vars,
            )
            return local_filepath

    retval = await download_s3_asyn(
        s3cmd_url,
        local_path=local_filepath,
        new_only=True,
        file_mode=file_mode,
        context_vars=context_vars,
        logger=logger,
    )
    return retval


def cache(
    s3cmd_url,
    verbose_check=True,
    file_mode=0o664,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """Caches a file from S3 locally.

    Parameters
    ----------
    s3cmd_url : str
        URL specified by s3cmd or its https/http equivalent
    verbose_check : bool
        If True, check for modification timestamp as well. Otherwise, check for local existence only.
    file_mode : int
        to be passed directly to `os.chmod()` if not None
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging

    Returns
    -------
    local_filepath : str
        path to local file that has been downloaded & sync'ed to the remote S3 file.

    Notes
    -----
    If the remote file is from our image S3 bucket, the local file does not exist and no verbose
    check is required, the remote file will be downloaded via https instead of s3 for faster speed
    and to save data transfer cost.
    """
    return aio.srun(
        cache_asyn,
        s3cmd_url,
        verbose_check=verbose_check,
        file_mode=file_mode,
        extra_context_vars=default_context_vars,
        logger=logger,
    )


cache.folder_manager = (
    None if on_winnow_edge else CacheFolderManager(path.join(home_dirpath, "s3"))
)
cache.download_count = 0


# ----- new extension -----


def is_s3cmd_url(url: str) -> bool:
    """Returns if an url is an s3cmd_url."""
    for x in ["s3://", "ml://", "im://", "waste://", "goods://"]:
        if url.startswith(x):
            return True
    return False


def expand_s3cmd_url(s3cmd_url: str) -> str:
    if s3cmd_url.startswith("s3://"):
        return s3cmd_url
    for k, v in s3buckets.items():
        if s3cmd_url.startswith(k + "://"):
            return f"s3://{v}/" + s3cmd_url[3 + len(k) :]
    raise ValueError(f"Invalid s3cmd url: {s3cmd_url}")


def contract_s3cmd_url(s3cmd_url: str) -> str:
    if not s3cmd_url.startswith("s3://"):
        for k in s3buckets:
            if s3cmd_url.startswith(k):
                return s3cmd_url
        raise ValueError(f"Invalid s3cmd url: {s3cmd_url}")
    for k, v in s3buckets.items():
        if s3cmd_url.startswith(f"s3://{v}/"):
            return f"{k}://" + s3cmd_url[6 + len(v) :]
    return s3cmd_url


def as_s3cmd_url(url, raise_exception=True, expanded=False):
    """Converts an s3cmd_url or a http_url into a s3cmd_url.

    Parameters
    ----------
    url: str
        s3cmd url or http url or https url
    raise_exception: bool
        whether to raise a ValueError or to return None upon error
    expanded : str
        if expanded is ON, always returns 's3://' format. Otherwise, it returns an url that is as
        compact as possible

    Returns
    -------
    s3cmd_url: str
        s3cmd url
    """
    if expanded:
        if is_s3cmd_url(url):
            try:
                return expand_s3cmd_url(url)
            except ValueError:
                return None

        prefixes = {
            "http://e5251f96e0164a19b3cd12c7a0b3174a.s3.amazonaws.com/": "s3://e5251f96e0164a19b3cd12c7a0b3174a/",
            "https://e5251f96e0164a19b3cd12c7a0b3174a.s3.amazonaws.com/": "s3://e5251f96e0164a19b3cd12c7a0b3174a/",
            "https://s3.amazonaws.com/e5251f96e0164a19b3cd12c7a0b3174a/": "s3://e5251f96e0164a19b3cd12c7a0b3174a/",
            "http://c76a090f-0e84-44f4-98bf-fe0469e163cd.s3.amazonaws.com/": "s3://c76a090f-0e84-44f4-98bf-fe0469e163cd/",
            "https://s3.amazonaws.com/c76a090f-0e84-44f4-98bf-fe0469e163cd/": "s3://c76a090f-0e84-44f4-98bf-fe0469e163cd/",
            "https://s3.amazonaws.com/": "s3://",
            "https://vision-waste-image-final-prod.s3.amazonaws.com/": "s3://vision-waste-image-final-prod/",
            "http://vision-ml-datasets.s3.amazonaws.com/": "s3://vision-ml-datasets/",
            "https://vision-ml-datasets.s3.amazonaws.com/": "s3://vision-ml-datasets/",
            "https://s3.amazonaws.com/vision-ml-datasets/": "s3://vision-ml-datasets/",
        }
    else:
        if is_s3cmd_url(url):
            return contract_s3cmd_url(url)

        prefixes = {
            "http://e5251f96e0164a19b3cd12c7a0b3174a.s3.amazonaws.com/": "ml://",
            "https://e5251f96e0164a19b3cd12c7a0b3174a.s3.amazonaws.com/": "ml://",
            "https://s3.amazonaws.com/e5251f96e0164a19b3cd12c7a0b3174a/": "ml://",
            "http://c76a090f-0e84-44f4-98bf-fe0469e163cd.s3.amazonaws.com/": "im://",
            "https://s3.amazonaws.com/c76a090f-0e84-44f4-98bf-fe0469e163cd/": "im://",
            "https://s3.amazonaws.com/": "s3://",
            "https://vision-waste-image-final-prod.s3.amazonaws.com/": "waste://",
            "http://vision-ml-datasets.s3.amazonaws.com/": "goods://",
            "https://vision-ml-datasets.s3.amazonaws.com/": "goods://",
            "https://s3.amazonaws.com/vision-ml-datasets/": "goods://",
        }

    for k, v in prefixes.items():
        if url.startswith(k):
            return v + url[len(k) :]

    if raise_exception:
        raise ValueError("Unable to convert to s3cmd_url: {}".format(url))
    else:
        return None


def as_https_url(url, raise_exception=True):
    """Converts an url pointing to an S3 object into an https_url.

    Parameters
    ----------
    url: str
        s3cmd url or http url or https url pointing to an S3 object
    raise_exception: bool
        whether to raise a ValueError or to return None upon error

    Returns
    -------
    https_url: str
        an https url
    """
    if "://" not in url:
        if raise_exception:
            raise ValueError("Invalid url: {}".format(url))
        else:
            return None

    if url.startswith("https"):
        return url

    if is_s3cmd_url(url):
        s3cmd_url = contract_s3cmd_url(url)
    else:
        s3cmd_url = as_s3cmd_url(url, raise_exception=True, expanded=False)

    if s3cmd_url.startswith("ml://"):
        return (
            "https://s3.amazonaws.com/e5251f96e0164a19b3cd12c7a0b3174a" + s3cmd_url[4:]
        )

    if s3cmd_url.startswith("im://"):
        return (
            "https://s3.amazonaws.com/c76a090f-0e84-44f4-98bf-fe0469e163cd"
            + s3cmd_url[4:]
        )

    if s3cmd_url.startswith("waste://"):
        return "https://s3.amazonaws.com/vision-waste-image-final-prod" + s3cmd_url[7:]

    if s3cmd_url.startswith("goods://"):
        return "https://s3.amazonaws.com/vision-ml-datasets" + s3cmd_url[7:]

    return "https://s3.amazonaws.com" + s3cmd_url[4:]


def exists(s3cmd_url, local_check=False):
    """Checks if an S3 object/file exists.

    Parameters
    ----------
    s3cmd_url: str
        s3cmd url
    local_check : bool
        If True, checks locally for the existence of the file and only checks remotely if the local
        one does not exist. If False, checks remotely only.

    Returns
    -------
    bool
        whether or not the file/object exists
    """
    if local_check:
        filepath = cache_localpath(s3cmd_url)
        if path.exists(filepath):
            return True

    return (
        aio.srun(
            s3.list_object_info, s3cmd_url, extra_context_vars=default_context_vars
        )
        is not None
    )


def upload(filepath, s3cmd_url, logger: tp.Optional[logg.IndentedLoggerAdapter] = None):
    """Uploads a file to S3.

    Parameters
    ----------
    filepath: str
        local path to the file to be uploaded
    s3cmd_url : str
        URL specified by `s3cmd`
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    bool
        whether or not the file/object has been uploaded
    """
    if s3cmd_url.endswith("/"):  # directory
        s3cmd_url += path.basename(filepath)

    if logger:
        logger.info("S3upload:")
        logger.info("  from: {}".format(filepath))
        logger.info("    to: {}".format(s3cmd_url))

    bucket_name, bucket_path = split(s3cmd_url)
    # to have 's3://' prefix
    strict_s3cmd_url = s3.join(bucket_name, bucket_path)
    try:
        data = aio.srun(aio.read_binary, filepath)
        aio.srun(
            s3.put_object,
            strict_s3cmd_url,
            data,
            show_progress=bool(logger),
            extra_context_vars=default_context_vars,
        )
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code in (412, 304):
            if logger:
                logger.warn("Upload failed: '{}' -> '{}'.".format(filepath, s3cmd_url))
            return False

    return True


def list_objects(s3cmd_url: str, show_progress: bool = False) -> list:
    """Lists all objects in a given s3cmd url.

    Parameters
    ----------
    s3cmd_url: str
        s3cmd url
    show_progress : bool
        show a progress spinner in the terminal

    Returns
    -------
    s3cmd_url_list : list
        list of s3cmd urls in S3 prefixed by it
    """

    bucket, key = split(s3cmd_url)
    s3cmd_url = s3.join(bucket, key)  # to strictly have 's3://' prefix
    candidate_list = aio.srun(
        s3.list_objects,
        s3cmd_url,
        show_progress=show_progress,
        extra_context_vars=default_context_vars,
    )
    return [s3.join(bucket, candidate["Key"]) for candidate in candidate_list]


def prepare_filepath2key_map(
    l_srcFilepaths: tp.List[str],
    src_filepath_prefix: str,
    dst_s3url_prefix: str,
):
    """Prepares the filepath2key_map argument for :func:`put_files`.

    Parameters
    ----------
    l_srcFilepaths : list
        list of local files, identified by their paths, to be uploaded to S3.
    src_filepath_prefix : str
        the common source filepath prefix that all files must share. Files not having the same
        source prefix will be ignored. The prefix must end with '/'.
    dst_s3url_prefix : str
        the common destination s3cmd url prefix. Each filepath has its source prefix be replaced by
        the destination prefix, to form the corresponding s3 url. The prefix must end with '/'.

    Returns
    -------
    filepath2key_map : dict
        mapping from local filepath to bucket key, defining which file to upload and where to
        upload to in the S3 bucket
    bucket : str
        bucket name
    """

    if not src_filepath_prefix.endswith("/"):
        src_filepath_prefix += "/"
    if not dst_s3url_prefix.endswith("/"):
        dst_s3url_prefix += "/"

    bucket_name, s3_dirpath = split(dst_s3url_prefix)
    filepath2key_map = {}
    N = len(src_filepath_prefix)
    for filepath in l_srcFilepaths:
        if not filepath.startswith(src_filepath_prefix):
            continue
        filepath_postfix = filepath[N:]
        s3key = path.join(s3_dirpath, filepath_postfix)
        filepath2key_map[filepath] = s3key

    return filepath2key_map, bucket_name


def put_files(
    bucket: str,
    filepath2key_map: dict,
    total_filesize: tp.Optional[int] = None,
    set_acl_public_read: tp.Optional[bool] = None,
    list_uploaded_s3urls: bool = False,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """Uploads many files to the same S3 bucket using boto3.

    This function wraps :func:`mt.base.s3.put_files_boto3` providing the default context variables
    and the total file size.

    Parameters
    ----------
    bucket : str
        bucket name
    filepath2key_map : dict
        mapping from local filepath to bucket key, defining which file to upload and where to
        upload to in the S3 bucket
    total_filesize : int
        total size of all files in bytes, if you know. Useful for drawing a progress bar.
    set_acl_public_read : bool, optional
        whether or not to set ACL public-read policy on the uploaded object(s). If not provided,
        the value is be automatically determined. In this case, if it is the ML bucket and all
        bucket keys start with 'web/' then the value is set to True. Otherwise it is set to False.
    list_uploaded_s3urls : bool
        whether or not to list the uploaded s3urls. Only valid if `logger` is provided.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging
    """
    if set_acl_public_read is None:
        if bucket != "e5251f96e0164a19b3cd12c7a0b3174a":
            set_acl_public_read = False
        else:
            set_acl_public_read = True
            for v in filepath2key_map.values():
                if not v.startswith("web/"):
                    set_acl_public_read = False
                    break
        if logger:
            logger.info("In function wml.core.s3.put_files:")
            logger.info(f"  set_acl_public_read -> {set_acl_public_read}")

    s3bucket = f"s3://{bucket}/"
    total_filesize = sum((path.getsize(x) for x in filepath2key_map))
    with logg.scoped_info(f"Uploading to {s3bucket}", logger=logger):
        logg.info("File count: {}".format(len(filepath2key_map)), logger=logger)
        if set_acl_public_read:
            logg.info("Enabled acl_public_read.", logger=logger)
        res = s3.put_files_boto3(
            bucket,
            filepath2key_map,
            show_progress=bool(logger),
            total_filesize=total_filesize,
            set_acl_public_read=set_acl_public_read,
            context_vars=default_context_vars,
        )
        if list_uploaded_s3urls and logger:
            with logger.scoped_info("Uploaded s3urls"):
                for s3key in filepath2key_map.values():
                    logger.info(s3bucket + s3key)
    return res


def sync_to_s3(
    s3cmd_url: str,
    force_upload: bool = False,
    set_acl_public_read: bool = False,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """Sync-upload all local cached files to S3.

    Given an s3cmd url, the function searches for all local cached files prefixed with the urls and
    uploads all the missing files to S3.

    Parameters
    ----------
    s3cmd_url : str
        an s3cmd url describing the bucket and the prefix folder to upload-sync
    force_upload : bool, optional
        If True, forces all files to be uploaded. Otherwise (default), check the remote S3 bucket
        for objects that have been uploaded
    set_acl_public_read : bool
        whether or not to set ACL public-read policy on the uploaded object(s)
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Notes
    -----
    For any discovered local cached file, if its filepath has a special character, the special
    character must appear at the prefix part that is covered by the original s3cmd url, not the
    postfix part that identifies the file.
    """

    while s3cmd_url[-1] == "/":
        s3cmd_url = s3cmd_url[:-1]

    with logg.scoped_info(
        "Sync-uploading local files to '{}'".format(s3cmd_url), logger=logger
    ):
        s3url = as_s3cmd_url(as_https_url(s3cmd_url), expanded=True)  # expanded version
        local_dirpath = cache_localpath(s3url)
        local_filepaths = path.glob(path.join(local_dirpath, "**"), recursive=True)
        local_postfixes = [
            f[len(local_dirpath) + 1 :] for f in local_filepaths if path.isfile(f)
        ]

        if logger:
            logger.info("Found {} cached files.".format(len(local_postfixes)))
            logger.debug("First 5: {}".format(local_postfixes[:5]))
        if force_upload:
            new_postfixes = local_postfixes
        else:
            if logger:
                logger.info(
                    "Listing remote objects prefixed with '{}':".format(s3cmd_url)
                )
            s3_objects = list_objects(
                s3cmd_url, show_progress=bool(logger)
            )  # expanded existing s3 objects
            s3_postfixes = [f[len(s3url) + 1 :] for f in s3_objects]

            new_postfixes = list(set(local_postfixes) - set(s3_postfixes))
            if logger:
                logger.debug("First 5: {}".format(s3_postfixes[:5]))
        if logger:
            logger.info("Sync-uploading {} cached files:".format(len(new_postfixes)))

        filepath2key_map = {}
        bucket_name, s3_dirpath = split(s3url)
        for postfix in new_postfixes:
            local_filepath = path.join(local_dirpath, postfix)
            s3_key = path.join(s3_dirpath, postfix)
            filepath2key_map[local_filepath] = s3_key
        put_files(
            bucket_name,
            filepath2key_map,
            set_acl_public_read=set_acl_public_read,
            logger=logger,
        )
