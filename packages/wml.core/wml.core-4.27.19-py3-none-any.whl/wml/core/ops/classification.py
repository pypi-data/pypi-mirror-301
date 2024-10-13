# pylint: disable=line-too-long, invalid-name, relative-beyond-top-level

"""Stuff related to classification."""

import warnings
import math

from mt import np, base


def softmax(tv_logits):
    """Transforms a tensor of logit vectors to a tensor of softmax vectors.

    Parameters
    ----------
    tv_logits : array_like
        a tensor of logit vectors of shape shape `(...,J)` and dtype float32 where `J` is the
        number of classes. The tensor can be a numpy array or a tensorflow tensor. No checking is
        implemented.

    Returns
    -------
    tv_probs : array_like
        a tensor of softmax vectors. The tensor has the same type, shape and dtype as the input
        tensor.
    """

    if base.is_ndarray(tv_logits):
        x = np.exp(tv_logits - tv_logits.mean(axis=-1))
        x /= x.sum(axis=-1)
    elif base.is_tftensor(tv_logits):
        from mt import tf

        x = tv_logits - tf.reduce_mean(tv_logits, axis=-1, keepdims=True)
        x = tf.math.exp(x)
        x = tf.math.divide_no_nan(x, tf.reduce_sum(x, axis=-1, keepdims=True))
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return x


def confidence(tv_probs, ndim=None):
    """Computes the classification confidences from a tensor of softmax vectors.

    The classification confidence of a softmax vector `x` is defined as:

    `conf(x) = 1 - H(x)/log2(n) = D_{KL}(x||u)/log2(n)`

    where `n` is the dimensionality of `x` and `H(x)` is the entropy of `x`, `u` is the softmax
    vector that represents the uniform distribution.

    The range of `conf(x)` is `[0,1]` where 0 means it is least unconfident and 1 means it is most
    confident.

    Parameters
    ----------
    tv_probs : array_like
        a tensor of softmax vectors of non-negative components with positive component sums. The
        tensor has shape `(...,J)` of dtype float32 where `J` is the number of classes. The tensor
        can be a numpy array or a tensorflow tensor. Each softmax vector will be  normalised into a
        pmf internally before computing. No checking is implemented.
    ndim : scalar, optional
        the the dimensionaliy of the softmax vector. If not provided,  ``tv_probs.shape[-1]`` is
        used.

    Returns
    -------
    t_confs : array_like
        a tensor of classification confidences of the softmax vectors, with the same data type as
        input, and with the same shape but without the last dimension of `J` components, `(...,)`.
    """

    if base.is_ndarray(tv_probs):
        x = np.divide_no_nan(tv_probs, tv_probs.sum(axis=-1))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x_log2x = np.where(x > 0, x * np.log2(x), 0.0)  # to avoid 0*log2(0)
            hx = -x_log2x.sum(axis=-1)
            if ndim is None:
                ndim = x.shape[-1]
            if ndim > 1:
                conf_x = 1.0 - hx / math.log2(ndim)
            else:
                conf_x = np.ones(x.shape[0])
    elif base.is_tftensor(tv_probs):
        from mt import tf

        x = tf.math.divide_no_nan(
            tv_probs, tf.reduce_sum(tv_probs, axis=-1, keepdims=True)
        )
        x_logx = tf.where(x > 0, x * tf.math.log(x), 0.0)  # to avoid 0*log(0)
        hx = -tf.reduce_sum(x_logx, axis=-1)
        if ndim is None:
            ndim = tf.shape(x)[-1]
        ndim = tf.cast(ndim, tf.float32)
        hx2 = tf.math.divide_no_nan(hx, tf.math.log(ndim))
        conf_x = tf.where(ndim > 1, 1 - hx2, 1.0)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return conf_x


