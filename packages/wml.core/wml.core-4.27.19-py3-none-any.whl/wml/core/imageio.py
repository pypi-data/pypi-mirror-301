import json

from PIL import ImageFile

from mt import tp, cv, iio, path, aio, logg
from mt.base import filetype
from .s3 import cache_asyn, cache_localpath, as_s3cmd_url, default_context_vars

from .jpeg import jpegload


__all__ = [
    "immeta_asyn",
    "immeta",
    "imread_asyn",
    "imread",
    "imexists_asyn",
    "imexists",
    "imremove",
]


async def immeta_asyn(fname, context_vars: dict = {}, logger=None) -> dict:
    """An asyn function that determines some metadata of an image file.

    Parameters
    ----------
    fname : str
        s3cmd_url, https_url, or local filepath to the image
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
        Variable 's3_client' must exist and hold an enter-result of an async with statement
        invoking :func:`mt.base.s3.create_s3_client`. In asynchronous mode, variable
        'http_session' must exist and hold an enter-result of an async with statement invoking
        :func:`mt.base.http.create_http_session`. You can use
        :func:`wml.core.s3.create_context_vars` to create a dictionary like this.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging messages

    Returns
    -------
    dict
        a dictionary `{'width': image_width, 'height': image_height, 'nchannels': number_of_channels, 'type': image_type}`.
        If the file is not an image, then the dictionary is `{'type': None}`

    Notes
    -----
    We use a local derived file `image_localpath+'.immeta'` to save the computed metadata for future reuse.

    Raises
    ------
    OSError
        if file not found
    """

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    s3cmd_url = as_s3cmd_url(fname, raise_exception=False)
    if s3cmd_url is None:  # assume local file given
        image_localpath = fname
    else:  # remote file given
        image_localpath = await cache_asyn(
            s3cmd_url, verbose_check=False, context_vars=context_vars, logger=logger
        )

    if not path.exists(image_localpath):
        if fname == image_localpath:
            msg = "Local image file '{}' does not exist.".format(fname)
        else:
            msg = "Local path '{}' of image file '{}' does not exist.".format(
                image_localpath, fname
            )
        raise OSError(msg)

    meta_filepath = image_localpath + ".immeta"

    if path.exists(meta_filepath):
        try:
            meta = await aio.json_load(meta_filepath, context_vars=context_vars)
            if "type" in meta:
                return meta
        except json.decoder.JSONDecodeError:  # broken file
            meta = None

    what = await filetype.image_match_asyn(image_localpath, context_vars=context_vars)
    if what is not None:
        what = what.mime[6:]
    meta = {"type": what}
    if what:  # valid image
        try:
            im = await cv.imload(image_localpath, context_vars=context_vars)
            meta["width"] = im.shape[1]
            meta["height"] = im.shape[0]
            meta["nchannels"] = 1 if len(im.shape) == 2 else im.shape[2]
        except ValueError:  # corrupted image file
            if logger:
                logger.warn_last_exception()
            meta["type"] = None

    await aio.json_save(meta_filepath, meta, context_vars=context_vars)

    return meta


def immeta(fname, logger=None):
    """Determines some metadata of an image file.

    Parameters
    ----------
    fname : str
        s3cmd_url, https_url, or local filepath to the image
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging messages

    Returns
    -------
    dict
        a dictionary `{'width': image_width, 'height': image_height, 'nchannels': number_of_channels, 'type': image_type}`. If the file is not an image, then the dictionary is `{'type': None}`

    Notes
    -----
    We use a local derived file `image_localpath+'.immeta'` to save the computed metadata for future reuse.

    Raises
    ------
    OSError
        if file not found
    """

    return aio.srun(immeta_asyn, fname, logger=logger)


