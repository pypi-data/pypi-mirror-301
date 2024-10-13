from . import s3
from urllib import parse

from mt import tp, logg, aio

__all__ = ["resolve_resource_asyn", "resolve_resource"]


async def resolve_resource_asyn(
    resource_url,
    check_update=True,
    context_vars: dict = {},
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """
    An asyn function that resolves a given URL to a local path, caching resources if necessary

    Parameters
    ----------
    resource_url: string
        The original URL of the resource
    check_update: boolean
        (Optional) in case of a cacheable resource (e.g. S3), allows for a check in the upstream
        source for changes
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.
        Variable 's3_client' must exist and hold an enter-result of an async with statement
        invoking :func:`mt.base.s3.create_s3_client`. In asynchronous mode, variable
        'http_session' must exist and hold an enter-result of an async with statement invoking
        :func:`mt.base.http.create_http_session`. You can use
        :func:`wml.core.s3.create_context_vars` to create a dictionary like this.
    logger: mt.logg.IndentedLoggerAdapter, optional
        (Optional) logger instance to be used for log messages

    Returns
    -------
    string
        The location of the resolved resource on the local filesystem
    """

    scheme_resolvers = {
        # use __s3 resolver for all of these prefixes for now
        "s3": __s3,
        "ml": __s3,
        "im": __s3,
        "goods": __s3,
        "file": __file,
    }
    url = parse.urlparse(resource_url)
    resolver = scheme_resolvers.get(url.scheme)

    if resolver:
        result = await resolver(resource_url, url, check_update, context_vars, logger)
        if logger:
            logger.info("Resolved resource url:")
            logger.info("  from: {}".format(resource_url))
            logger.info("    to: {}".format(result))
        return result
    else:
        if logger:
            logger.info("No specific resolver found for {}".format(resource_url))
        return resource_url


async def __s3(original_url, parsed_url, check_update, context_vars, logger):
    return await s3.cache_asyn(
        original_url,
        verbose_check=check_update,
        context_vars=context_vars,
        logger=logger,
    )


async def __file(original_url, parsed_url, check_update, context_vars, logger):
    if parsed_url.netloc and parsed_url.netloc != "":
        return parsed_url.netloc + parsed_url.path
    else:
        return parsed_url.path


def resolve_resource(
    resource_url,
    check_update=True,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """
    Resolves a given URL to a local path, caching resources if necessary

    Parameters
    ----------
    resource_url: string
        The original URL of the resource
    check_update: boolean
        (Optional) in case of a cacheable resource (e.g. S3), allows for a check in the upstream
        source for changes
    logger: mt.logg.IndentedLoggerAdapter, optional
        (Optional) logger instance to be used for log messages

    Returns
    -------
    string
        The location of the resolved resource on the local filesystem
    """
    return aio.srun(
        resolve_resource_asyn,
        resource_url,
        check_update=check_update,
        extra_context_vars=s3.default_context_vars,
        logger=logger,
    )
