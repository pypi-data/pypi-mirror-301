"""Batch processing a dataframe."""

from mt import tp, pd, logg
from mt.pandas.dataframe_processing import *


process_dataframe_base = process_dataframe


async def process_dataframe(
    df: pd.DataFrame,
    preprocess_func,
    batchprocess_func=None,
    postprocess_func=None,
    rng_seed: int = 0,
    num_iters: tp.Optional[int] = None,
    preprocess_args: tuple = (),
    preprocess_kwargs: dict = {},
    batchprocess_args: tuple = (),
    batchprocess_kwargs: dict = {},
    postprocess_args: tuple = (),
    postprocess_kwargs: dict = {},
    skip_null: bool = False,
    iter_policy: str = "sequential",
    resampling_col: tp.Optional[str] = None,
    batch_size: int = 32,
    max_concurrency: int = 16,
    context_vars: dict = {},
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    from .s3 import get_default_s3_profile

    s3_profile = get_default_s3_profile()
    return await process_dataframe_base(
        df,
        preprocess_func,
        batchprocess_func=batchprocess_func,
        postprocess_func=postprocess_func,
        rng_seed=rng_seed,
        num_iters=num_iters,
        preprocess_args=preprocess_args,
        preprocess_kwargs=preprocess_kwargs,
        batchprocess_args=batchprocess_args,
        batchprocess_kwargs=batchprocess_kwargs,
        postprocess_args=postprocess_args,
        postprocess_kwargs=postprocess_kwargs,
        skip_null=skip_null,
        iter_policy=iter_policy,
        resampling_col=resampling_col,
        batch_size=batch_size,
        s3_profile=s3_profile,
        max_concurrency=max_concurrency,
        context_vars=context_vars,
        logger=logger,
    )


process_dataframe.__doc__ = (
    process_dataframe_base.__doc__
    + """
    This function wraps :func:`mt.base.dataframe_processing.process_dataframe` with argument
    's3_profile' set to be the returning string of :func:`wml.core.s3.get_default_s3_profile`.
"""
)
