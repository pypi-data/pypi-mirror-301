# pylint: disable=line-too-long, invalid-name, relative-beyond-top-level

"""Stuff related to mask comparisons."""

from mt import np, base


def mask_stats(bt_trueMasks, bt_predMasks):
    """Computes statistics and metrics when comparing true masks against predicted masks.

    Parameters
    ----------
    bt_trueMasks : array_like
        a batch of tensors of shape `(B, ...)`, dtype float32 with each cell can be either 0.0 or
        1.0, representing true masks.
    bt_predMasks : array_like
        a batch of tensors of the same shape as `bt_trueMasks`, dtype float32 with each cell can be
        either 0.0 or 1.0, representing predicted masks.

    Returns
    -------
    bv_maskStats : array_like
        a tensor of mask statistics, of shape `(B, 9)` and dtype float32 corresponding to the
        statistics of each batch item, that is `(TP, FN, FP, TN, FAR, FRR, precis, recall, iou)`
        containing the numbers of true positives, true negatives, false positives, false negatives,
        the false acceptance rate, the false rejection rate, the precision, the recall and the
        intersection-over-union respectively.
    """

    rank = len(bt_trueMasks.shape)

    bt_TPs = bt_trueMasks * bt_predMasks
    bt_FNs = bt_trueMasks - bt_TPs
    bt_FPs = bt_predMasks - bt_TPs
    bt_TNs = 1.0 - bt_trueMasks - bt_FPs

    if base.is_ndarray(bt_trueMasks):
        l_maskAxes = tuple(range(1, rank))
        b_TPs = np.sum(bt_TPs, axis=l_maskAxes)
        b_FNs = np.sum(bt_FNs, axis=l_maskAxes)
        b_FPs = np.sum(bt_FPs, axis=l_maskAxes)
        b_TNs = np.sum(bt_TNs, axis=l_maskAxes)

        b_FARs = np.divide_no_nan(b_FPs, b_FPs + b_TNs)
        b_FRRs = np.divide_no_nan(b_FNs, b_FNs + b_TPs)
        b_preciss = np.divide_no_nan(b_TPs, b_TPs + b_FPs)
        b_recalls = np.divide_no_nan(b_TPs, b_TPs + b_FNs)
        b_ious = np.divide_no_nan(b_TPs, b_TPs + b_FNs + b_FPs)
        bv_maskStats = np.stack(
            [b_TPs, b_FNs, b_FPs, b_TNs, b_FARs, b_FRRs, b_preciss, b_recalls, b_ious],
            axis=-1,
        )
    elif base.is_tftensor(bt_trueMasks):
        from mt import tf

        l_maskAxes = list(range(1, rank))
        b_TPs = tf.reduce_sum(bt_TPs, axis=l_maskAxes)
        b_FNs = tf.reduce_sum(bt_FNs, axis=l_maskAxes)
        b_FPs = tf.reduce_sum(bt_FPs, axis=l_maskAxes)
        b_TNs = tf.reduce_sum(bt_TNs, axis=l_maskAxes)

        b_FARs = tf.math.divide_no_nan(b_FPs, b_FPs + b_TNs)
        b_FRRs = tf.math.divide_no_nan(b_FNs, b_FNs + b_TPs)
        b_preciss = tf.math.divide_no_nan(b_TPs, b_TPs + b_FPs)
        b_recalls = tf.math.divide_no_nan(b_TPs, b_TPs + b_FNs)
        b_ious = tf.math.divide_no_nan(b_TPs, b_TPs + b_FNs + b_FPs)
        bv_maskStats = tf.stack(
            [b_TPs, b_FNs, b_FPs, b_TNs, b_FARs, b_FRRs, b_preciss, b_recalls, b_ious],
            axis=-1,
        )
    else:
        raise NotImplementedError("Neither an ndarray or a tf tensor was given.")

    return bv_maskStats


mask_stats.names = [
    "TP",
    "FN",
    "FP",
    "TN",
    "FAR",
    "FRR",
    "precis",
    "recall",
    "iou",
]
