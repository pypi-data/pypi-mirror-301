# pylint: disable=line-too-long, invalid-name, relative-beyond-top-level

"""Ops supporting DUC encoder and decoder models."""

from mt import tp, np, base


def unstack(ai_ducImages, N: int):
    """Unstacks a batch of DUC images.

    The function unstacks and reshapes a batch of shape `(B, H0 * N, W0, D)` to a batch of shape
    `(B, H0, W0, D * N)`.

    Parameters
    ----------
    ai_ducImages : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, H0 * N, W0, D)` in numpy array or tf tensor.
    N : int
        the number of items in each stack

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B, H0, W0, D * N)` and same dtype
    """

    x = ai_ducImages

    if base.is_ndarray(x):
        B = x.shape[0]
        HN = x.shape[1]
        if HN % N != 0:
            raise ValueError("The height {} is not a multiple of {}.".format(HN, N))
        H0 = HN // N
        W0 = x.shape[2]
        D = x.shape[3]
        x = np.reshape(x, [B, N, H0, W0, D])
        x = np.transpose(x, axes=[0, 2, 3, 1, 4])
        x = np.reshape(x, [B, H0, W0, D * N])
    elif base.is_tftensor(x):
        from mt import tf

        x_shape = tf.shape(x)
        B = x_shape[0]
        H0 = x_shape[1] // N
        W0 = x_shape[2]
        D = x_shape[3]
        x = tf.reshape(x, [B, N, H0, W0, D])
        x = tf.transpose(x, perm=[0, 2, 3, 1, 4])
        x = tf.reshape(x, [B, H0, W0, D * N])
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return x


def stack(ai_ducImages, N: int):
    """Stacks a batch of DUC images.

    The function stacks and reshapes a batch of shape `(B, H0, W0, D*N)` to a batch of shape
    `(B, H0*N, W0, D)`.

    Parameters
    ----------
    ai_ducImages : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, H0, W0, D*N)` in numpy array or tf tensor.
    N : int
        the number of items in each stack

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B, H0*N, W0, D)` and same dtype
    """

    x = ai_ducImages

    if base.is_ndarray(x):
        B = x.shape[0]
        H0 = x.shape[1]
        W0 = x.shape[2]
        DN = x.shape[3]
        if DN % N != 0:
            raise ValueError(
                "The pixel dimensionality {} is not a multiple of {}.".format(DN, N)
            )
        D = DN // N
        x = np.reshape(x, [B, H0, W0, N, D])
        x = np.transpose(x, axes=[0, 3, 1, 2, 4])
        x = np.reshape(x, [B, H0 * N, W0, D])
    elif base.is_tftensor(x):
        from mt import tf

        x_shape = tf.shape(x)
        B = x_shape[0]
        H0 = x_shape[1]
        W0 = x_shape[2]
        D = x_shape[3] // N
        x = tf.reshape(x, [B, H0, W0, N, D])
        x = tf.transpose(x, perm=[0, 3, 1, 2, 4])
        x = tf.reshape(x, [B, H0 * N, W0, D])
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return x


