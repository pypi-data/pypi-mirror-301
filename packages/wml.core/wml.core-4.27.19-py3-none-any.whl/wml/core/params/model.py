"""Abstract classes representing parameters.
"""

from mt.tfc import ModelParams

from ..tensor_names import TensorNames


class BaseModelParams(ModelParams):
    yaml_tag = "!BaseModelParams"

    """Parameters for defining and creating a model.

    This is an abstract class for all Winnow models. Compared to its abstract superclass, it
    requires the user to further implement :func:`get_tensor_names` to return all input and
    outpred tensor names of the model.

    Parameters
    ----------
    gen : int
        model generation/family number, starting from 1
    """

    def __init__(self, gen: int = 1):
        super().__init__(gen=gen)

    def get_tensor_names(self) -> TensorNames:
        """Gets a TensorNames instance containing the input and outpred tensor names."""
        raise NotImplementedError
