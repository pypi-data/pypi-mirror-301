"""Menu-scoped and menuversion-scoped mappings from menu codes to model codes.
"""

import multiprocessing
from tqdm.auto import tqdm

from mt import tp, pd, logg

from .prim import CodeMappingsPrim


# Definition:
#
#   - menu code: the taxcode associated with a menu item that lives in the taxonomy tree. Winnow
#     is currently restricted to maximum one taxcode per menu item.
#   - primary code: an element the disjoint set of all menu codes of a given menu. The disjoint
#     operation is conducted with respect to the most current taxonomy tree
#
# As of 2023/09/15, after an intensive discussion between Marc, Phong and Minhtri, it has been
# agreed that for a menu code which has a descendant menu code in the same menu (i.e. a vulnerable
# menu code), it is interpreted that the ground truth is the whole branch of the ancestor menu code
# EXCLUDING every subbranch of every descendant menu code.
#
# The foreseeable consequence as of 2023/09/15 was that all Aquarium codes with a vulnerable
# ancestor menu code need cleaning. And all events with a vulnerable menu code need cleaning.


def init_worker(function, m2s, l_modelCodes):
    function.m2s = m2s
    function.l_modelCodes = l_modelCodes


def func_m2s(menux_id: int):
    return func_m2s.m2s._m2s(func_m2s.l_modelCodes, menux_id)


class Menux2ModelCodeMappings(CodeMappingsPrim):
    """Mappings between menu(-version) codes and model codes.

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
            taxtree_df,
            menuCode_df,
            missing_codes=missing_codes,
            with_menuversion=with_menuversion,
            logger=logger,
        )

    def _m2s(self, l_modelCodes, menux_id):
        l_menuCodes = self.dl_menuCodes[menux_id]
        l_primCodes = self.dl_primCodes[menux_id]
        dl_primCodes = self.ddl_primCodes[menux_id]

        d_t2s = self.project_disjoint(l_primCodes, l_modelCodes, disable_logging=True)

        # aggregate
        ddl_pModelCodes = {}
        for menu_code in l_menuCodes:
            l_primCodes = dl_primCodes[menu_code]
            ddl_pModelCodes[menu_code] = {t: d_t2s[t] for t in l_primCodes}

        return (menux_id, ddl_pModelCodes)

    def project_m2s(
        self, l_modelCodes: tp.List[str], in_parallel: bool = False
    ) -> pd.DataFrame:
        """Projects every menu code of every menux to a list of disjoint model codes.

        For every menux, first :func:`project_disjoint` is used to project every primary code
        to the model codes. Then, all the model codes of all the primary codes of each menu code
        can be constructed by taking the union of all model code sets across all primary codes.

        Parameters
        ----------
        l_modelCodes : dict
            list of disjoint model codes where the primary codes are projected to. No checking is
            conducted to ensure the model codes are disjoint.
        in_parallel : bool
            whether to run the main for loop in parallel using multiprocessing or not

        Returns
        -------
        m2s_df : pandas.DataFrame
            a sorted dataframe of 4 columns
            ``[menux, 'menu_code', 'primary_code', 'model_codes']``
            telling for each menux and each menu code and each primary code, which model
            codes it maps to
        """

        d = self.dl_menuCodes
        if in_parallel:
            pool = multiprocessing.Pool(
                initializer=init_worker, initargs=(func_m2s, self, l_modelCodes)
            )
            generator = pool.map(func_m2s, d)
        else:
            func_m2s.m2s = self
            func_m2s.l_modelCodes = l_modelCodes
            generator = map(func_m2s, d)
        generator = tqdm(generator, total=len(d), desc="menux2model")

        data = []
        for menux_id, ddl_pModelCodes in generator:
            for menu_code, dl_pModelCodes in ddl_pModelCodes.items():
                for primary_code, l_pModelCodes in dl_pModelCodes.items():
                    data.append((menux_id, menu_code, primary_code, l_pModelCodes))

        columns = [self.menux, "menu_code", "primary_code", "model_codes"]
        df = pd.DataFrame(columns=columns, data=data)
        return df.sort_values([self.menux, "menu_code", "primary_code"])
