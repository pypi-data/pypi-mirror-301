"""Functions dealing with an attribute list.

An attribute list in our context is an ordered list of attributes, each of which is represented by a fixed-size list of [name, values, weight]. The reason for using a fixed-size list instead of a tuple is so that the attribute list can be serialized using yaml without introducing python tuple. Item `name` represents the name of an attributes. Item `values` is a ordered list of strings containing all the valid values for that name. Item `weight` tells how the attributes are important compared to one another.

Given an attribute list, an attribute value array is a tuple of attribute values. Each value corresponds to an attribute in the attribute list. An attribute index array is the attribute value array encoded into 0-based indices. An attribute onehot array is the attribute encoded into onehot vectors and then concatenated into a single vector.
"""

import numpy as _np


__all__ = [
    "count",
    "attr_count",
    "ndim",
    "names",
    "values2indices",
    "values2onehots",
    "indices2onehots",
    "indices2values",
    "onehots2values",
    "onehots2indices",
]


def count(attr_list):
    """Returns the number of attributes defined in the attribute list."""
    return len(attr_list)


def attr_count(index, attr_list):
    """Returns the number of attribute values for a given attribute.

    Parameters
    ----------
    index : int
        the index of the attribute in the attribute list
    attr_list : list
        the input attribute list

    Returns
    -------
    int
        the number of values associated with the attribute
    """
    return len(attr_list[index][1])


def ndim(attr_list):
    """Counts up the total number of attribute values across all attributes.

    Parameters
    ----------
    attr_list : list
        an attribute list

    Returns
    -------
    int
        sum of the number of classes of all problems
    """
    return sum((len(x[1]) for x in attr_list))


def names(attr_list):
    """Extracts all attribute names from the attribute list.

    Parameters
    ----------
    attr_list : list
        an attribute list

    Returns
    -------
    list
        list of all problem names
    """
    return [x[0] for x in attr_list]


def values2indices(attr_values, attr_list):
    """Converts an attribute value array to an attribute index array.

    Parameters
    ----------
    attr_values : iterable
        an attribute value array
    attr_list : list
        an attribute list

    Returns
    -------
    numpy.ndarray
        a 1D numpy array of int32 representing the attribute indices
    """
    arr = []
    for i in range(len(attr_list)):
        name, values, weight = attr_list[i]
        index = values.index(attr_values[i])
        if index < 0:
            raise ValueError(
                "Unexpected attribute value '{}' in tuple '{}'".format(
                    attr_values[i], attr_values
                )
            )
        arr.append(index)
    return _np.array(arr)


def values2onehots(attr_values, attr_list):
    """Converts an attribute value array to an attribute onehot array.

    Parameters
    ----------
    attr_values : iterable
        an attribute value array
    attr_list : list
        an attribute list

    Returns
    -------
    numpy.ndarray
        a 1D numpy array of floats representing the attribute indices in concatenated onehot format
    """
    arr = _np.zeros(ndim(attr_list))
    ofs = 0
    for i in range(len(attr_list)):
        name, values, weight = attr_list[i]
        index = values.index(attr_values[i])
        if index < 0:
            raise ValueError(
                "Unexpected attribute value '{}' in tuple '{}'".format(
                    attr_values[i], attr_values
                )
            )
        arr[ofs + index] = 1
        ofs += len(values)
    return arr


def indices2onehots(attr_indices, attr_list):
    """Converts an attribute index array to an attribute onehot array.

    Parameters
    ----------
    attr_indices : iterable
        an interable of attribute indices, each index for one attribute of the attribute list, respectively
    attr_list : list
        an attribute list

    Returns
    -------
    numpy.ndarray
        a 1D numpy array of floats representing the attribute indices in concatenated onehot format
    """
    arr = _np.zeros(ndim(attr_list))
    ofs = 0
    for i in range(len(attr_list)):
        attr_cnt = attr_count(i, attr_list)
        index = attr_indices[i]
        if index < 0 or index >= attr_cnt:
            raise ValueError(
                "Unexpected attribute index '({},{})' in tuple '{}'".format(
                    i, index, attr_indices
                )
            )
        arr[ofs + index] = 1
        ofs += attr_cnt
    return arr


def indices2values(attr_indices, attr_list):
    """Converts an attribute index array to an attribute value array.

    Parameters
    ----------
    attr_indices : iterable
        an interable of attribute indices, each index for one attribute of the attribute list, respectively
    attr_list : list
        an attribute list

    Returns
    -------
    tuple
        the output attribute value array
    """
    arr = [attr[1][index] for index, attr in zip(attr_indices, attr_list)]
    return tuple(arr)


def onehots2values(attr_onehots, attr_list):
    """Converts an attribute onehot array to an attribute onehot array.

    Parameters
    ----------
    attr_onehots : numpy.ndarray
        a 1D array of at least `ndim(attr_list)` floats, representing an attribute onehot array, or a concatenated softmax/logit array whose components align with any attribute onehot array associated with the given attribute list
    attr_list : list
        an attribute list

    Returns
    -------
    tuple
        the output attribute value array
    """
    attr_onehots = attr_onehots.ravel()
    arr = []
    ofs = 0
    for i in range(len(attr_list)):
        attr_cnt = attr_count(i, attr_list)
        arr.append(attr_list[i][1][_np.argmax(attr_onehots[ofs : ofs + attr_cnt])])
        ofs += attr_cnt
    return tuple(arr)


def onehots2indices(attr_onehots, attr_list):
    """Converts an attribute onehot array to an attribute index array.

    Parameters
    ----------
    attr_onehots : numpy.ndarray
        a 1D array of at least `ndim(attr_list)` floats, representing an attribute onehot array, or a concatenated softmax/logit array whose components align with any attribute onehot array associated with the given attribute list
    attr_list : list
        an attribute list

    Returns
    -------
    numpy.ndarray
        a 1D numpy array of int32 representing the attribute indices
    """
    attr_onehots = attr_onehots.ravel()
    arr = []
    ofs = 0
    for i in range(len(attr_list)):
        attr_cnt = attr_count(i, attr_list)
        arr.append(_np.argmax(attr_onehots[ofs : ofs + attr_cnt]))
        ofs += attr_cnt
    return _nd.array(arr)


def get_numerics():
    from mt import net

    a = _np.array(net.get_numerics())
    b = a[[7, 9, 1, 3, 5]]
    c = _np.concatenate([b, a[[0, 2, 4, 6, 8, 10]]], axis=0)
    return b, c
