"""A DAG is a directed acyclic graph of visual codes."""


import networkx as nx
import scipy.sparse as ss
from mt import tp, np, pd, logg
from mt.base import LogicError

from .min_heap import MinHeap


class DAG:
    """A directed acyclic graph of visual codes.

    In this structure, we maintain a directed graph with no loop and a set of atomic visual codes.
    """

    def __init__(self):
        self.g = nx.DiGraph()
        self.s_atomicCodes = set()
        self.topo_valid = False  # whether i2v and v2i are valid
        self.i2v = None  # topo id to visual code
        self.v2i = None  # visual code to topo id

    def make_topo_order(self):
        if self.topo_valid:
            return
        self.v2i = {}
        self.i2v = {}
        for i, v in enumerate(nx.topological_sort(self.g)):
            self.v2i[v] = i
            self.i2v[i] = v
        self.topo_valid = True

    def add_root(self, root_code: str) -> None:
        """Adds a root code to the DAG, forming a new component."""
        self.g.add_node(root_code)
        self.s_atomicCodes.add(root_code)
        self.topo_valid = False

    def expand_atomic(
        self, parent_code: str, l_children: tp.List[str], check: bool = True
    ) -> None:
        """Turns a atomic visual code into a parent of new (sub-)atomic codes."""
        if check:
            if parent_code not in self.s_atomicCodes:
                raise LogicError(
                    "Parent code is not an atomic visual code in the DAG.",
                    debug={"parent_code": parent_code, "l_children": l_children},
                )
            for code in l_children:
                if self.g.has_node(code):
                    raise LogicError(
                        "Child code already exists in the DAG.",
                        debug={
                            "child_code": code,
                            "parent_code": parent_code,
                            "l_children": l_children,
                        },
                    )
        for code in l_children:
            self.g.add_node(code)
            self.g.add_edge(parent_code, code)
        self.s_atomicCodes.discard(parent_code)
        self.s_atomicCodes.update(l_children)
        self.topo_valid = False

    def add_new_parent(
        self, parent_code: str, l_children: tp.List[str], check: bool = True
    ) -> None:
        """Adds a new parent code to the DAG."""
        if check:
            if self.g.has_node(parent_code):
                raise LogicError(
                    "Parent code already exists in the DAG.",
                    debug={"parent_code": parent_code, "l_children": l_children},
                )
            for code in l_children:
                if not self.g.has_node(code):
                    raise LogicError(
                        "Child code does not exist in the DAG.",
                        debug={
                            "child_code": code,
                            "parent_code": parent_code,
                            "l_children": l_children,
                        },
                    )
        self.g.add_node(parent_code)
        for code in l_children:
            self.g.add_edge(parent_code, code)
        self.topo_valid = False

    def merge_from(
        self,
        other: "DAG",
        conflict: str = "raise",
        logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
    ) -> "DAG":
        """Merges data from another DAG to the current DAG.

        The merge strategy is to expand the existing atomic visual codes first, and then add new
        parent codes.

        Parameters
        ----------
        other : wml.core.datatype.DAG
            the other DAG to merge from
        conflict : {'raise', 'warn', 'skip'}
            the strategy for resolving conflicts. 'raise' is to raise an exception. 'warn' is to
            write a warning message. 'skip' is to just skip without saying anything.
        logger : mt.logg.IndentedLoggerAdapter, optional
            logger for debugging
        """

        def expand_atomic(parent_code: str):
            if parent_code not in self.s_atomicCodes:
                return
            l_children = list(other.g.succ[parent_code].keys())
            for code in l_children:
                if self.g.has_node(code):
                    if conflict == "raise":
                        raise LogicError(
                            "Child code already exists in the DAG.",
                            debug={
                                "child_code": code,
                                "parent_code": parent_code,
                                "l_children": l_children,
                            },
                        )
                    if conflict == "warn":
                        msg = f"Skipped expanding atomic '{parent_code}' as a child code exists in the DAG."
                        logg.warn(msg, logger=logger)
                    return
            self.expand_atomic(parent_code, l_children, check=False)
            for code in l_children:
                expand_atomic(code)

        # expand each atomic branch
        l_candidates = other.g.nodes & self.s_atomicCodes
        for code in l_candidates:
            expand_atomic(code)

        def add_new_parent(parent_code: str):
            if self.g.has_node(parent_code):
                return
            l_children = list(other.g.succ[parent_code].keys())
            for code in l_children:
                if not self.g.has_node(code):
                    if conflict == "raise":
                        raise LogicError(
                            "Child code does not exist in the DAG.",
                            debug={
                                "child_code": code,
                                "parent_code": parent_code,
                                "l_children": l_children,
                            },
                        )
                    if conflict == "warn":
                        msg = f"Child code '{code}' of parent code '{parent_code}' does not exist in the DAG."
                        logg.warn(msg, logger=logger)
                    return
            self.add_new_parent(parent_code, l_children, check=False)
            l_grandParents = list(other.g.pred[parent_code].keys())
            for grand_parent_code in l_grandParents:
                add_new_parent(grand_parent_code)

        # add new parents
        l_candidates = other.g.nodes - self.g.nodes
        for code in l_candidates:
            add_new_parent(code)

        self.topo_valid = False

        return self

    def traverse_upward(self, code: str):
        """A generator that traverses upward all ancestors of a code in the inverse topological order."""

        self.make_topo_order()
        heap = MinHeap(self.g.number_of_nodes())
        i = self.v2i[code]
        heap.insert(-i)
        i += 1

        while heap.size > 0:
            j = -heap.pop()
            if j >= i:
                continue
            code = self.i2v[j]
            yield code
            i = j
            for parent_code, _ in self.g.in_edges(code):
                j = self.v2i[parent_code]
                heap.insert(-j)

    def traverse_downward(self, code: str):
        """A generator that traverses downward all descendants of a code in the topological order."""

        self.make_topo_order()
        heap = MinHeap(self.g.number_of_nodes())
        i = self.v2i[code]
        heap.insert(i)
        i -= 1

        while heap.size > 0:
            j = heap.pop()
            if j <= i:
                continue
            code = self.i2v[j]
            yield code
            i = j
            for _, child_code in self.g.out_edges(code):
                j = self.v2i[child_code]
                heap.insert(j)

    def find_conflicts(self, l_codes: tp.List[str]) -> tp.List[tp.Tuple[str, str, str]]:
        """Finds non-exhaustively pairs from a given list of codes that share a common descendant.

        The main purpose of the function is to make sure that for a given menu, all the visual
        codes associated with the menu items are mutually exclusive.

        Parameters
        ----------
        l_codes : list
            list of input codes

        Returns
        -------
        list
            list of output pairs of codes sharing a common descendant. The list is non-exhaustive.
            But the method will find at least one pair if such pair exists. Each returning pair is
            a tuple (first_code, second_code, common_code)."""

        l_res = []

        self.make_topo_order()

        # initialise a min heap and a dictionary
        i2x = {}
        heap = MinHeap(self.g.number_of_nodes())
        for v in l_codes:
            if v not in self.v2i:
                continue
            i = self.v2i[v]

            if i in i2x:
                l_res.append((v, i2x[i], v))
                continue

            i2x[i] = v
            heap.insert(i)

        # repeat popping and expanding items from the heap until there's nothing left
        while heap.size > 0:
            i = heap.pop()
            v = self.i2v[i]
            x = i2x[i]
            for _, y in self.g.edges(v):
                j = self.v2i[y]
                if j in i2x:
                    if i2x[j] != x:
                        l_res.append((x, i2x[j], y))
                    continue
                i2x[j] = x
                heap.insert(j)

        return l_res

    @staticmethod
    def build(df: pd.DataFrame) -> "DAG":
        """Builds a DAG from a dataframe.

        The dataframe must contain 2 columns 'code' and 'parent_code'. All atomic visual codes must
        be declared as `(code, parent_code) = (None, something)`. Only parent codes of the
        dataframe are used as codes of the dag.

        Parameters
        ----------
        df : pandas.DataFrame
            the input dataframe, described above

        Returns
        -------
        DAG
            the constructed dag

        Raises
        ------
        mt.base.LogicError
            for any exception caused when constructing the dag
        """

        dag = DAG()

        # remove all rows without a parent code
        df = df[df["parent_code"].notna()]

        # get all atomic visual codes
        s = df["code"].isna()
        df2 = df[s]
        l_processedCodes = df2["parent_code"].drop_duplicates().tolist()
        for code in l_processedCodes:
            dag.add_root(code)
        df = df[~s]

        while len(df) > 0:
            # find candidate parent codes
            l_candidateParentCodes = df["parent_code"].drop_duplicates().tolist()
            s = df["code"].isin(l_processedCodes)
            l_nonCandidateParentCodes = df[~s]["parent_code"].drop_duplicates().tolist()
            l_candidateParentCodes = list(
                set(l_candidateParentCodes) - set(l_nonCandidateParentCodes)
            )

            if not l_candidateParentCodes:
                raise LogicError(
                    "Loop detected building a DAG from a dataframe.",
                    debug={
                        "df": df,
                        "l_nonCandidateParentCodes": l_nonCandidateParentCodes,
                    },
                )

            # go through each candidate parent code
            for parent_code in l_candidateParentCodes:
                df2 = df[df["parent_code"] == parent_code]
                l_children = df2["code"].drop_duplicates().tolist()
                dag.add_new_parent(parent_code, l_children, check=False)

            # paperwork
            df = df[~df["parent_code"].isin(l_candidateParentCodes)]
            l_processedCodes.extend(l_candidateParentCodes)

        return dag

    def get_atomic_visual_codes(self):
        """Returns the list of atomic visual codes."""
        return list(self.s_atomicCodes)

    def make_upward_transition_matrix(
        self,
        l_dstCodes: tp.List[str],
        l_srcCodes: tp.Optional[tp.List[str]] = None,
        upward_policy: tp.Literal["first", "all"] = "first",
    ) -> ss.coo_array:
        """Makes a score transition matrix from one list of codes to another.

        Transitions only happen upward in the dag (using in_edges). The user is responsible to
        finding a way to transit downward, which is non-trivial.

        Parameters
        ----------
        l_dstCodes : list
            the list of target visual codes to transit to. Usually the list represents a list of
            menu-restricted visual codes.
        l_srcCodes : list, optional
            the list of source visual codes to transit from. Usually the list represents a list of
            model codes. If None is provided, the list of atomic visual codes is used.
        upward_policy : {'first', 'all'}
            policy to project the scores upward in the dag (using in_edges). 'first' means the
            ancestor target code with highest topological id will receive coeff 1.0. 'all' means
            all ancestor target codes will receive coeff 1.0.

        Returns
        -------
        scipy.sparse.coo_array
            the output sparse matrix with M rows and N columns where M is the number of target
            visual codes and N is the number of source visual codes. The orders on the lists are
            preserved.
        """

        if l_srcCodes is None:
            l_srcCodes = self.get_atomic_visual_codes()

        d_dstCodes = {code: i for i, code in enumerate(l_dstCodes)}
        l_rows = []
        l_cols = []

        for i, code in enumerate(l_srcCodes):
            for upward_code in self.traverse_upward(code):
                if upward_code not in d_dstCodes:
                    continue
                j = d_dstCodes[upward_code]
                l_cols.append(i)
                l_rows.append(j)
                if upward_policy == "first":
                    break

        n = len(l_rows)
        shape = (len(l_dstCodes), len(l_srcCodes))
        a = ss.coo_array((np.ones(n), (l_rows, l_cols)), shape=shape)
        return a

    def make_downward_transition_matrix_to_atomic(
        self,
        l_srcCodes: tp.List[str],
        downward_policy: tp.Literal["first", "distributed"] = "distributed",
    ) -> ss.coo_array:
        """Makes a score transition matrix from one list of codes to the list of atomic visual codes.

        Transitions only happen downward in the dag (using out_edges).

        Parameters
        ----------
        l_srcCodes : list
            the list of source visual codes to transit from. Usually the list represents a list of
            model codes.
        downward_policy : {'first', 'distributed'}
            policy to project the scores downward in the dag (using out_edges) to the atomic visual
            codes. 'first' means the descendant atomic visual code with the highest topological id
            will receive coeff 1. 'distributed' means the scores are distributed evenly among all
            descendant atomic visual codes.

        Returns
        -------
        scipy.sparse.coo_array
            the output sparse matrix with M rows and N columns where M is the number of atomic
            visual codes and N is the number of source visual codes. The orders on the lists are
            preserved.
        """

        l_dstCodes = self.get_atomic_visual_codes()
        d_dstCodes = {code: i for i, code in enumerate(l_dstCodes)}
        l_rows = []
        l_cols = []
        l_data = []

        for i, code in enumerate(l_srcCodes):
            l_rows2 = []
            l_cols2 = []
            for downward_code in self.traverse_downward(code):
                if downward_code not in d_dstCodes:
                    continue
                j = d_dstCodes[downward_code]
                l_cols2.append(i)
                l_rows2.append(j)
                if downward_policy == "first":
                    break
            n = len(l_rows2)
            l_rows.extend(l_rows2)
            l_cols.extend(l_cols2)
            l_data.extend((1.0 / n,) * n)

        shape = (len(l_dstCodes), len(l_srcCodes))
        a = ss.coo_array((l_data, (l_rows, l_cols)), shape=shape)
        return a

    def make_transition_matrix(
        self,
        l_dstCodes: tp.List[str],
        l_srcCodes: tp.Optional[tp.List[str]],
        upward_policy: tp.Literal["first", "all"] = "first",
        downward_policy: tp.Literal["first", "distributed"] = "distributed",
    ) -> ss.coo_array:
        """Makes a score transition matrix from one list of codes to another.

        Transitions mostly happen upward in the dag (using in_edges). If there is a target visual
        code that is non-atomic, then the transition becomes 2 steps: first downward to atomic
        visual codes given the downward policy, then upward to the target visual codes using the
        upward policy.

        Parameters
        ----------
        l_dstCodes : list
            the list of target visual codes to transit to. Usually the list represents a list of
            menu-restricted visual codes.
        l_srcCodes : list, optional
            the list of source visual codes to transit from. Usually the list represents a list of
            model codes. If None is provided, the list of atomic visual codes is used.
        upward_policy : {'first', 'all'}
            policy to project the scores upward in the dag (using in_edges). 'first' means the
            ancestor target code with highest topological id will receive coeff 1.0. 'all' means
            all ancestor target codes will receive coeff 1.0.
        downward_policy : {'first', 'distributed'}
            policy to project the scores downward in the dag (using out_edges) to the atomic visual
            codes. 'first' means the descendant atomic visual code with the highest topological id
            will receive coeff 1. 'distributed' means the scores are distributed evenly among all
            descendant atomic visual codes.

        Returns
        -------
        scipy.sparse.coo_array
            the output sparse matrix with M rows and N columns where M is the number of target
            visual codes and N is the number of source visual codes. The orders on the lists are
            preserved.
        """

        # split l_srcCodes into d_srcCodes1 (atomic) and d_srcCodes2 (non-atomic)
        n = len(l_srcCodes)
        d_srcCodes1 = {}
        d_srcCodes2 = {}
        a = [None] * n
        for i, code in enumerate(l_srcCodes):
            a[i] = code in self.l_atomicCodes
            if a[i]:
                d_srcCodes1[code] = i
            else:
                d_srcCodes2[code] = i

        m1 = self.make_upward_transition_matrix(
            l_dstCodes, l_srcCodes=d_srcCodes1.keys(), upward_policy=upward_policy
        )
        if not d_srcCodes2:
            return m1

        # deal with non-atomic source visual codes
        m2a = self.make_downward_transition_matrix_to_atomic(
            d_srcCodes2.keys(), downward_policy=downward_policy
        )
        m2b = self.make_upward_transition_matrix(
            l_dstCodes, upward_policy=upward_policy
        )
        m2 = m2b @ m2a

        # merge and return the result
        m = ss.csc_array((len(l_dstCodes), n))
        m1 = m1.tocsc()
        m2 = m2.tocsc()
        for i, code in enumerate(l_srcCodes):
            if a[i]:
                j = d_srcCodes1[code]
                m[:, i] = m1[:, j]
            else:
                j = d_srcCodes2[code]
                m[:, i] = m2[:, j]
        return m.tocoo()