def block22(ai_inputs, output_avg: bool = False):
    """Groups 2x2 blocks of pixels.

    The function takes as input a batch of shape `[B, H*2, W*2, D]`, groups pixels into 2x2 blocks
    in height and width, flattens the pixel dimensions in each group, and returns a batch of shape
    `[B, H, W, 2*2*D]`.

    Parameters
    ----------
    ai_inputs : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, H*2, W*2, D)` in numpy array or tf tensor.
    output_avg : bool
        whether or not to output the average tensor

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B, H, W, 2*2*D)` and same dtype
    numpy.ndarray or tensorflow.Tensor
        the average batch of shape `(B, H, W, D)` and same dtype. Only available if `output_avg` is
        True.
    """

    x = ai_inputs

    if base.is_ndarray(x):
        B = x.shape[0]
        H = x.shape[1]
        if H % 2 != 0:
            raise ValueError("The height {} is not even.".format(H))
        H >>= 1
        W = x.shape[2]
        if W % 2 != 0:
            raise ValueError("The width {} is not even.".format(W))
        W >>= 1
        D = x.shape[3]
        x = np.reshape(x, [B, H, 2, W, 2, D])
        if output_avg:
            x_avg = np.mean(x, axis=(2, 4), keepdims=False)
        x = np.transpose(x, axes=[0, 1, 3, 2, 4, 5])
        x = np.reshape(x, [B, H, W, 2 * 2 * D])
    elif base.is_tftensor(x):
        from mt import tf

        x_shape = tf.shape(x)
        B = x_shape[0]
        H = x_shape[1] // 2
        W = x_shape[2] // 2
        D = x_shape[3]
        x = tf.reshape(x, [B, H, 2, W, 2, D])
        if output_avg:
            x_avg = tf.reduce_mean(x, axis=[2, 4], keepdims=False)
        x = tf.transpose(x, perm=[0, 1, 3, 2, 4, 5])
        x = tf.reshape(x, [B, H, W, 2 * 2 * D])
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    if output_avg:
        return x, x_avg
    return x


def unblock22(ai_inputs, ai_shifts=None):
    """Ungroups 2x2 blocks of pixels.

    The function takes as input a batch of shape `[B, H, W, 4*D]`, splits each pixel into 4 pixels
    of dimension `D` each, forms them into a 2x2 block, merges 2 to the height dimension and the
    other 2 to the width dimension, and returns a batch of shape `[B, H*2, W*2, D]`.

    Parameters
    ----------
    ai_inputs : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, H, W, 4*D)` in numpy array or tf tensor.

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B, H*2, W*2, D)` and same dtype
    """

    x = ai_inputs

    if base.is_ndarray(x):
        B = x.shape[0]
        H = x.shape[1]
        W = x.shape[2]
        D = x.shape[3]
        if D % 4 != 0:
            raise ValueError(
                "The pixel dimensionality {} is not divisible by 4.".format(W)
            )
        D >>= 2
        x = np.reshape(x, [B, H, W, 2, 2, D])
        if ai_shifts is not None:
            x += ai_shifts[:, :, :, np.newaxis, np.newaxis, :]
        x = np.transpose(x, axes=[0, 1, 3, 2, 4, 5])
        x = np.reshape(x, [B, H * 2, W * 2, D])
    elif base.is_tftensor(x):
        from mt import tf

        x_shape = tf.shape(x)
        B = x_shape[0]
        H = x_shape[1]
        W = x_shape[2]
        D = x_shape[3] // 4
        x = tf.reshape(x, [B, H, W, 2, 2, D])
        if ai_shifts is not None:
            x += ai_shifts[:, :, :, tf.newaxis, tf.newaxis, :]
        x = tf.transpose(x, perm=[0, 1, 3, 2, 4, 5])
        x = tf.reshape(x, [B, H * 2, W * 2, D])
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return x


def mean_squared(x):
    """Computes the mean of squared values for each batch item.

    Parameters
    ----------
    x : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, ...)` in numpy array or tf tensor

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B,)` and same dtype representing the mean of squared values
        for each batch item
    """

    if base.is_ndarray(x):
        if len(x.shape) > 2:
            x = x.reshape((x.shape[0], -1))
        x = np.mean(x * x, axis=-1, keepdims=False)
    elif base.is_tftensor(x):
        from mt import tf

        x = tf.reshape(x, [tf.shape(x)[0], -1])
        x = tf.reduce_mean(x * x, axis=-1, keepdims=False)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return x


def mse(x, y):
    """Computes the mean squared errors between two tensors of the same shape.

    Parameters
    ----------
    x : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of shape `(B, ...)` in numpy array or tf tensor
    y : numpy.ndarray or tensorflow.Tensor or tensorflow.KerasTensor
        a batch of same shape `(B, ...)` in numpy array or tf tensor

    Returns
    -------
    numpy.ndarray or tensorflow.Tensor
        the output batch of shape `(B,)` and same dtype representing the mean squared error
        for each batch item
    """

    return mean_squared(y - x)
