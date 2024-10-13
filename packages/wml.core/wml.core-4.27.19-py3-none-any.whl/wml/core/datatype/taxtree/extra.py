"""Extra functions about a taxtree."""

from mt import tp, np, pd, logg

from .base import Taxtree


class LeafsetMapper:
    """Given a taxtree, mapping each set of tree nodes to a set of leaf taxcodes as a bool ndarray.

    Parameters
    ----------
    tt : Taxtree
        an input taxtree

    Attributes
    ----------
    N : int
        number of tree taxcodes
    M : int
        number of leaf taxcodes
    l_taxcodes : list
        a sorted list of leaf taxcodes
    df : pandas.DataFrame
        a dataframe with columns ['taxcode', 'leaf_set']. Each row represents a taxcode of the tree
        and its associated set of leaf taxcodes as a bool ndarray.
    """

    def __init__(self, tt: Taxtree):
        self.N = tt.nbElems()  # number of taxcodes

        # construct the taxcode list and make the map that goes from tree idx to list idx of each leaf
        l_leaves = []
        for i in range(self.N):
            if tt.isLeaf(i):
                l_leaves.append((tt.taxcode(i), i))
        l_leaves = sorted(l_leaves, key=lambda x: x[0])
        self.l_taxcodes = [x[0].decode() for x in l_leaves]
        mapLeaf_tree2list = {x[1]: i for i, x in enumerate(l_leaves)}
        self.M = len(l_leaves)  # number of leaf taxcodes

        # make the dataframe
        l_arrays = [None] * self.N

        def visit(i: int) -> np.ndarray:
            if l_arrays[i] is not None:
                return l_arrays[i]
            if tt.isLeaf(i):
                arr = np.eye(1, self.M, mapLeaf_tree2list[i], dtype=np.bool)[0]
            else:
                arr = np.zeros(self.M, dtype=np.bool)
                for j in tt.children(i):
                    arr |= visit(j)
            l_arrays[i] = arr
            return arr

        data = []
        for i in range(self.N):
            data.append((tt.taxcode(i).decode(), visit(i)))
        self.df = pd.DataFrame(columns=["taxcode", "leaf_set"], data=data)

    def compute_leafset(self, x) -> np.ndarray:
        """Maps a taxcodeset into an bool ndarray representing the set of leaf taxcodes.

        Parameters
        ----------
        x : str or list
            a valid tree taxcode or a valid taxcodeset where all the taxcodes exist in the tree

        Returns
        -------
        numpy.ndarray
            a bool ndarray representing the set of leaf taxcodes. See also :attr:`l_taxcodes`.
        """

        if isinstance(x, str):  # turn it into a list
            if "[" in x:
                import json

                x = json.loads(x)
            else:
                x = [x]
        elif not isinstance(x, list):
            raise ValueError(
                "Only a list or a str is accepted. Got type '{}'.".format(type(x))
            )

        df = self.df[self.df["taxcode"].isin(x)]
        if len(df) == 0:
            return np.zeros(self.M, dtype=np.bool)

        if len(df) == 1:
            return df["leaf_set"].iloc[0]

        union_arr = np.zeros(self.M, dtype=np.bool)
        for _, arr in df["leaf_set"].iteritems():
            union_arr |= arr

        return union_arr


def check_disjoint(l_codes: tp.List[str], taxtree: Taxtree, logger=None):
    """Checks if a list of code is disjoint."""

    if logger:
        logger.info("Checking a disjoint list.")

    if len(l_codes) != len(set(l_codes)):
        raise LogicError(
            "Duplicate items found on the list of disjoint codes.",
            debug={"l_codes": l_codes},
        )

    for i, code in enumerate(l_codes):
        for j in range(i):
            code2 = l_codes[j]
            if not taxtree.separated(code, code2):
                msg = "Found an undirected ancestor-descendant pair."
                raise LogicError(msg, debug={"code": code, "code2": code2})


