from mt.base import LogicError
from mt import tp, pd, logg

from ..taxcode import valid_taxcode
from ..dag import DAG


class Taxtree:
    """A growing taxonomy tree

    Notes
    -----
    It is guaranteed that children ids are greater than parent id for all nodes.
    """

    def __init__(self):
        self._nodes = {}
        self._root_node = None

    @property
    def size(self):
        return len(self._nodes)

    @property
    def root_node(self):
        if self._root_node is None:
            for code in self._nodes.keys():
                if self._nodes[code]["parent"] is None:
                    self._root_node = code
                    break
        return self._root_node

    def exists(self, taxcode):
        return taxcode in self._nodes

    def insert(self, taxcode, parent_taxcode=None):
        if parent_taxcode != None:
            if not self.exists(parent_taxcode):
                raise LogicError(
                    "Parent node does not exist.",
                    debug={"parent_taxcode": parent_taxcode, "taxcode": taxcode},
                )
            self._nodes[parent_taxcode]["children"].append(taxcode)
        if taxcode not in self._nodes:
            self._nodes[taxcode] = {"children": [], "parent": None}
        self._nodes[taxcode]["parent"] = parent_taxcode

    def parent_of(self, taxcode):
        return self._nodes[taxcode]["parent"]

    def children_of(self, taxcode):
        return self._nodes[taxcode]["children"]

    def is_leaf(self, taxcode):
        return len(self.children_of(taxcode)) == 0

    def is_root(self, taxcode):
        return self.parent_of(taxcode) is None

    def trace_to_root(self, taxcode: str) -> tp.Generator[str, None, None]:
        """A generator that returns the trace from the taxcode to the root node."""

        parent = self._nodes[taxcode]["parent"]
        yield taxcode
        if parent is not None:
            yield from self.trace_to_root(parent)

    def trace_from_root(self, taxcode: str) -> tp.Generator[str, None, None]:
        """A generator that returns the trace from the root node to the taxcode."""

        parent = self._nodes[taxcode]["parent"]
        if parent is not None:
            yield from self.trace_from_root(parent)
        yield taxcode

    def least_common_ancestor(self, code_a, code_b):
        if code_a == code_b:
            return code_a
        trace_a = list(self.trace_from_root(code_a))
        for i, b in enumerate(self.trace_from_root(code_b)):
            if i >= len(trace_a) or trace_a[i] != b:
                return trace_a[i - 1]
        return b

    def disjoint_process(self, taxcode, codeset):
        for code in codeset:
            node = self.least_common_ancestor(taxcode, code)
            if node == taxcode:
                for node in self.find_relatives(taxcode, code):
                    self.disjoint_process(node, codeset)
                return
            elif node == code:
                for i, node in enumerate(codeset):
                    if node == code:
                        codeset[i] = taxcode
                        break
                codeset.extend(self.find_relatives(code, taxcode))
                return
        codeset.append(taxcode)

    def disjoint(self, taxcodes):
        l_disjoint = []
        for code in taxcodes:
            self.disjoint_process(code, l_disjoint)
        return l_disjoint

    def minimum_disjoint_set(
        self,
        l_taxcodes: tp.List[str],
        if_not_exists: str = "raise",
    ) -> tp.Generator[str, None, None]:
        """A generator that finds the minimum disjoint set of a list of taxcodes.

        Parameters
        ----------
        l_taxcodes : list
            list of taxcodes to compute the minimum disjoint set from
        if_not_exists : {'ignore', 'raise'}
            whether to ignore or raise a LogicError if a taxcode of the input list does not exist
            in the tree

        Yields
        ------
        str
            returning taxcode of the tree that forms the minimum disjoint set
        """

        # build the coreset
        coreset = set()
        for taxcode in l_taxcodes:
            if not self.exists(taxcode):
                if if_not_exists == "ignore":
                    continue
                raise LogicError(
                    "A taxcode of the input list does not exist in the tree.",
                    debug={"taxcode": taxcode},
                )
            for code in self.trace_to_root(taxcode):
                if code in coreset:
                    break
                coreset.add(code)

        # find the minimum disjoint set, which is all the leaf nodes of the coreset when the
        # coreset is viewed as a subtree, and every non-coreset child of every coreset node
        for code in coreset:
            # determine if we need to expand this code or not
            for child_code in self.children_of(code):
                if child_code in coreset:  # yes we do
                    # visit children again to avoid creating temporary variables
                    yield from (x for x in self.children_of(code) if x not in coreset)
                    break
            else:  # no we don't
                yield code

    def find_relatives(self, ancestor: str, descendant: str):
        """A generator that recursively explodes the ancestor to a minimal set of nodes that contains the descendant.

        The descendant itself is excluded from the returning set.
        """

        if ancestor == descendant:
            return []
        parent_of_descendant = self._nodes[descendant]["parent"]
        yield from self.find_relatives(ancestor, parent_of_descendant)
        for child in self._nodes[parent_of_descendant]["children"]:
            if child == descendant:
                continue
            yield child

    def minimum_cover_set(self, coreset):
        current_set = {self.root_node}
        for taxcode in coreset:
            if taxcode in current_set:
                continue
            path = []
            pointer = taxcode
            while pointer not in current_set:
                parent = self._nodes[pointer]["parent"]
                if parent is None:
                    path = []
                    break
                path.append(parent)
                pointer = parent

            for node in path:
                current_set.discard(node)
                for child in self._nodes[node]["children"]:
                    current_set.add(child)

        return list(current_set)

    def separated(self, code_a, code_b):
        code_c = self.least_common_ancestor(code_a, code_b)
        return code_c != code_a and code_c != code_b

    def covers(self, code_a, code_b):
        for code in self.trace_to_root(code_b):
            if code == code_a:
                return True
        return False

    def covered_by(self, code_a, code_b):
        for code in self.trace_to_root(code_a):
            if code == code_b:
                return True
        return False

    def covered_elems(self, taxcode, leaf_only=False):
        out = []
        queue = [taxcode]

        while queue:
            node = queue.pop()
            if not leaf_only or not self._nodes[node]["children"]:
                out.append(node)
            if self._nodes[node]["children"]:
                queue += self._nodes[node]["children"]
        return out

    # ----- serialization -----

    def as_dag(self) -> DAG:
        dag = DAG()

        def insert(node: str):
            l_children = self.children_of(node)
            dag.expand_leaf(node, l_children)
            for child_node in l_children:
                insert(child_node)

        node = self.root_node()
        dag.add_root(node)
        insert(node)

        return dag


