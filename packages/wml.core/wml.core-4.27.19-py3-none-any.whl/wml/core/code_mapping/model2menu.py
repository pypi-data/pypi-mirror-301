"""Menu-scoped and menuversion-scoped mappings from model codes to menu codes.
"""

import multiprocessing
from tqdm.auto import tqdm
import scipy.sparse as ss

from mt import tp, np, pd, logg

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


def func_s2m(menux_id: int):
    return func_s2m.m2s._s2m(func_s2m.l_modelCodes, menux_id)


class Model2MenuxCodeMappings(CodeMappingsPrim):
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

    def _s2m(self, l_modelCodes, menux_id):
        l_menuCodes = self.dl_menuCodes[menux_id]
        l_primCodes = self.dl_primCodes[menux_id]
        dl_primCodes = self.ddl_primCodes[menux_id]

        # dd_s2w
        d_s2t = self.project_disjoint(l_modelCodes, l_primCodes, disable_logging=True)
        dd_s2w = {t: {} for t in l_primCodes}
        for model_code, l_pPrimCodes in d_s2t.items():
            if len(l_pPrimCodes) == 0:
                continue
            w = 1.0 / len(l_pPrimCodes)
            for primary_code in l_pPrimCodes:
                d = dd_s2w[primary_code]
                d[model_code] = d.get(model_code, 0) + w

        # aggregates
        dd_pModelCodes = {}
        for menu_code in l_menuCodes:
            d = {}
            for primary_code in dl_primCodes[menu_code]:
                for model_code, w in dd_s2w[primary_code].items():
                    d[model_code] = d.get(model_code, 0) + w
            dd_pModelCodes[menu_code] = d

        return (menux_id, dd_pModelCodes)

    def project_s2m(
        self, l_modelCodes: tp.List[str], in_parallel: bool = False
    ) -> pd.DataFrame:
        """Projects every model code to the list of primary codes of every menux.

        For every menux, first :func:`project_disjoint` is used to project every model code
        to the primary codes with weights. Then, all the model codes of all the primary codes of each
        menu code are summed up.

        Parameters
        ----------
        l_modelCodes : dict
            list of disjoint model codes to be projected to every list of primary codes. No checking
            is conducted to ensure the model codes are disjoint.
        in_parallel : bool
            whether to run the main for loop in parallel using multiprocessing or not

        Returns
        -------
        s2m_df : pandas.DataFrame
            a dataframe of 4 columns ``[menux, 'menu_code', 'model_code', 'weight']``
            telling for each menux and each menu code, which model codes maps to it and with
            what weight. The dataframe is sorted in the ascending order of columns
            `[menux, 'menu_code', 'model_code']`.
        """

        d = self.dl_menuCodes
        if in_parallel:
            initargs = (func_s2m, self, l_modelCodes)
            pool = multiprocessing.Pool(initializer=init_worker, initargs=initargs)
            generator = pool.map(func_s2m, d)
        else:
            func_s2m.m2s = self
            func_s2m.l_modelCodes = l_modelCodes
            generator = map(func_s2m, d)
        generator = tqdm(generator, total=len(d), desc="model2menux")

        data = []
        for menux_id, dd_pModelCodes in generator:
            for menu_code, d_pModelCodes in dd_pModelCodes.items():
                for model_code, weight in d_pModelCodes.items():
                    data.append((menux_id, menu_code, model_code, weight))

        columns = [self.menux, "menu_code", "model_code", "weight"]
        df = pd.DataFrame(columns=columns, data=data)
        return df.sort_values([self.menux, "menu_code", "model_code"])


def compute_model2menux_matrices(
    df: pd.DataFrame,
    l_modelCodes: list,
    with_menuversion: bool = True,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> tp.Dict[int, np.ndarray]:
    """Computes all model-to-menux transition matrices from a dataframe.

    The transition matrix of a menux is a J-row K-columns matrix where K is the number of model
    codes and J is the number of menu codes. The codes are in the same order as provided in input
    arguments. The idea is that for a given full softmax vector in model space, one just has to
    left-multiply the softmax vector with the transition matrix, to get a raw softmax vector in the
    menux space. This softmax vector needs not have sum of components to 1. One can just assign
    'menu_score' to that sum and then normalise the menu softmax vector.

    We use :class:`scipy.sparse.coo_array` to store each sparse transition matrix.

    Parameters
    ----------
    df : pandas.DataFrame
        the model2menux dataframe containing the
        ``(menux_id, model_code, weight) -> (menux_id, menu_code)`` mappings. It has 4 columns
        ``['menux_id', 'model_code', 'menu_code', 'weight']``. The dataframe can be obtained by
        invoking function `project_s2m` of some code mapping classes.
    l_modelCodes : list
        list of global model codes, likely obtained from a model
    with_menuversion : bool
        whether menux means menuversion (True) or menu (False)
    logger : mt.logg.IndentedLoggerAdapter, optional
        logger for debugging purposes

    Returns
    -------
    dm_transitions : dict
        a ``{menux_id: scipy.sparse.coo_array}`` dictionary
    dl_menuCodes : dict
        a ``{menux_id: list_of_menu_codes}`` dictionary containing all the
       ``(menux_id, menu_code)`` pairs
    """

    menux = "menu_version_id" if with_menuversion else "menu_id"

    # detect model codes not available in the global taxcode list
    l_dfModelCodes = df["model_code"].drop_duplicates().tolist()
    l_outlierModelCodes = set(l_dfModelCodes) - set(l_modelCodes)
    if len(l_outlierModelCodes):
        msg = f"Ignored {len(l_outlierModelCodes)} model codes non-existent in the global taxcode list."
        logg.warn(msg, logger=logger)
        logg.warn(l_outlierModelCodes, logger=logger)
        df = df[df["model_code"].isin(l_modelCodes)]

    # go through each menux
    dm_transitions = {}
    dl_menuCodes = {}
    l_menuXIds = df[menux].drop_duplicates().tolist()
    K = len(l_modelCodes)
    for menux_id in tqdm(l_menuXIds, total=len(l_menuXIds), unit=menux):
        df1 = df[df[menux] == menux_id]
        l_menuCodes = df1["menu_code"].drop_duplicates().tolist()
        J = len(l_menuCodes)
        data = []
        row = []
        col = []

        # go through each row
        for _, r in df1.iterrows():
            row.append(l_menuCodes.index(r["menu_code"]))
            col.append(l_modelCodes.index(r["model_code"]))
            data.append(r["weight"])

        dm_transitions[menux_id] = ss.coo_array((data, (row, col)), shape=(J, K))
        dl_menuCodes[menux_id] = l_menuCodes

    return dm_transitions, dl_menuCodes
