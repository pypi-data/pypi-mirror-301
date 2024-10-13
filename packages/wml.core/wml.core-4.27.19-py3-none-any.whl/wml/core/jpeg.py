"""Module for efficiently loading jpeg files via flexibily choosing the best package among TurboJPEG, scikit-image, or OpenCV."""

import warnings
import numpy as np
from mt import aio
from mt.base import logger

__all__ = ["jpegload"]


try:
    from turbojpeg import TurboJPEG

    jp = TurboJPEG()

    async def jpegload(filepath: str, context_vars: dict = {}) -> np.ndarray:
        buf = await aio.read_binary(filepath, context_vars=context_vars)
        with warnings.catch_warnings(record=True) as l_wMsgs:
            arr = jp.decode(buf)
        if len(l_wMsgs) > 0:
            with logger.scoped_warn("Caught warnings while jpeg-loading", curly=False):
                logger.warn("file: {}".format(filepath))
                for wMsg in l_wMsgs:
                    warnings.warn(wMsg)
        if len(arr.shape) == 3 and arr.shape[2] == 3:  # BGR->RGB
            arr = arr[:, :, ::-1].copy()
            return arr

except ImportError:
    try:
        from mt import cv

        logger.warn(
            "IMPORT: Package PyTurboJPEG is not installed. Falling back to OpenCV to read JPEG."
        )

        async def jpegload(filepath: str, context_vars: dict = {}) -> np.ndarray:
            arr = await cv.imload(filepath, context_vars=context_vars)
            if len(arr.shape) == 3 and arr.shape[2] == 3:  # BGR->RGB
                arr = arr[:, :, ::-1].copy()
            return arr

    except ImportError:
        import imageio.v3 as iio

        try:
            logger.warn(
                "IMPORT: Neither package PyTurboJPEG nor OpenCV is installed. Falling back to imageio to read JPEG."
            )

            async def jpegload(filepath: str, context_vars: dict = {}) -> np.ndarray:
                return iio.imread(filepath)

        except ImportError:
            raise ImportError(
                "None of these package found to read JPEG: PyTurboJPEG, OpenCV, or imageio."
            )

jpegload.__doc__ = """An asyn function that loads a JPEG buffer into an RGB image or a grayscale image.

    Parameters
    ----------
    filepath : str
        path to a jpeg file
    context_vars : dict
        a dictionary of context variables within which the function runs. It must include
        `context_vars['async']` to tell whether to invoke the function asynchronously or not.

    Returns
    -------
    numpy.ndarray
        the loaded image
"""