def load_taxtree(df: pd.DataFrame, logger=None) -> Taxtree:
    """Loads the taxtree from a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        The taxtree dataframe containing columns `['taxcode', 'parent_taxcode']`. There must be a
        single root taxcode whose parent taxcode is null. Every other row must have a valid
        parent taxcode.
    logger: logging.Logger or None
        logger for debugging

    Returns
    -------
    retval : Taxtree
        the generated taxtree
    """

    # Initialize the taxtree.
    taxtree = Taxtree()

    # Create a queue to store the nodes to be processed.
    queue = []

    # For each row in the dataframe,
    for index, row in df.iterrows():
        # Get the taxcode and parent taxcode of the row.
        taxcode = row["taxcode"]
        parent_taxcode = row["parent_taxcode"]

        if not valid_taxcode(taxcode):
            logg.info(row, logger=logger)
            raise LogicError("Invalid taxcode", debug={"taxcode": taxcode})

        # If the parent taxcode is null, then the node is the root node.
        if pd.isnull(parent_taxcode):
            taxtree.insert(taxcode)
        else:
            # If the parent node does not exist, then add it to the queue.
            if not valid_taxcode(parent_taxcode):
                raise LogicError(
                    "Invalid parent taxcode", debug={"parent_taxcode": parent_taxcode}
                )

            if not taxtree.exists(parent_taxcode):
                queue.append((taxcode, parent_taxcode))
            else:
                # Insert the node into the taxtree.
                taxtree.insert(taxcode, parent_taxcode)

    # While the queue is not empty,
    while queue:
        # Pop the front node from the queue.
        taxcode, parent_taxcode = queue.pop(0)

        if taxtree.exists(parent_taxcode):
            taxtree.insert(taxcode, parent_taxcode)
        else:
            queue.append((taxcode, parent_taxcode))

    # Return the taxtree.
    return taxtree
