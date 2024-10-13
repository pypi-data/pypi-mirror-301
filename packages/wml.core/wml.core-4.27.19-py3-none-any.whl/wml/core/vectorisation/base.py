# pylint: disable=line-too-long

"""Some useful functions to vectorise things
"""

from mt import tp, np, pd


__all__ = ["vectorise_periodic"]


def vectorise_periodic(v: tp.Optional[float] = None) -> np.ndarray:
    """Converts a periodic scalar into a 2D vector.

    A periodic scalar is a scalar that is either None, np.nan or in a range [0,1] where `0==1`.
    It is converted into a 2D vector as follows. If it is null, then the output vector is (0,0).
    Otherwise, the output vector is on the unit sphere using the following formula:

        x = cos(v*(pi*2))
        y = sin(v*(pi*2))

    Parameters
    ----------
    x : float, optional
        the periodic scalar

    Returns
    -------
    numpy.ndarray
        a 2-vector
    """

    if pd.isnull(v):
        return np.zeros(2)

    v *= np.pi * 2
    return np.array([np.cos(v), np.sin(v)])