def binary_confidence(t_probs):
    """Computes the binary classification confidences from a tensor of probabilities.

    Each cell of the tensor is treated as a separate binary classification problem where the value
    of the cell represents the predicted probability of the positive class. The binary
    classification confidence of predicted positive probability `x` is defined as:

    `bconf(x) = 1 - H(x) = 1 + (1-x) log2(1-x) + x log2(x)`

    where `H(x)` is the binary entropy of `x`.

    `bconf(x)` is a special case of `conf(x)` where `n = 2`. The range of `bconf(x)` is `[0,1]`
    where 0 means it is least unconfident and 1 means it is most confident.

    Parameters
    ----------
    t_probs : array_like
        a tensor of [0,1] cells and is of dtype float32. The tensor can be a numpy array or a
        tensorflow tensor. No checking is implemented.

    Returns
    -------
    t_bconfs : array_like
        a tensor of binary classification confidences, with the same shape and dtype as input.
    """

    if base.is_ndarray(t_probs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = np.stack([t_probs, 1.0 - t_probs], axis=-1)
            x_log2x = np.where(x > 0, x * np.log2(x), 0.0)  # to avoid 0*log2(0)
            bconf_x = 1 + x_log2x.sum(axis=-1)
    elif base.is_tftensor(t_probs):
        from mt import tf

        x = tf.stack([t_probs, 1.0 - t_probs], axis=-1)
        x_logx = tf.where(x > 0, x * tf.math.log(x), 0.0)  # to avoid 0*log(0)
        bconf_x = 1.0 + tf.reduce_sum(x_logx, axis=-1)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return bconf_x


def set_prob(tv_trues, tv_probs, eps: float = 1e-8):
    """Computes set probabilities.

    Given a tensor/batch of true class sets ``x`` where ``x[i,j]`` being zero or one telling
    whether class j is a true class for batch item i or not, and a tensor/batch of softmax
    vectors ``y`` of the same shape as ``x``, the set_prob function outputs a 1D tensor/batch
    ``z`` where ``z[i] = reduce_sum(x[i]*y[i], axis=1)`` if ``x[i]`` is non-zero vector and
    ``z[i] = 1`` if ``x[i]`` is the zero vector.

    Parameters
    ----------
    tv_trues : array_like
        a tensor of shape ``(N,J)`` of zeros and ones such that for an item at location (i,j), it
        tells whether class j is a true class for batch item i or not.. The tensor can be a numpy
        array or a tensorflow tensor.
    tv_probs : array_like
        a tensor of softmax vectors of non-negative components with positive component sums. The
        tensor has shape `(...,J)` of dtype float32 where `J` is the number of classes. The tensor
        can be a numpy array or a tensorflow tensor. No internal softmax normalisation is
        implemented.
    eps : float
        small value to check for zero vectors

    Returns
    -------
    t_setProbs : array_like
        a tensor of set probabilities, with the same data type as the inputs, and with the same
        shape but without the last dimension of `J` components, `(...,)`.
    """

    if base.is_ndarray(tv_trues):
        t_setProbs = np.where(
            tv_trues.sum(axis=-1) > eps, (tv_trues * tv_probs).sum(axis=-1), 1.0
        )
    elif base.is_tftensor(tv_trues):
        from mt import tf

        t_setProbs = tf.where(
            tf.reduce_sum(tv_trues, axis=-1) > eps,
            tf.reduce_sum(tv_trues * tv_probs, axis=-1),
            1.0,
        )
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return t_setProbs


def neg_log(t_probs, eps: float = 1e-8):
    """Computes negative natural logarithms of elements of tensor.

    Parameters
    ----------
    t_probs : array_like
        a tensor of probabilities. The tensor can be a numpy array or a tensorflow tensor.
    eps : float
        small value to check for zero probabilities

    Returns
    -------
    t_negLogs : array_like
        a tensor of negative natural logarithms of probabilities, with the same data type and shape
        as the input tensor.
    """

    if base.is_ndarray(t_probs):
        t_probs = np.where(t_probs > eps, t_probs, eps)
        t_negLogs = -np.log(t_probs)
    elif base.is_tftensor(t_probs):
        from mt import tf

        t_probs = tf.where(t_probs > eps, t_probs, eps)
        t_negLogs = -tf.math.log(t_probs)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return t_negLogs


def label_metrics(tv_trues, tv_probs, eps: float = 1e-8):
    """Computes label metrics.

    Given a tensor/batch of true class sets ``x`` with shape (B,J) where ``x[i,j]`` being zero or
    one telling whether class j is a true class for batch item i or not, and a tensor/batch of
    softmax vectors ``y`` of the same shape as ``x``, the label_metrics function outputs a
    tensor/batch of shape (B,9) telling for each batch item the 'setprob', 'setconf', 'setacc',
    'confidence', 'accuracy', 'rank', 'top1', 'top8' metrics when comparing the two input
    tensors.

    Parameters
    ----------
    tv_trues : array_like
        a tensor of shape (B,J) of zeros and ones such that for an item at location (i,j), it tells
        whether class j is a true class for batch item i or not.. The tensor can be a numpy array
        or a tensorflow tensor.
    tv_probs : array_like
        a tensor of softmax vectors of the same shape as `tv_trues` and with non-negative
        components in each row summing up to 1. The tensor can be a numpy array or a tensorflow
        tensor. No internal softmax normalisation is implemented.
    eps : float
        small value to check for zeros

    Returns
    -------
    tv_labelMetrics : array_like
        a tensor of label metrics of shape (B,9), with the same dtype as the inputs.
    """

    t_confs = confidence(tv_probs)
    t_setProbs = set_prob(tv_trues, tv_probs, eps=eps)
    t_setConfs = binary_confidence(t_setProbs)

    if base.is_ndarray(tv_trues):
        t_setAccs = (t_setProbs >= 0.5).astype(tv_probs.dtype)
        t_targets = np.argmax(tv_trues, axis=1)
        t_accs = np.take(tv_probs, t_targets, axis=1)
        t_sortedIndices = np.argsort(-tv_probs, axis=1)  # in descending order
        t_equals = t_sortedIndices == t_targets[:, np.newaxis]
        t_ranks = np.argmax(t_equals, axis=1)
        t_ranks2 = t_ranks.astype(tv_probs.dtype)
        t_top1s = (t_ranks < 1).astype(tv_probs.dtype)
        t_top8s = (t_ranks < 8).astype(tv_probs.dtype)

        tv_labelMetrics = np.stack(
            [
                t_setProbs,
                t_setConfs,
                t_setAccs,
                t_confs,
                t_accs,
                t_ranks2,
                t_top1s,
                t_top8s,
            ],
            axis=1,
        )
    elif base.is_tftensor(tv_trues):
        from mt import tf

        t_setAccs = tf.cast(t_setProbs >= 0.5, tv_probs.dtype)
        t_targets = tf.math.argmax(tv_trues, axis=1)
        t_accs = tf.gather(tv_probs, t_targets, axis=1, batch_dims=1)
        t_sortedIndices = tf.argsort(tv_probs, axis=1, direction="DESCENDING")
        t_equals = t_sortedIndices == tf.cast(t_targets[:, tf.newaxis], tf.int32)
        t_ranks = tf.math.argmax(t_equals, axis=1)
        t_ranks2 = tf.cast(t_ranks, tv_probs.dtype)
        t_top1s = tf.cast(t_ranks < 1, tv_probs.dtype)
        t_top8s = tf.cast(t_ranks < 8, tv_probs.dtype)

        tv_labelMetrics = tf.stack(
            [
                t_setProbs,
                t_setConfs,
                t_setAccs,
                t_confs,
                t_accs,
                t_ranks2,
                t_top1s,
                t_top8s,
            ],
            axis=1,
        )
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return tv_labelMetrics


label_metrics.names = [
    "setprob",
    "setconf",
    "setacc",
    "confidence",
    "accuracy",
    "rank",
    "top1",
    "top8",
]


def nms(bt_scores, *args):
    """Global non-maximum suppression.

    Suppose there is a batch `bt_scores` of tensors of scores of shape ``(B,) + X``. Each score is
    associated with a location. For each batch item, let the max-location be the location with the
    maximum score.

    Next, suppose that on these locations there are K batches of tensors of data tensors of shape
    ``(B,) + X + Y_k`` where ``Y_k`` is the shape of each data tensor of the k-th batch and k goes
    from 1 to K. For each batch item and for each input batch including ``bt_scores``, the function
    extracts the data item at the max-location. Then it groups data items of the same type into an
    output batch of tensors, resulting a list containing ``b_maxScores`` of shape ``(B,)`` followed
    by tensors of shape ``(B,) + Y_k`` for k goes from 1 to K.

    Parameters
    ----------
    bt_scores : array_like
        a tensor of scores of shape shape ``(B,) + X `` and dtype float32. The tensor can be a
        numpy array or a tensorflow tensor.
    *args : tuple
        a tuple of tensors of data tensors of shape ``(B,) + X + Y_k`` and dtype float32. Each
        tensor has the same type as `bt_scores`. No checking is implemented.

    Returns
    -------
    b_maxScores : array_like
        a batch of scalars representing the maximum scores. It has the same type as `bt_scores` but
        with shape ``(B,)``.
    *args : tuple
        each item is a batch of shape ``(B,) + Y_k`` corresponding to the max-location items of the
        corresponding input batch of shape ``(B,) + X + Y_k``
    """

    if base.is_ndarray(bt_scores):
        shape = bt_scores.shape
        ndim = len(shape)
        B = shape[0]
        X = shape[1:]
        pX = np.prod(X)
        bv_scores = bt_scores.reshape((B, pX))
        b_indices = np.argmax(bv_scores, axis=1)
        b_maxScores = np.take(bv_scores, b_indices, axis=1)
        l_outputs = [b_maxScores]

        for bt_data in args:
            Y = bt_data.shape[ndim:]
            bv_data = bt_data.reshape((B, pX) + Y)
            b_maxData = np.take(bv_data, b_indices, axis=1)
            l_outputs.append(b_maxData)
    elif base.is_tftensor(bt_scores):
        from mt import tf

        shape = tf.shape(bt_scores)
        ndim = tf.rank(bt_scores)
        B = shape[:1]
        X = shape[1:]
        pX = [tf.math.reduce_prod(X)]
        bv_scores = tf.reshape(bt_scores, tf.concat([B, pX], 0))
        b_indices = tf.math.argmax(bv_scores, axis=1)
        b_maxScores = tf.gather(bv_scores, b_indices, axis=1, batch_dims=1)
        l_outputs = [b_maxScores]

        for bt_data in args:
            Y = tf.shape(bt_data)[ndim:]
            bv_data = tf.reshape(bt_data, tf.concat([B, pX, Y], 0))
            b_maxData = tf.gather(bv_data, b_indices, axis=1, batch_dims=1)
            l_outputs.append(b_maxData)
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    if len(l_outputs) == 1:
        return l_outputs[0]
    return tuple(l_outputs)
