"""Module dealing with tensor names of a training session."""

from mt import tp


class TensorNames:
    """A class to encapsulate all tensor names of a training session.

    In the context of wml training, in each training session, there are 4 kinds of tensor names:

      1. Names corresponding to tensors provided to the model as input, called input names.
      2. Names corresponding to model output tensors, called outpred names.
      3. Names corresponding to true output tensors, called outtrue names.
      4. Names corresponding to other tensors not used by the model, called control names.

    When dealing with TF losses and metrics, we need to feed outpred tensors and outtrue tensors to
    the losses and metrics for computation. However, since Keras has some strict conditions on the
    outpred and outtrue tensors, we need an ability to exclude some output tensors.

    Parameters
    ----------
    l_inputNames : list
        list of input tensor names, in the same order as that of the model's input list
    l_outpredNames : list
        list of outpred tensor names, in the same order as that of the model's output list
    l_outtrueNames : list
        list of outtrue tensor names, if any
    l_controlNames : list
        list of control tensor names, if any
    l_tfExcludedOutpredNames : list
        a subset of `l_outpredNames` containing outpred tensors to be excluded when computing TF
        losses and metrics
    l_tfExcludedOuttrueNames : list
        a subset of `l_outtrueNames` containing outtrue tensors to be excluded when computing TF
        losses and metrics
    """

    def __init__(
        self,
        l_inputNames: list = [],
        l_outpredNames: list = [],
        l_outtrueNames: list = [],
        l_controlNames: list = [],
        l_tfExcludedOutpredNames: list = [],
        l_tfExcludedOuttrueNames: list = [],
    ):
        self.l_inputNames = l_inputNames
        self.l_outpredNames = l_outpredNames
        self.l_outtrueNames = l_outtrueNames
        self.l_controlNames = l_controlNames
        self.l_tfExcludedOutpredNames = l_tfExcludedOutpredNames
        self.l_tfExcludedOuttrueNames = l_tfExcludedOuttrueNames
