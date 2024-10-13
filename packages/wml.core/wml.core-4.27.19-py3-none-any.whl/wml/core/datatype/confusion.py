"""Module dealing with confusion matrices."""

import json

from mt import tp, np, pd, logg, base


class ConfusionMatrix:
    """A class encapsulating a confusion matrix.

    A confusion matrix here is defined as a list of J classes and a matrix M associated with it.
    Each class is a set of labels which are strings. Matrix M is JxJ that represents the joint
    distribution 'Pr(true class is i AND predicted class is j)'.

    Note that because a prediction can have classes outside the J classes, we expect the sum of all
    elements of M to be less than or equal to 1. There is an attribute `a_weights` to represent the
    prior weight of each of J true classes. It is virtually untouched here but the user can use it
    to connect to other entities.

    Parameters
    ----------
    ls_labels : list
        a list of non-empty set of labels. Each label is a string. Each set corresponds to one
        class.
    M : numpy.ndarray
        A JxJ matrix where J is the number of classes represnting the joint distribution above
    a_weights : numpy.ndarray
        the prior weight for each of the J true classes
    """

    def __init__(self, ls_labels: list, M: np.ndarray, a_weights: np.ndarray):
        self.ls_labels = ls_labels
        self.J = len(self.ls_labels)

        if M.shape != (self.J, self.J):
            raise ValueError(
                "The list has {J} classes but the matrix shape {Mshape} is "
                "not ({J},{J}).".format(J=self.J, Mshape=M.shape)
            )

        if a_weights.shape != (self.J,):
            raise ValueError(
                "The list has {J} classes but the weight arrays's shape is "
                "not ({J},).".format(J=self.J)
            )

        self.M = M
        self.a_weights = a_weights

    def merge_classes(self, i: int, j: int):
        """Merges two classes into one, removing the latter class.

        Parameters
        ----------
        i : int
            first class
        j : int
            second class

        Returns
        -------
        ConfusionMatrix
            an output confusion matrix where class j is merged into class i
        """

        if i < 0 or i >= self.J:
            raise ValueError(
                "Class i must be an integer in [0, {}). Got: {}.".format(self.J, i)
            )

        if j < 0 or j >= self.J:
            raise ValueError(
                "Class j must be an integer in [0, {}). Got: {}.".format(self.J, j)
            )

        # merge columns
        M = self.M.copy()
        M[:, i] += M[:, j]
        M = np.delete(M, j, axis=1)

        # merge rows
        M[i, :] += M[j, :]
        M = np.delete(M, j, axis=0)

        # merge labels
        ls_labels = self.ls_labels.copy()
        ls_labels[i] |= ls_labels[j]
        ls_labels.pop(j)

        # merge prior weights
        a_weights = self.a_weights.copy()
        a_weights[i] += a_weights[j]
        a_weights = np.delete(a_weights, j, axis=0)

        return ConfusionMatrix(ls_labels, M, a_weights)

    def find_most_confused(self, symmetric: bool = True):
        """Finds a pair (i,j) that has maximum confusion.

        Parameters
        ----------
        symmetric : bool
            If True, return one that `M[i,j] + M[j,i]` is maximised. Otherwise, return one that
            `M[i,j]` is maximised.

        Returns
        -------
        tuple
            tuple (i,j, val) where `i != j` and `val` is the value of confusion
        """

        if self.J <= 1:
            raise SyntaxError(
                "A confusion matrix with 1 class cannot have any confused pair."
            )

        if symmetric:
            M = self.M + self.M.T
        else:
            M = np.triu(self.M)
        np.fill_diagonal(M, 0)

        index = np.argmax(M)
        i = index // self.J
        j = index % self.J

        return (i, j, M[i, j])

    def find_most_confused_pair(self):
        """Finds a pair (i,j) that has maximum intra-confusion.

        Returns
        -------
        tuple
            tuple (i,j, val) where `i != j` and `val` is the value of intra-confusion
        """

        if self.J <= 1:
            raise SyntaxError(
                "A confusion matrix with 1 class cannot have any confused pair."
            )

        bi = -1
        bj = -1
        bval = -1

        for i in range(self.J - 1):
            for j in range(i + 1, self.J):
                acc = self.M[i, i] + self.M[j, j]
                err = self.M[i, j] + self.M[j, i]
                confusion = err / (acc + err) if abs(acc + err) > 1e-8 else 0.0
                if confusion > bval:
                    bi = i
                    bj = j
                    bval = confusion

        return (bi, bj, bval)

    def find_most_confused_pair2(self, class_error: bool = True):
        """Finds the lightest class i and the class j that is most confused to it.

        Returns
        -------
        tuple
            tuple (i,j, val) where `i != j` and `val` is the value of intra-confusion
        """

        if self.J <= 1:
            raise SyntaxError(
                "A confusion matrix with 1 class cannot have any confused pair."
            )

        # find the lightest class
        i = np.argmin(self.a_weights)

        bj = -1
        bval = -1

        for j in range(self.J):
            if j == i:
                continue
            if class_error:
                acc = self.M[i, i] + self.M[j, j]
                err = self.M[i, j] + self.M[j, i]
                confusion = err / (acc + err) if abs(acc + err) > 1e-8 else 0.0
            else:
                confusion = self.M[i, j] + self.M[j, i]
            if confusion > bval:
                bj = j
                bval = confusion

        return (i, bj, bval)

    def to_hdf5(self, h5_group):
        """Dumps the confusion matrix to a h5py.Group object.

        Parameters
        ----------
        h5_group : h5py.Group
            a :class:`h5py.Group` object to write to

        Raises
        ------
        ImportError
            if h5py is not importable
        ValueError
            if the provided group is not of type :class:`h5py.Group`
        """

        if not base.is_h5group(h5_group):
            raise ValueError("The provided group is not a h5py.Group instance.")

        h5_group.attrs["J"] = self.J
        h5_group.attrs["ll_labels"] = [list(x) for x in self.ls_labels]
        h5_group.create_dataset("M", data=self.M)
        h5_group.create_dataset("a_weights", data=self.a_weights)

    @classmethod
    def from_hdf5(cls, h5_group):
        """Loads a confusion matrix from an HDF5 group.

        Parameters
        ----------
        h5_group : h5py.Group
            a :class:`h5py.Group` object to read from

        Returns
        -------
        ConfusionMatrix
            the loaded confusion matrix
        """

        if not base.is_h5group(h5_group):
            raise ValueError("The provided group is not a h5py.Group instance.")

        J = h5_group.attrs["J"]
        ls_labels = [set(x) for x in h5_group.attrs["ll_labels"]]

        if len(ls_labels) != J:
            raise ValueError("Corrupted data. TBC.")

        M = h5_group["M"][:]

        if M.shape != (J, J):
            raise ValueError("Corrupted data. TBC.")

        a_weights = h5_group["a_weights"][:]

        if a_weights.shape != (J,):
            raise ValueError("Corrupted data. TBC.")

        return ConfusionMatrix(ls_labels, M, a_weights)

    @classmethod
    def from_df(cls, df: pd.DataFrame, ml_kind: tp.Optional[str] = None, logger=None):
        """Loads a confusion matrix from a dataframe.

        The dataframe is supposed to have minimally 3 columns: 'taxcode', 'prediction' and
        'ml_weight'. Column 'taxcode' represents the ground truth taxcode. Column 'prediction'
        is a json string representing a list top-20 of predicted taxcodes and its corresponding
        list of predicted scores, in descending order. Column 'ml_weight' represents the weight
        of each record/event.

        The dataframe can have additionally column 'ml_kind'. In that case, the user can use
        argument `ml_kind` to restrict to a certain kind of data.

        Parameters
        ----------
        df : pandas.DataFrame
            input dataframe to parse from
        ml_kind : str, optional
            the ml_kind to restrict to, if any
        logger : mt.logg.IndentedLoggerAdapter
            logger for debugging purposes

        Returns
        -------
        ConfusionMatrix
            output confusion matrix
        """

        with logg.scoped_info(
            "Extracting a confusion matrix from a taxcode prediction dataframe",
            logger=logger,
        ):
            if ml_kind is not None:
                if logger:
                    logger.info("Restricted to '{}' ml_kind.".format(ml_kind))
                df = df[df["ml_kind"] == ml_kind]

            # prepare the list of taxcodes
            df2 = df[df["taxcode"].notnull()]
            if len(df2) < len(df):
                if logger:
                    logger.info(
                        "Removed {} records with null taxcodes.".format(
                            len(df) - len(df2)
                        )
                    )
                df = df2
            df2 = (
                df2.groupby(["taxcode"])["ml_weight"]
                .sum()
                .to_frame("ml_weight")
                .sort_index()
            )
            df2 = df2.reset_index(drop=False)
            l_taxcodes = df2["taxcode"].tolist()
            a_weights = df2["ml_weight"].values
            J = len(l_taxcodes)
            if logger:
                logger.info(
                    "Found {} true taxcodes out of {} records.".format(J, len(df))
                )

            def get_top1(pred_str):
                pred_taxcode_list = json.loads(pred_str)[0]
                for pred_taxcode in pred_taxcode_list:
                    if pred_taxcode in l_taxcodes:
                        return pred_taxcode
                return "NONE"

            # get top1
            if logger:
                logger.info("Extracting top1 predictions...")
            df["top1"] = df["prediction"].apply(get_top1)

            # regroup, after that df.colunns == ['taxcode', 'top1', 'ml_weight']
            dfg = df.groupby(["taxcode", "top1"])
            df = dfg["ml_weight"].sum().to_frame("ml_weight").reset_index(drop=False)

            # form a joint distribution
            prior_weight = a_weights.sum()
            df = df[df["top1"] != "NONE"]
            df["prob"] = df["ml_weight"] / prior_weight

            # make the confusion matrix
            M = np.zeros((J, J))
            for _, row in df.iterrows():
                i = l_taxcodes.index(row["taxcode"])
                j = l_taxcodes.index(row["top1"])
                M[i][j] += row["prob"]

            # make and return a confusion matrix
            ls_labels = [{x} for x in l_taxcodes]
            return ConfusionMatrix(ls_labels, M, a_weights)

    def accuracy(self):
        """Returns the accuracy extracted from the confusion matrix."""
        return np.diag(self.M).sum()

    def sort_classes(self):
        """Returns an order of classes in increasing order of confusion.

        Returns
        -------
        pandas.DataFrame
            an output dataframe containing columns ['class_index', 'weight', 'confusion'] where the
            first column represents the class index, the second column represents the weight of the
            class and the second column represents the confusion peeled off from each class.
            Confusion means sum of probabilities from the off-diagonal elements of the class.
        """

        J = self.J
        a_indices = np.arange(J)
        M = self.M + self.M.T
        np.fill_diagonal(M, 0)
        data = []
        while J > 0:
            Msum = np.sum(M, axis=0)
            i = np.argmin(Msum)
            j = a_indices[i]
            data.append((j, self.a_weights[j], Msum[i]))
            a_indices = np.delete(a_indices, i)
            M = np.delete(M, i, axis=0)
            M = np.delete(M, i, axis=1)
            J -= 1

        return pd.DataFrame(columns=["class_index", "weight", "confusion"], data=data)
