"""Menu-scoped and menuversion-scoped mappings between menu codes and slice codes.
"""

import multiprocessing
from functools import partial
from tqdm.auto import tqdm
import scipy.sparse as ss

from mt import tp, np, pd, logg

from ..code_mapping import CodeMappingsPrim


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


def func1(m2s, l_disjointCodes, l_menuCodes):
    dl_projectedCodes = m2s.project_disjoint(
        l_menuCodes, l_disjointCodes, disable_logging=True
    )
    df = pd.Series(dl_projectedCodes).to_frame("slice_codes")
    df.index.name = "menu_code"
    return df.reset_index(drop=False)


def init_worker(function, m2s, l_sliceCodes):
    function.m2s = m2s
    function.l_sliceCodes = l_sliceCodes


def func_m2s(menux_id: int):
    return func_m2s.m2s._m2s(func_m2s.l_sliceCodes, menux_id)


def func_s2m(menux_id: int):
    return func_s2m.m2s._s2m(func_s2m.l_sliceCodes, menux_id)


class Menux2SliceCodeMappings(CodeMappingsPrim):
    """Mappings between menu(-version) codes and slice codes.

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

    def project_menuxes(
        self,
        l_disjointCodes: tp.List[str],
        n_cores: tp.Union[int, bool] = False,
    ) -> tp.Tuple[pd.DataFrame, pd.DataFrame]:
        """Projects every menux's list of menu codes to a list of disjoint codes.

        The projection is done using :func:`project_disjoint` per menux.

        Parameters
        ----------
        l_disjointCodes : dict
            list of disjoint codes where the input code is projected to. No checking is conducted
            to ensure the codes are disjoint.
        n_cores : int or bool
            Run the main for loop in serial if False (default). Otherwise, run it in parallel using
            multiprocessing. True means that the number of cores is automatically decided.
            Otherwise, the given integer is the number of cores.

        Returns
        -------
        menux2slice_df : pandas
            a sorted dataframe of 3 columns ``[menux, 'menu_code', 'slice_codes']``
            telling for each menux and each menu code, which slice codes it maps to
        slice2menux_df : pandas
            a sorted dataframe of 3 columns ``[menux, 'slice_code', 'menu_code']``
            telling for each menux and each slice code, which menu code it maps to
        """

        if n_cores is False:
            data = []
            things = tqdm(
                self.dl_menuCodes.items(),
                total=len(self.dl_menuCodes),
                unit=self.menux,
                desc="menux2slice",
            )
            for menux_id, l_menuCodes in things:
                dl_projectedCodes = self.project_disjoint(
                    l_menuCodes, l_disjointCodes, disable_logging=True
                )
                for menu_code, l_sliceCodes in dl_projectedCodes.items():
                    data.append((menux_id, menu_code, l_sliceCodes))

            menux2slice_df = pd.DataFrame(
                columns=[self.menux, "menu_code", "slice_codes"], data=data
            )
        else:
            s = pd.Series(self.dl_menuCodes)
            func1a = partial(func1, self, l_disjointCodes)
            n_cores = -1 if n_cores is True else int(n_cores)
            msg = "menux2slice in parallel"
            s = pd.series_parallel_apply(
                s, func1a, n_cores=n_cores, logger=self.logger, scoped_msg=msg
            )
            dfs = []
            for menux_id, df in s.items():
                df[self.menux] = menux_id
                dfs.append(df)
            menux2slice_df = pd.concat(dfs)

        columns = [self.menux, "slice_code", "menu_code"]
        slice2menux_df = menux2slice_df.explode("slice_codes").rename(
            columns={"slice_codes": "slice_code"}
        )
        slice2menux_df = (
            slice2menux_df[columns].sort_values(columns).reset_index(drop=True)
        )

        return menux2slice_df, slice2menux_df

    def _m2s(self, l_sliceCodes, menux_id):
        l_menuCodes = self.dl_menuCodes[menux_id]
        l_primCodes = self.dl_primCodes[menux_id]
        dl_primCodes = self.ddl_primCodes[menux_id]

        d_t2s = self.project_disjoint(l_primCodes, l_sliceCodes, disable_logging=True)

        # aggregate
        ddl_pSliceCodes = {}
        for menu_code in l_menuCodes:
            l_primCodes = dl_primCodes[menu_code]
            ddl_pSliceCodes[menu_code] = {t: d_t2s[t] for t in l_primCodes}

        return (menux_id, ddl_pSliceCodes)

    def project_m2s(
        self, l_sliceCodes: tp.List[str], in_parallel: bool = False
    ) -> pd.DataFrame:
        """Projects every menu code of every menux a list of disjoint slice codes.

        For every menux, first :func:`project_disjoint` is used to project every primary code
        to the slice codes. Then, all the slice codes of all the primary codes of each menu code
        can be constructed by taking the union of all slice code sets across all primary codes.

        Parameters
        ----------
        l_sliceCodes : dict
            list of disjoint slice codes where the primary codes are projected to. No checking is
            conducted to ensure the slice codes are disjoint.
        in_parallel : bool
            whether to run the main for loop in parallel using multiprocessing or not

        Returns
        -------
        m2s_df : pandas.DataFrame
            a sorted dataframe of 4 columns
            ``[menux, 'menu_code', 'primary_code', 'slice_codes']``
            telling for each menux and each menu code and each primary code, which slice
            codes it maps to
        """

        d = self.dl_menuCodes
        if in_parallel:
            pool = multiprocessing.Pool(
                initializer=init_worker, initargs=(func_m2s, self, l_sliceCodes)
            )
            generator = pool.map(func_m2s, d)
        else:
            func_m2s.m2s = self
            func_m2s.l_sliceCodes = l_sliceCodes
            generator = map(func_m2s, d)
        generator = tqdm(generator, total=len(d), desc="menux2slice")

        data = []
        for menux_id, ddl_pSliceCodes in generator:
            for menu_code, dl_pSliceCodes in ddl_pSliceCodes.items():
                for primary_code, l_pSliceCodes in dl_pSliceCodes.items():
                    data.append((menux_id, menu_code, primary_code, l_pSliceCodes))

        columns = [self.menux, "menu_code", "primary_code", "slice_codes"]
        df = pd.DataFrame(columns=columns, data=data)
        return df.sort_values([self.menux, "menu_code", "primary_code"])

    def _s2m(self, l_sliceCodes, menux_id):
        l_menuCodes = self.dl_menuCodes[menux_id]
        l_primCodes = self.dl_primCodes[menux_id]
        dl_primCodes = self.ddl_primCodes[menux_id]

        # dd_s2w
        d_s2t = self.project_disjoint(l_sliceCodes, l_primCodes, disable_logging=True)
        dd_s2w = {t: {} for t in l_primCodes}
        for slice_code, l_pPrimCodes in d_s2t.items():
            if len(l_pPrimCodes) == 0:
                continue
            w = 1.0 / len(l_pPrimCodes)
            for primary_code in l_pPrimCodes:
                d = dd_s2w[primary_code]
                d[slice_code] = d.get(slice_code, 0) + w

        # aggregates
        dd_pSliceCodes = {}
        for menu_code in l_menuCodes:
            d = {}
            for primary_code in dl_primCodes[menu_code]:
                for slice_code, w in dd_s2w[primary_code].items():
                    d[slice_code] = d.get(slice_code, 0) + w
            dd_pSliceCodes[menu_code] = d

        return (menux_id, dd_pSliceCodes)

    def project_s2m(
        self, l_sliceCodes: tp.List[str], in_parallel: bool = False
    ) -> pd.DataFrame:
        """Projects every slice code to the list of primary codes of every menux.

        For every menux, first :func:`project_disjoint` is used to project every slice code
        to the primary codes with weights. Then, all the slice codes of all the primary codes of each
        menu code are summed up.

        Parameters
        ----------
        l_sliceCodes : dict
            list of disjoint slice codes to be projected to every list of primary codes. No checking
            is conducted to ensure the slice codes are disjoint.
        in_parallel : bool
            whether to run the main for loop in parallel using multiprocessing or not

        Returns
        -------
        s2m_df : pandas.DataFrame
            a dataframe of 4 columns ``[menux, 'menu_code', 'slice_code', 'weight']``
            telling for each menux and each menu code, which slice codes maps to it and with
            what weight. The dataframe is sorted in the ascending order of columns
            `[menux, 'menu_code', 'slice_code']`.
        """

        d = self.dl_menuCodes
        if in_parallel:
            initargs = (func_s2m, self, l_sliceCodes)
            pool = multiprocessing.Pool(initializer=init_worker, initargs=initargs)
            generator = pool.map(func_s2m, d)
        else:
            func_s2m.m2s = self
            func_s2m.l_sliceCodes = l_sliceCodes
            generator = map(func_s2m, d)
        generator = tqdm(generator, total=len(d), desc="slice2menux")

        data = []
        for menux_id, dd_pSliceCodes in generator:
            for menu_code, d_pSliceCodes in dd_pSliceCodes.items():
                for slice_code, weight in d_pSliceCodes.items():
                    data.append((menux_id, menu_code, slice_code, weight))

        columns = [self.menux, "menu_code", "slice_code", "weight"]
        df = pd.DataFrame(columns=columns, data=data)
        return df.sort_values([self.menux, "menu_code", "slice_code"])


def compute_slice2menux_matrices(
    df: pd.DataFrame,
    l_sliceCodes: list,
    with_menuversion: bool = True,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> tp.Dict[int, np.ndarray]:
    """Computes all slice-to-menux transition matrices from a dataframe.

    The transition matrix of a menux is a J-row K-columns matrix where K is the number of slice
    codes and J is the number of menu codes. The codes are in the same order as provided in input
    arguments. The idea is that for a given full softmax vector in slice space, one just has to
    left-multiply the softmax vector with the transition matrix, to get a raw softmax vector in the
    menux space. This softmax vector needs not have sum of components to 1. One can just assign
    'menu_score' to that sum and then normalise the menu softmax vector.

    We use :class:`scipy.sparse.coo_array` to store each sparse transition matrix.

    Parameters
    ----------
    df : pandas.DataFrame
        the slice2menux dataframe containing the
        ``(menux_id, slice_code, weight) -> (menux_id, menu_code)`` mappings. It has 4 columns
        ``['menux_id', 'slice_code', 'menu_code', 'weight']``.
    l_sliceCodes : list
        list of global slice codes, likely obtained from a model
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

    # detect slice codes not available in the global taxcode list
    l_dfSliceCodes = df["slice_code"].drop_duplicates().tolist()
    l_outlierSliceCodes = set(l_dfSliceCodes) - set(l_sliceCodes)
    if len(l_outlierSliceCodes):
        msg = f"Ignored {len(l_outlierSliceCodes)} slice codes non-existent in the global taxcode list."
        logg.warn(msg, logger=logger)
        logg.warn(l_outlierSliceCodes, logger=logger)
        df = df[df["slice_code"].isin(l_sliceCodes)]

    # go through each menux
    dm_transitions = {}
    dl_menuCodes = {}
    l_menuXIds = df[menux].drop_duplicates().tolist()
    K = len(l_sliceCodes)
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
            col.append(l_sliceCodes.index(r["slice_code"]))
            data.append(r["weight"])

        dm_transitions[menux_id] = ss.coo_array((data, (row, col)), shape=(J, K))
        dl_menuCodes[menux_id] = l_menuCodes

    return dm_transitions, dl_menuCodes
