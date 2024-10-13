"""Winnow's prediction context.

A prediction context (CPC) can be one of the following forms:

    - An integer representing a client region id. We call it a full CPC.
    - A dictionary containing the following optional keys 'clientId', 'regionId', and 'countryId'.
      If all 3 keys appear, we call it a full CPC. Otherwise we call it a partial CPC.
"""

import re
import json

from mt import tp, pd


def get_cpc_key(df: pd.DataFrame) -> str:
    """Detects the CPC field in a dataframe."""
    for x in ["client_region_id", "prediction_context"]:
        if x in df.columns:
            return x
    raise ValueError("Unable to detect any CPC field in the dataframe.")


def parse_cpc(cpc: tp.Union[int, str, None]) -> dict:
    """Parses the CPC value into a dictionary."""
    if isinstance(cpc, int):
        return {"client_region_id": cpc}

    if not isinstance(cpc, str):
        return {}

    res = json.loads(cpc)
    res = {k: v for k, v in res.items() if v is not None}
    return res


class CPCIndexer:
    """Indexes either field 'client_region_id' or 'prediction_context' of a dataframe.

    The default agruments represent a null CPCIndexer which has no CPC.

    Parameters
    ----------
    key : str
        CPC field name
    values : list
        list of possible, preferably partial, CPC values, either in string or in integer.
    """

    def __init__(self, key: str = "no_cpc", values: list = []):
        self.key = key
        self.values = sorted(values)  # in alphabetical order
        self.cpc_dicts = [parse_cpc(x) for x in self.values]  # for finding CPCs

    def find(self, full_cpc):
        """Finds the index of the CPC value in the instance that matches with a given full CPC.

        Parameters
        ----------
        full_cpc : int or str
            the input full CPC to match with

        Returns
        -------
        index : int
            index to one of the CPCs in the instance, or -1 if unable to match
        """
        if full_cpc is None:
            return -1

        if isinstance(full_cpc, int):
            try:
                return self.values.index(full_cpc)
            except ValueError:
                return -1

        a_dict = parse_cpc(full_cpc)
        for i, b_dict in enumerate(self.cpc_dicts):
            ok = True
            for k in b_dict:
                if (not k in a_dict) or (a_dict[k] != b_dict[k]):
                    ok = False
                    break
            if ok:
                return i

        return -1  # not found

    @staticmethod
    def from_df(df: pd.DataFrame):
        """Creates a CPCIndexer directly from a dataframe by detecting for the right field."""
        try:
            key = get_cpc_key(df)
            values = df[key].dropna().drop_duplicates().tolist()
            return CPCIndexer(key=key, values=values)
        except ValueError:
            return CPCIndexer()

    def to_json(self) -> dict:
        """Exports the instance to a json object."""
        return {"key": self.key, "values": self.values}

    @staticmethod
    def from_json(json_obj):
        """Constructs a CPCIndexer instance from an exported json object."""
        return CPCIndexer(json_obj["key"], json_obj["values"])

    def n_values(self) -> int:
        """Gets the number of CPC values that can be indexed."""
        return len(self.values)
