"""Model operating mode (opmode).

Winnow's food recognition models, since 2022/06/01, have been having the ability to operate at
different modes. There is always a neutral opmode where the output predicted taxcode distribution
is not explicitly modified. The user can specify additionally a number of new opmodes N. Each new
opmode introduces a modification to the output predicted distribution.

Up until 2022/08/10, the naming convention was that, given value N, opmode 0 to opmode N-1 were
defined as additional opmodes while opmode N was defined as the neutral opmode.

Since 2022/08/11, a new naming convention is introduced, only to :class:`Predctx2OpmodeMapper`,
in which opmode 0 is reserved for the neutral opmode while all non-neutral opmodes are indexed from
1. The user can specify this convention at the point of instantiating the class.

Technically, the way the modification works is that the opmode is transformed into N-dim one-hot
vectors with the exception that opmode N is transformed into the N-dim zero vector. Then, the
vector is concatenated to the total feature vector before the final Dense layer. Each component of
the one-hot vector connects to a column in the Dense layer's weight matrix, that represents the
bias logit vector to be applied to the output predicted distribution.

Winnow's client region ids and prediction contexts are then mapped to different opmodes. How to map
is application-specific. But the general idea is as the followings:

    - If N is 1 and it is a MuNet model always map to opmode 0, the single non-neutral opmode.
    - For events coming from clients or client regions or categories that have not formed a
      critical mass, assign to the neutral opmodes.
    - For events coming from a category that has formed a critical mass, assign a non-neutral
      opmode.
"""

import abc
import re
import json

from mt import tp, pd


