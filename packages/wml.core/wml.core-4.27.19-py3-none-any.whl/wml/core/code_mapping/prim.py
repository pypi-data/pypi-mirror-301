"""Module for mapping codes and deriving primary codes for each menu.
"""

from functools import partial
from tqdm.auto import tqdm

from mt.base import LogicError
from mt import tp, np, pd, logg

from .base import CodeMappingsBase


# Definition:
#
#   - menu code: the taxcode associated with a menu item that lives in the taxonomy tree. Winnow
#     is currently restricted to maximum one taxcode per menu item.
#   - primary code: an element the disjoint set of all menu codes of a given menu. The disjoint
#     operation is conducted with respect to the most current taxonomy tree


def make_prim_codes(m2s, missing_codes, row):
    menu_version_id = row.name
    l_menuCodes = row["menu_codes"]
    try:
        l_primCodes = m2s.disjoint(l_menuCodes)
    except LogicError as e:
        if e.args[0] == "A taxcode of the input list does not exist in the tree.":
            raise LogicError(
                "Menu code not found in the taxtree. Maybe run `visionml_recreate_taxtree.py`?",
                debug={
                    "menu_version_id": menu_version_id,
                    "menu_code": e.args[1]["taxcode"],
                },
            )
        else:
            raise
    dl_primCodes = m2s.project_disjoint(
        l_menuCodes, l_primCodes, no_input_below_disjoint=True, disable_logging=True
    )

    return pd.Series(
        name=menu_version_id,
        data={"primary_codes": l_primCodes, "pprimary_codes": dl_primCodes},
    )


class CodeMappingsPrim(CodeMappingsBase):
    """Mappings from model codes to menu(-version) codes.

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
    missing_codes : {'warn', 'raise'}
        policy to deal with codes not living in the tree. 'warn' means to raise a warning message.
        'raise' means to raise a LogicError
    with_menuversion : bool
        If True, the scope is (menu, version) pair. Otherwise the scope is menu only.
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    There are new attributes as follows in addition to the attributes of :class:`CodeMappingsBase`.

    Attributes
    ----------
    dl_primCodes : dict
        a dictionary mapping each menux id to a list of primary codes. A primary code is a
        code on the taxonomy, such that the set of all primary codes of a given menux id is
        disjoint and the set has minimum length.
    ddl_primCodes : dict
        a dictionary of dictionaries mapping each (menux_id, menu_code) pair to a list of
        primary codes.
    """

    def __init__(
        self,
        taxtree_df: pd.DataFrame,
        menuCode_df: pd.DataFrame,
        missing_codes: str = "warn",
        with_menuversion: bool = True,
        logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
    ):
        super().__init__(
            taxtree_df, menuCode_df, with_menuversion=with_menuversion, logger=logger
        )

        # primary codes
        df = pd.Series(self.dl_menuCodes).to_frame("menu_codes")
        df.index.name = self.menux
        func = partial(make_prim_codes, self, missing_codes)
        msg = "Project menuxes"
        df = pd.parallel_apply(df, func, logger=logger, scoped_msg=msg)
        self.dl_primCodes = df["primary_codes"].to_dict()
        self.ddl_primCodes = df["pprimary_codes"].to_dict()

    def project_disjoint(
        self,
        l_codes: tp.List[str],
        l_disjointCodes: tp.List[str],
        no_input_below_disjoint: bool = False,
        disable_logging: bool = False,
    ) -> tp.Dict[str, tp.List[str]]:
        """Projects a list of codes to a list of disjoint codes.

        Each disjoint code is assigned to all input codes which are its descendants, and to the
        closest ancestor input code, if it exists.

        This function is designed to map each primary code to a subset of model codes for training
        purposes. Mapping from from menu codes to model codes will be done by union operations.

        It can also be used to map each model code to a set of primary codes per menu, for testing
        purposes. However, in this case each model-to-prim arrow has a probability equal to
        `1/len(dl_projectedCodes[model_code]`. Mapping from model codes to menu codes will be done
        by a matrix-vector dot product.

        Parameters
        ----------
        l_codes : list
            list of input codes to project. Each code must live in the tree.
        l_disjointCodes : dict
            list of disjoint codes where the input code is projected to. No checking is conducted
            to ensure the codes are disjoint.
        no_input_below_disjoint : bool
            whether or not there is no input code that is strictly a descendant of a disjoint code
        disable_logging : bool
            whether or not to disable the use of self.logger

        Returns
        -------
        dl_projectedCodes : dict
           a dictionary mapping each input code to a subset of `l_disjointCodes`
        """

        logger = None if disable_logging else self.logger

        msg = f"Mapping the {len(l_disjointCodes)} disjoint codes to the {len(l_codes)} input codes"
        with logg.scoped_info(msg, logger=logger):
            dl_projectedCodes = {code: [] for code in l_codes}

            if not no_input_below_disjoint:
                msg = f"Finding every input code that is a descendant of a disjoint code..."
                logg.info(msg, logger=logger)
                s_disjointCodes = set(l_disjointCodes)
                for code in l_codes:
                    if not self.taxtree.exists(code):
                        continue
                    for x in self.taxtree.trace_to_root(code):
                        if x in s_disjointCodes:
                            dl_projectedCodes[code].append(x)
                            break

                msg = f"Finding every disjoint code that is a descendant of a remaining input code..."
                s_codes = set((x for x in l_codes if len(dl_projectedCodes[x]) == 0))
            else:
                msg = f"Finding every disjoint code that is a descendant of an input code..."
                s_codes = set(l_codes)

            logg.info(msg, logger=logger)
            for disjoint_code in l_disjointCodes:
                for x in self.taxtree.trace_to_root(disjoint_code):
                    if x in s_codes:
                        dl_projectedCodes[x].append(disjoint_code)
                        break

        generator = (
            l_codes
            if logger is None
            else tqdm(l_codes, total=len(l_codes), desc="Sorting projected codes")
        )
        for code in generator:
            l_projectedCodes = dl_projectedCodes[code]
            dl_projectedCodes[code] = sorted(l_projectedCodes)

        return dl_projectedCodes