async def imread_impl(
    filepath,
    plugin: tp.Optional[str] = None,
    extension: tp.Optional[str] = None,
    format_hint: tp.Optional[str] = None,
    plugin_kwargs: dict = {},
    context_vars: dict = {},
):
    l_substrs = [
        "mlcore/s3/vision-waste-image-final-prod",
        "mlcore/s3/c76a090f-0e84-44f4-98bf-fe0469e163cd",
    ]
    for x in l_substrs:
        if x in filepath:  # jpeg file?
            return await jpegload(filepath, context_vars=context_vars)
    filepath_lower = filepath.lower()
    if filepath_lower.endswith(".jpg") or filepath_lower.endswith(".jpeg"):
        return await jpegload(filepath, context_vars=context_vars)
    return await iio.imread_asyn(
        filepath,
        plugin=plugin,
        extension=extension,
        format_hint=format_hint,
        context_vars=context_vars,
        **plugin_kwargs,
    )


async def imread_asyn(
    fname,
    plugin: tp.Optional[str] = None,
    extension: tp.Optional[str] = None,
    format_hint: tp.Optional[str] = None,
    plugin_kwargs: dict = {},
    context_vars: dict = {},
    logger=None,
):
    """An asyn function that loads an image file for ML with a logger and an additional OSError check.

    Parameters
    ----------
    fname : str
        s3cmd_url, https_url, or local filepath to the image
    plugin : str, optional
        Only valid if the function falls back to imageio.v3.imread. The plugin to use. If set to
        None (default) imread will perform a search for a matching plugin. If not None, this takes
        priority over the provided format hint (if present).
    extension : str, optional
        Only valid if the function falls back to imageio.v3.imread. If not None, treat the provided
        ImageResource as if it had the given extension. This affects the order in which backends
        are considered.
    format_hint : str, optional
        Only valid if the function falls back to imageio.v3.imread. A format hint to help optimize
        plugin selection given as the format’s extension, e.g. '.png'. This can speed up the
        selection process for ImageResources that don’t have an explicit extension, e.g. streams,
        or for ImageResources where the extension does not match the resource’s content.
    plugin_kwargs : dict
        Only valid if the function falls back to imageio.v3.imread. Additional keyword arguments to
        be passed as-is to the plugin's read call.
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
        Variable 's3_client' must exist and hold an enter-result of an async with statement
        invoking :func:`mt.base.s3.create_s3_client`. In asynchronous mode, variable
        'http_session' must exist and hold an enter-result of an async with statement invoking
        :func:`mt.base.http.create_http_session`. You can use
        :func:`wml.core.s3.create_context_vars` to create a dictionary like this.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging messages

    Notes
    -----
    We additionally search for the image in our local s3 cache, saving data bandwidth.

    This imread version differs in mtopencv's imread version in that the output color image has RGB
    channels instead of OpenCV's old style BGR channels.

    Raises
    ------
    ValueError
    OSError

    See Also
    --------
    mt.cv.imread
        mtopencv' imread function
    """

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    s3cmd_url = as_s3cmd_url(fname, raise_exception=False)
    if s3cmd_url is None:  # normal way
        try:
            return await iio.imread_asyn(
                fname,
                plugin=plugin,
                extension=extension,
                format_hint=format_hint,
                context_vars=context_vars,
                **plugin_kwargs,
            )
        except:
            logg.warn(f"Caught an exception while imreading '{fname}'.", logger=logger)
            raise

    for i in range(3):
        localpath = await cache_asyn(
            s3cmd_url, verbose_check=False, context_vars=context_vars, logger=logger
        )

        if path.getsize(localpath) > 0:
            break

        path.remove(localpath)
        # and any immeta file associated with it
        path.remove(localpath + ".immeta")

        if i == 2:
            raise OSError("Empty remote image '{}'.".format(fname))

        if logger:
            logger.warning(
                "Empty cache file detected, attempting #{} to redownload".format(i + 1)
            )
            logger.warning("  remote image '{}'.".format(fname))

        await aio.sleep(i + 1, context_vars=context_vars)

    try:
        retval = await imread_impl(
            localpath,
            plugin=plugin,
            extension=extension,
            format_hint=format_hint,
            plugin_kwargs=plugin_kwargs,
            context_vars=context_vars,
        )
        return retval
    except (ValueError, OSError, RuntimeError, TypeError) as e:
        if logger:
            logger.warn_last_exception()
            logger.warning("{} intercepted while trying to imread".format(e.__class__))
            logger.warning("  cache file '{}'".format(localpath))
            logger.warning("    size {}".format(path.getsize(localpath)))
            logger.warning("  of remote image '{}'.".format(fname))

        # attempt to redownload once
        path.remove(localpath)
        # and any immeta file associated with it
        path.remove(localpath + ".immeta")
        if logger:
            logger.info("Removed the cache file. Attempting to redownload it.")
        await aio.sleep(1, context_vars=context_vars)
        localpath = await cache_asyn(
            s3cmd_url, verbose_check=False, context_vars=context_vars, logger=logger
        )

        try:
            retval = await imread_impl(
                localpath,
                plugin=plugin,
                extension=extension,
                format_hint=format_hint,
                plugin_kwargs=plugin_kwargs,
                context_vars=context_vars,
            )
            return retval
        except (ValueError, OSError, RuntimeError, TypeError) as e:
            if logger:
                logger.error("The remote image file '{}' is corrupted.".format(fname))
            raise