class OpmodeMapperInterface(metaclass=abc.ABCMeta):
    """A mapper interface that maps any object to an opmode.

    Classes of this interface must implement three functions, :func:`n_opmodes` which returns the
    number of additional opmodes, :func:`neutral_opmode` which returns the index of the neutral
    opmode, and :func:`__call__` which takes as input an object and returns the corresponding
    opmode or raises a ValueError if the conversion is not successful.

    As of 2022/12/21, it has been required that there be a property called 'predctx_key' containing
    the field name representing the prediction context. It can have value None to assert that there
    is no corresponding field.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "n_opmodes")
            and callable(subclass.n_opmodes)
            and hasattr(subclass, "neutral_opmode")
            and callable(subclass.neutral_opmode)
            and hasattr(subclass, "__call__")
            and callable(subclass.__call__)
        )

    @abc.abstractmethod
    def n_opmodes(self) -> int:
        """Gets the number of additional opmodes."""
        raise NotImplementedError

    @abc.abstractmethod
    def neutral_opmode(self) -> int:
        """Gets the index of the neutral opmode."""
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, obj) -> int:
        """Finds the corresponding opmode of an object, raising ValueError if not found."""
        raise NotImplementedError


class NullOpmodeMapper(OpmodeMapperInterface):
    """A null mapper having only the neutral opmode."""

    predctx_key = None

    def n_opmodes(self) -> int:
        return 0

    n_opmodes.__doc__ = OpmodeMapperInterface.n_opmodes.__doc__

    def neutral_opmode(self) -> int:
        return 0

    neutral_opmode.__doc__ = OpmodeMapperInterface.neutral_opmode.__doc__

    def __call__(self, obj) -> int:
        return 0

    __call__.__doc__ = OpmodeMapperInterface.__call__.__doc__


class Crid2OpmodeMapper(OpmodeMapperInterface):
    """A mapper converting client region ids into opmodes.

    Parameters
    ----------
    l_crids : list
        list of all valid client region ids
    silent : bool
        whether (default) or not to silently convert to the neutral opmode upon encountering an
        invalid client region id
    """

    predctx_key = "client_region_id"

    def __init__(self, l_crids: list, silent: bool = True):
        self.l_crids = sorted(list(set(l_crids)))
        self.silent = silent

    def n_opmodes(self) -> int:
        return len(self.l_crids)

    n_opmodes.__doc__ = OpmodeMapperInterface.n_opmodes.__doc__

    def neutral_opmode(self) -> int:
        return self.n_opmodes()

    neutral_opmode.__doc__ = OpmodeMapperInterface.neutral_opmode.__doc__

    def __call__(self, obj) -> int:
        try:
            return self.l_crids.index(obj)
        except ValueError:
            if self.silent:
                return self.neutral_opmode()
            raise

    __call__.__doc__ = OpmodeMapperInterface.__call__.__doc__

    @classmethod
    def from_json(cls, json_obj):
        """Constructs a Crid2OpmodeMapper instance from an exported json object."""
        l_crids = json_obj["l_crids"]
        silent = json_obj["silent"]
        return Crid2OpmodeMapper(l_crids, silent=silent)

    def to_json(self) -> dict:
        """Exports the instance to a json object."""
        return {"l_crids": self.l_crids, "silent": self.silent}


def unique_gpc(gpc: tp.Union[str, dict]) -> str:
    """Makes a string, which represents a prediction context, compact and unique.

    Parameters
    ----------
    gpc : str or dict
        a dict or its JSON-compliant string representing a prediction context

    Returns
    -------
    str
        an output JSON-compliant string representing the same prediction context, but with every
        key having null value removed, and with the keys being sorted.
    """
    x = gpc if isinstance(gpc, dict) else json.loads(gpc)
    keys = sorted(list(x.keys()))
    x = {k: x[k] for k in keys if x[k] is not None}
    return json.dumps(x)


class Predctx2OpmodeMapper(OpmodeMapperInterface):
    """A mapper converting prediction contexts and installation contexts into opmodes.

    As of 2022/06/22, after discussing with the data team and the engineering team, the following
    agreements had been made:

      - An installation context is a JSON-compliant string containing a dictionary of (key,value)
        pairs. All keys and values are strings. All keys must be present.
      - A prediction context is a partial from of an installation context where some keys are
        omitetd, or their values are null, asseting the key is not used. An installation context A
        is said to belong to a prediction context B if for every key of B that has non-null value,
        A has the same key and `B[key] == A[key]`.

    As of 2022/08/09, prediction contexts and groupings can be dictionaries.

    The user provides a list of prediction context. For a given query installation context or a
    given query prediction context, the class would go through the list one-by-one until it finds
    a match. Otherwise a ValueError is raised.

    Parameters
    ----------
    l_gpcs : list
        list of prediction contexts, each item for one non-neutral opmode
    silent : bool
        whether (default) or not to silently convert to the neutral opmode upon encountering an
        invalid client region id or an invalid prediction context
    neutral_first : bool
        If True, the value of the neutral opmode is 0. Otherwise (default), the value is
        the number of opmodes.

    Notes
    -----
    The actual number of opmodes maybe lower than `len(l_gpcs)` if there are null elements or
    duplicate gpcs in `l_gpcs`.
    """

    predctx_key = "prediction_context"

    def __init__(self, l_gpcs: list, silent: bool = True, neutral_first: bool = False):
        l_gpcs = sorted([unique_gpc(x) for x in l_gpcs if isinstance(x, (str, dict))])
        self.l_gpcs = [json.loads(x) for x in l_gpcs]
        self.silent = silent
        if neutral_first:
            raise NotImplementedError

    def n_opmodes(self) -> int:
        return len(self.l_gpcs)

    n_opmodes.__doc__ = OpmodeMapperInterface.n_opmodes.__doc__

    def neutral_opmode(self) -> int:
        return self.n_opmodes()

    neutral_opmode.__doc__ = OpmodeMapperInterface.neutral_opmode.__doc__

    def __call__(self, obj) -> int:
        if pd.isnull(obj):  # neutral case
            return self.neutral_opmode()

        if isinstance(obj, dict):
            query_dict = obj
        else:
            try:
                query_dict = json.loads(obj)
            except json.decoder.JSONDecodeError:
                if self.silent:
                    return self.neutral_opmode()
                else:
                    raise ValueError(f"Object is not json-compatible: {obj}.")
            if not isinstance(query_dict, dict):
                raise ValueError(
                    "Input is not a JSON-compliant string representing a dictionary. "
                    "Got: '{}'".format(obj)
                )

        for i, gpc in enumerate(self.l_gpcs):
            ok = True
            for k in gpc:
                if query_dict.get(k, None) != gpc[k]:
                    ok = False
                    break
            if ok:  # found a match
                return i

        # no match found
        if self.silent:
            return self.neutral_opmode()

        raise ValueError("No opmode found for '{}'".format(obj))

    __call__.__doc__ = OpmodeMapperInterface.__call__.__doc__

    @classmethod
    def from_json(cls, json_obj):
        """Constructs a Predctx2OpmodeMapper instance from an exported json object."""
        return Predctx2OpmodeMapper(json_obj["l_gpcs"], silent=json_obj["silent"])

    def to_json(self) -> dict:
        """Exports the instance to a json object."""
        return {"silent": self.silent, "l_gpcs": [json.dumps(x) for x in self.l_gpcs]}
