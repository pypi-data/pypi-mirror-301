"""Base module for mapping codes"""

from mt import tp, np, pd, logg

from ..datatype.taxtree import (
    load_taxtree,
    check_disjoint,
    merge2base_taxtree_df,
    merge2sealed_taxtree_df,
)


class TaxtreeLoader:
    """A base class that just loads a taxtree.

    Parameters
    ----------
    taxtree_df : pandas.DataFrame
        The taxtree dataframe containing columns ``['code', 'parent_code']``. There must be no
        cycle among the code relationships. There are 3 cases: A, B and C. In case A, the dataframe
        is downloaded from ML DB and the parent code of each root code must be null. In case B and
        C, there is no row where the parent code is null. The root codes are defined to be those
        in the 'code' field but not in the 'parent_code' field. The difference between B and C is
        that B is for base term codes only and C can contain codes with facets.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Attributes
    ----------
    taxtree : wml.core.datatype.taxtree.Taxtree
        the taxonomy tree augmented with the global menu codes
    taxtree_df : pandas.DataFrame
        dataframe with  columns ``['taxcode', 'parent_taxcode']`` containing nodes on the taxonomy
        tree
    """

    def __init__(
        self,
        taxtree_df: pd.DataFrame,
        logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
    ):
        self.logger = logger
        self.load_taxtree(taxtree_df)

    def load_taxtree(self, taxtree_df: pd.DataFrame):
        """Loads a taxtree from a taxtree dataframe."""
        s = taxtree_df["parent_code"].isna()
        if s.sum() > 0:  # case A
            is_sealed = True
            msg = "Taxtree dataframe from ML DB detected."
            logg.info(msg, logger=self.logger)
            taxtree_df = taxtree_df[["code", "parent_code"]].copy()
        else:  # case B and C
            # determine which merge function depending on whether there is a 'X1234/' kind of code
            is_sealed = False
            for code in taxtree_df["code"]:
                if code.endswith("/"):
                    is_sealed = True
                    break
            if is_sealed:
                msg = f"Sealed taxtree dataframe with {len(taxtree_df)} rows detected."
                logg.info(msg, logger=self.logger)
                merge_func = merge2sealed_taxtree_df
            else:
                msg = f"Base taxtree dataframe with {len(taxtree_df)} rows detected."
                logg.info(msg, logger=self.logger)
                merge_func = merge2base_taxtree_df

            # merge the menu codes to the taxtree dataframe
            taxtree_df, root_code = merge_func(
                taxtree_df, self.l_menuCodes, logger=self.logger
            )

            # merge the root code to the taxtree dataframe
            df = pd.DataFrame(columns=["code", "parent_code"], data=[(root_code, None)])
            taxtree_df = pd.concat([taxtree_df, df])

        # make the tree
        taxtree_df.columns = ["taxcode", "parent_taxcode"]
        self.taxtree_df = taxtree_df
        self.taxtree = load_taxtree(self.taxtree_df)

    def disjoint(
        self,
        l_codes: tp.List[str],
        post_check: bool = False,
    ) -> tp.List[str]:
        """Disjoints a list of codes so that every pair of codes is disjoint.

        Parameters
        ----------
        l_codes : list
            list of input codes. Each code must live in the tree.
        post_check : bool
            check if the output list is indeed disjoint or not

        Returns
        -------
        l_disjointCodes : dict
            the output sorted list of disjoint codes
        """

        l_disjointCodes = sorted(self.taxtree.minimum_disjoint_set(l_codes))
        if post_check:
            check_disjoint(l_disjointCodes, self.taxtree, logger=self.logger)
        return l_disjointCodes

    def project(self, code: str, l_disjointCodes: tp.List[str]) -> tp.List[str]:
        """Projects a code to a list of disjoint codes.

        Parameters
        ----------
        code : str
            an input code to project. It must live in the tree.
        l_disjointCodes : dict
            list of disjoint codes where the input code is projected to. No checking is conducted
            to ensure the codes are disjoint.

        Returns
        -------
        l_projectedCodes : list
            a subset of `l_disjointCodes` representing the list of projected codes
        """

        # upward projection
        for disjoint_code in l_disjointCodes:
            if self.taxtree.covered_by(code, disjoint_code):
                return [disjoint_code]

        # downward projection
        l_projectedCodes = []
        for disjoint_code in l_disjointCodes:
            if self.taxtree.covers(code, disjoint_code):
                l_projectedCodes.append(disjoint_code)
        return l_projectedCodes


# Definition:
#
#   - menu code: the taxcode associated with a menu item that lives in the taxonomy tree. Winnow
#     is currently restricted to maximum one taxcode per menu item.


class CodeMappingsBase(TaxtreeLoader):
    """Mappings between model codes and menu codes, base class.

    Each scope can be either a (menu, version) pair or a menu. Menux is a general term. If,
    `with_menuversion` is True, it means (menu, version) pair. Otherwise, it means menu.

    Parameters
    ----------
    taxtree_df : pandas.DataFrame
        The taxtree dataframe containing columns ``['code', 'parent_code']``. There must be no
        cycle among the code relationships. There are 3 cases: A, B and C. In case A, the dataframe
        is downloaded from ML DB and the parent code of each root code must be null. In case B and
        C, there is no row where the parent code is null. The root codes are defined to be those
        in the 'code' field but not in the 'parent_code' field. The difference between B and C is
        that B is for base term codes only and C can contain codes with facets.
    menuCode_df : pandas.DataFrame
        The dataframe of menu codes consisting of 2 columns ``[menux, 'menu_code']``.
        If a menu code appears in multiple menux ids, items from that menu code can be used
        in all those menuxes.
    with_menuversion : bool
        If True, the scope is (menu, version) pair. Otherwise the scope is menu only.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    There are new attributes as follows in addition to the attributes of :class:`TaxtreeLoader`.

    Attributes
    ----------
    l_menuxIds : list
        the global list of menux ids in the ascending order
    l_menuCodes : list
        the global list of menu codes in the ascending order
    dl_menuCodes : dict
        a dictionary mapping each menux id to a list of menu codes
    """

    def __init__(
        self,
        taxtree_df: pd.DataFrame,
        menuCode_df: pd.DataFrame,
        with_menuversion: bool = True,
        logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
    ):
        super().__init__(taxtree_df, logger=logger)

        if with_menuversion:
            self.with_menuversion = True
            self.menux = "menu_version_id"
        else:
            self.with_menuversion = False
            self.menux = "menu_id"

        menuCode_df[self.menux] = menuCode_df[self.menux].astype(int)
        self.l_menuxIds = sorted(menuCode_df[self.menux].drop_duplicates().tolist())

        # menu codes
        self.dl_menuCodes = {}
        for menux_id in self.l_menuxIds:
            df2 = menuCode_df[menuCode_df[self.menux] == menux_id]
            l_menuCodes = sorted(df2["menu_code"].drop_duplicates().tolist())
            self.dl_menuCodes[menux_id] = l_menuCodes
        self.l_menuCodes = sorted(menuCode_df["menu_code"].drop_duplicates().tolist())