def imread(
    fname,
    plugin: tp.Optional[str] = None,
    extension: tp.Optional[str] = None,
    format_hint: tp.Optional[str] = None,
    plugin_kwargs: dict = {},
    logger=None,
):
    """Loads an image file for ML with a logger and an additional OSError check.

    Parameters
    ----------
    fname : str
        s3cmd_url, https_url, or local filepath to the image
    plugin : str, optional
        Only valid if the function falls back to imageio.v3.imread. The plugin to use. If set to
        None (default) imread will perform a search for a matching plugin. If not None, this takes
        priority over the provided format hint (if present).
    extension : str, optional
        Only valid if the function falls back to imageio.v3.imread. If not None, treat the provided
        ImageResource as if it had the given extension. This affects the order in which backends
        are considered.
    format_hint : str, optional
        Only valid if the function falls back to imageio.v3.imread. A format hint to help optimize
        plugin selection given as the format’s extension, e.g. '.png'. This can speed up the
        selection process for ImageResources that don’t have an explicit extension, e.g. streams,
        or for ImageResources where the extension does not match the resource’s content.
    plugin_kwargs : dict
        Only valid if the function falls back to imageio.v3.imread. Additional keyword arguments to
        be passed as-is to the plugin's read call.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging messages

    Notes
    -----
    We additionally search for the image in our local s3 cache, saving data bandwidth.

    This imread version differs in mtopencv's imread version in that the output color image has RGB
    channels instead of OpenCV's old style BGR channels.

    Raises
    ------
    ValueError
    OSError

    See Also
    --------
    mt.cv.imread
        mtopencv' imread function
    """

    return aio.srun(
        imread_asyn,
        fname,
        plugin=plugin,
        extension=extension,
        format_hint=format_hint,
        plugin_kwargs=plugin_kwargs,
        logger=logger,
        extra_context_vars=default_context_vars,
    )


async def imexists_asyn(filepath, context_vars: dict = {}):
    """An asyn function that checks if a local file exists and it is either an image file or an .imm file."""

    if not path.exists(filepath):
        return False
    if filepath.lower().endswith(".imm"):
        return True
    retval = await filetype.is_image_asyn(filepath, context_vars=context_vars)
    return retval


def imexists(filepath):
    """Checks if a local file exists and it is either an image file or an .imm file."""
    return aio.srun(imexists_asyn, filepath)


def imremove(fname):
    """Removes an image file and its meta file from cache, if any.

    Parameters
    ----------
    fname : str
        s3cmd_url, https_url, or local filepath to the image
    """

    if "://" in fname:  # needs converting
        if fname.startswith("http"):
            fname = as_s3cmd_url(fname)
        fname = cache_localpath(fname)
    if path.exists(fname):
        path.remove(fname)
        # and any immeta file associated with it
        path.remove(fname + ".immeta")