def merge2base_taxtree_df(
    base_taxtree_df: pd.DataFrame,
    l_menuCodes: tp.List[str],
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Merges a list of menu codes to a taxtree dataframe of base terms.

    Parameters
    ----------
    base_taxtree_df : pandas.DataFrame
        The input taxtree dataframe containing columns ``['code', 'parent_code']``. There must be
        no cycle among the code relationships. All codes must be base terms only and must have
        exactly 5 alphanumeric letters.
    l_menuCodes : list
        list of menu codes to be merged from
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    sealed_taxtree_df : pandas.DataFrame
        The output taxtree dataframe containing columns ``['code', 'parent_code']``. Menu codes
        are assigned as children of their base terms. Each base term 'X1234' also comes with a
        child called 'X1234/' to represent all other children.
    root_code : str
        the root code
    """

    # clean up a bit
    columns = ["code", "parent_code"]
    base_taxtree_df = base_taxtree_df[columns].drop_duplicates().copy()

    # find the root codes
    set1 = set(base_taxtree_df["parent_code"].tolist())
    set2 = set(base_taxtree_df["code"].tolist())
    l_rootCodes = sorted(list(set1 - set2))
    l_baseCodes = sorted(list(set1 | set2))

    if len(l_rootCodes) == 0:
        raise LogicError("No root code detected.")
    if len(l_rootCodes) > 1:
        raise LogicError(
            f"Multiple root codes detected.", debug={"l_rootCodes": l_rootCodes}
        )
    root_code = l_rootCodes[0]

    # add all the base codes with slash
    data = [(base_code + "/", base_code) for base_code in l_baseCodes]

    # add all the menu codes
    l_newMenuCodes = []
    l_newBaseCodes = []
    for menu_code in l_menuCodes:
        if menu_code in l_baseCodes:
            l_newMenuCodes.append(menu_code)
            continue
        parent_code = menu_code[:5]
        if parent_code not in l_baseCodes:
            if parent_code not in l_newBaseCodes:
                l_newBaseCodes.append(parent_code)
        if menu_code != parent_code:
            data.append((menu_code, parent_code))
        l_newMenuCodes.append(menu_code)

    n_newBaseCodes = len(l_newBaseCodes)
    if n_newBaseCodes > 0:
        msg = f"Added new {n_newBaseCodes} baseterms to root code {root_code}."
        logg.warn(msg, logger=logger)
        for base_code in l_newBaseCodes:
            data.append((base_code, root_code))
            data.append((base_code + "/", base_code))

    # make a new dataframe
    df = pd.DataFrame(columns=columns, data=data)
    sealed_taxtree_df = (
        pd.concat([base_taxtree_df, df]).sort_values(columns).reset_index(drop=True)
    )

    return sealed_taxtree_df, root_code


def merge2sealed_taxtree_df(
    sealed_taxtree_df: pd.DataFrame,
    l_menuCodes: tp.List[str],
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Merges a list of menu codes to a sealed taxtree dataframe.

    Parameters
    ----------
    sealed_taxtree_df : pandas.DataFrame
        The input taxtree dataframe containing columns ``['code', 'parent_code']``. It must be
        an output dataframe by invoking :func:`merge2base_taxtree_df`.
    l_menuCodes : list
        list of menu codes to be merged from
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    unsealed_taxtree_df : pandas.DataFrame
        The output taxtree dataframe containing columns ``['code', 'parent_code']``. For each menu
        code 'X1234BLABLAH`, its base term `X1234` is compared against the dataframe. If the base
        term does not exist, the menu code is not merged. If the the base term does exist, the menu
        code is assigned as a child of the 'X1234/' code.
    root_code : str
        the root code
    """

    # clean up a bit
    columns = ["code", "parent_code"]
    sealed_taxtree_df = sealed_taxtree_df[columns].drop_duplicates().copy()

    # build a list of all full codes
    l_fullCodes = sealed_taxtree_df["code"].tolist()
    l_fullCodes += sealed_taxtree_df["parent_code"].tolist()
    l_fullCodes = set(l_fullCodes)

    # find the root codes
    df = sealed_taxtree_df[sealed_taxtree_df["code"].str.len() == 5]
    l_parentCodes = df["parent_code"].drop_duplicates().tolist()
    l_codes = df["code"].drop_duplicates().tolist()
    set1 = set([x[:5] for x in l_parentCodes])
    set2 = set([x[:5] for x in l_codes])
    l_rootCodes = sorted(set1 - set2)
    l_baseCodes = sorted(set1 | set2)

    if len(l_rootCodes) == 0:
        raise LogicError("No root code detected.")
    if len(l_rootCodes) > 1:
        raise LogicError(
            f"Multiple root codes detected.", debug={"l_rootCodes": l_rootCodes}
        )
    root_code = l_rootCodes[0]

    # add all the menu codes
    l_newBaseCodes = []
    data = []
    for menu_code in l_menuCodes:
        if menu_code in l_fullCodes:
            continue
        parent_code = menu_code[:5]
        if parent_code not in l_baseCodes:
            if parent_code not in l_newBaseCodes:
                l_newBaseCodes.append(parent_code)
        if len(menu_code) > 5:
            data.append((menu_code, parent_code + "/"))

    n_newBaseCodes = len(l_newBaseCodes)
    if n_newBaseCodes > 0:
        msg = f"Added new {n_newBaseCodes} baseterms to root code {root_code}."
        logg.warn(msg, logger=logger)
        for base_code in l_newBaseCodes:
            data.append((base_code, root_code))
            data.append((base_code + "/", base_code))

    # make a new dataframe
    df = pd.DataFrame(columns=columns, data=data)
    unsealed_taxtree_df = (
        pd.concat([sealed_taxtree_df, df]).sort_values(columns).reset_index(drop=True)
    )

    return unsealed_taxtree_df, root_code
