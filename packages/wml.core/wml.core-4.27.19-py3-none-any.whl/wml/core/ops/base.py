# pylint: disable=line-too-long, invalid-name, relative-beyond-top-level

"""Base ops."""

from mt import np, base


def rescale_range(
    x,
    src_min: float,
    src_max: float,
    dst_min: float,
    dst_max: float,
    clip: bool = False,
):
    """Rescale the pixel values from one range to another.

    Each pixel value of the input tensor `x` is affinely rescaled so that `src_min` becomes
    `dst_min` and `src_max` becomes `dst_max`.

    Parameters
    ----------
    x : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the input tensor of floating dtype
    src_min : float
        the source min value
    src_max : float
        the source max value. Must be greater than `src_min`.
    dst_min : float
        the target min value
    dst_max : float
        the target max value. Must be greater than `dst_min`.
    clip : bool
        whether or not to clip the target pixel values to the range ``[dst_min, dst_max]``

    Returns
    -------
    y : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the output tensor of the same dtype and shape as the input tensor
    """

    a = (dst_max - dst_min) / (src_max - src_min)
    b = dst_min - a * src_min

    if base.is_ndarray(x):
        y = x * a + b
        if clip:
            np.clip(y, dst_min, dst_max, out=y)
    elif base.is_tftensor(x):
        from mt import tf

        y = x * a + b
        if clip:
            y = tf.clip_by_value(y, dst_min, dst_max)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return y


def is_finite(x):
    """Checks if each component of a tensor is finite or not.

    Parameters
    ----------
    x : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the input tensor of floating dtype

    Returns
    -------
    y : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the output tensor of bool dtype and the same shape as the input tensor
    """

    if base.is_ndarray(x):
        return np.isfinite(x)

    if base.is_tftensor(x):
        from mt import tf

        if x.dtype not in (tf.bfloat16, tf.half, tf.float32, tf.float64):
            return True

        return tf.math.is_finite(x)

    raise NotImplementedError("Neither an ndarray or a tf tensor was given.")


def is_all_finite(x):
    """Checks if all components of a tensor is finite or not.

    Parameters
    ----------
    x : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the input tensor of floating dtype

    Returns
    -------
    y : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        the output scalar of bool dtype telling whether or not all components
        of x are finite
    """

    if base.is_ndarray(x):
        return np.all(np.isfinite(x))

    if base.is_tftensor(x):
        from mt import tf

        if x.dtype not in (tf.bfloat16, tf.half, tf.float32, tf.float64):
            return True

        return tf.math.reduce_all(tf.math.is_finite(x))

    raise NotImplementedError("Neither an ndarray or a tf tensor was given.")
