"""Module dealing with defining a food recognition problem.
"""

import warnings

from mt import tp, np, pd, logg

from .cpc import CPCIndexer, get_cpc_key
from .opmode import (
    OpmodeMapperInterface,
    NullOpmodeMapper,
    Crid2OpmodeMapper,
    unique_gpc,
    Predctx2OpmodeMapper,
)


def get_taxcode_list(df: pd.DataFrame) -> tp.Optional[list]:
    """Gets the taxcode list from a dataframe by checking field 'taxcode'."""
    if "slice_code" in df.columns:
        return sorted(df["slice_code"].dropna().drop_duplicates().tolist())
    return None


def filter_taxcodes(df: pd.DataFrame, l_taxcodes: list, logger=None):
    s = df["slice_code"].isin(l_taxcodes)
    if (~s).sum() > 0:
        l_unwanted = df[~s]["slice_code"].drop_duplicates().tolist()
        logger.warn(
            "Detected & removed {} unwanted taxcodes:\n{}".format(
                len(l_unwanted), l_unwanted
            )
        )
        df = df[s]
    return df


def extract_from_cpc_indexer(cpc_indexer: CPCIndexer) -> tuple:
    predctx_key = cpc_indexer.key
    if predctx_key is None or predctx_key == "no_cpc":
        predctx_key = None
        opmode_mapper = NullOpmodeMapper()
    elif predctx_key == "client_region_id":
        opmode_mapper = Crid2OpmodeMapper(cpc_indexer.values, silent=True)
    elif predctx_key == "prediction_context":
        opmode_mapper = Predctx2OpmodeMapper(cpc_indexer.values, silent=True)
    else:
        raise ValueError(
            "Unable to extract an opmode mapper when `predctx_key` is '{}'.".format(
                predctx_key
            )
        )
    return predctx_key, opmode_mapper


class FRProblem:
    """Parameters defining a food recognition problem.

    This class is a generalisation of :class:`FRProblem` and more.

    Parameters
    ----------
    l_taxcodes : list
        A (sorted) list of taxcodes
    predctx_key : {'client_region_id', 'prediction_context', None}
        name of the column in dataframes associated with the problem that contains the prediction
        contexts. If None is provided, the opmode mapper becomes a NullOpmodeMapper instance.
    opmode_mapper : OpmodeMapperInterface, optional
        mapper to map to opmodes for the problem
    av_probs : numpy.ndarray, optional
        A 2D array of K+1 rows and J columns where `K==opmode_mapper.n_opmodes()` and
        `J==len(l_taxcodes)`, that defines a distribution on (global) taxcodes for each opmode.
        Only valid for gen1 or later.
    ll_validTaxcodes : list, optional
        A list of list of valid taxcodes. The number of inner lists must equal
        `opmode_mapper.n_opmodes()`, so that each inner list corresponds to one non-neutral opmode.
        All taxcodes are by definition valid for the neutral opmode. Only valid for gen2 or later.
    gen : int
        The intended class generation. See notes below.

    Notes
    -----

    Gen0 consists of just a taxcode list and a OpmodeMapperInterface. It is equivalent to
    :class:`FRProblem`.

    Gen1 is gen0 together with a list of taxcode distributions for each non-neutral opmode.

    Gen2 is gen1 plus a list of valid taxcodes for each non-neutral opmode.
    """

    # ----- construction -----

    def __init__(
        self,
        l_taxcodes: list,
        predctx_key: tp.Optional[str] = None,
        opmode_mapper: tp.Optional[OpmodeMapperInterface] = None,
        av_probs: tp.Optional[np.ndarray] = None,
        ll_validTaxcodes: tp.Optional[list] = None,
        gen: int = 0,
    ):
        self.gen = gen
        self.l_taxcodes = sorted(l_taxcodes)
        self.predctx_key = predctx_key
        if predctx_key is None:
            self.opmode_mapper = NullOpmodeMapper()
        elif opmode_mapper is not None:
            self.opmode_mapper = opmode_mapper
        else:
            raise ValueError(
                "The prediction context column exists ('{}') but not opmode mapper is provided.".format(
                    predctx_key
                )
            )

        if gen >= 1:
            if av_probs is None:  # assign a uniform distribution for each opmode
                K = self.n_opmodes()
                J = self.n_taxcodes()
                self.av_probs = np.ones((K + 1, J)) / J
            else:
                self.av_probs = av_probs

            if gen >= 2:
                K = self.n_opmodes()
                if (
                    ll_validTaxcodes is None
                ):  # assign the global taxcode list to every opmode
                    self.ll_validTaxcodes = [self.l_taxcodes] * K
                else:
                    self.ll_validTaxcodes = ll_validTaxcodes

            self.normalise()

    @staticmethod
    def from_df(
        df: pd.DataFrame,
        l_taxcodes: tp.Optional[list] = None,
        opmode_mapper: tp.Optional[OpmodeMapperInterface] = None,
        eps: float = 1e-2,
        logger=None,
    ):
        """Constructs an FRProblem instance from a dataframe.

        The dataframe must be equivalent to a 'target_taxcode_distribution.csv' dataframe or an
        'event_munet.csv' dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            input dataframe, expecting, apart from the field corresponding to the precision
            context, fields ['taxcode', 'weight'] if it is a 'target_taxcode_distribution.csv'
            dataframe or fields ['taxcode', 'ml_weight'] if it is an 'event_munet.csv' dataframe
        l_taxcodes : list, optional
            list of taxcodes if known apriori
        opmode_mapper : OpmodeMapperInterface, optional
            mapper to map to opmodes for the problem, if known. Otherwise the mapper will be
            determined from the dataframe.
        eps : float
            threshold for a taxcode to be valid for an opmode. If a taxcode weight is below
            eps*max_weight where max_weight is the maximum weight of all the taxcodes for the
            opmode, then the taxcode is not seen as a valid taxcode for the opmode.
        logger : mt.logg.IndentedLoggerAdapter, optional
            logger for debugging

        Notes
        -----
        Special case, when predctx_key is 'prediction_context', it is possible for the input
        dataframe to not have the prediction context field. In this case, it is assumed that every
        opmode shares the same target taxcode distribution. Agreed with Clem as of 2023/02/21.

        """

        # remove records with null taxcodes
        df = df[df["slice_code"].notnull()]

        if "event_id" in df.columns:
            weight_key = "ml_weight"
        else:
            weight_key = "weight"

        # remove records with null weights
        if weight_key in df.columns:
            df = df[df[weight_key].notnull()]

        if l_taxcodes is None:  # determine the global taxcode list
            l_taxcodes = sorted(df["slice_code"].drop_duplicates().tolist())
        else:
            df = filter_taxcodes(df, l_taxcodes, logger=logger)

        if opmode_mapper is None:
            # check if there is a precision context key
            try:
                predctx_key = get_cpc_key(df)

                # determine the global list of groups of prediction contexts
                l_values = df[predctx_key].dropna().drop_duplicates().tolist()

                # make an opmode mapper
                if predctx_key == "client_region_id":
                    opmode_mapper = Crid2OpmodeMapper(l_values)
                elif predctx_key == "prediction_context":
                    opmode_mapper = Predctx2OpmodeMapper(l_values)
                else:
                    raise NotImplementedError
            except ValueError:  # no key
                predctx_key = "prediction_context"  # assume no non-neutral opmode
                opmode_mapper = Predctx2OpmodeMapper([])
        else:
            predctx_key = opmode_mapper.predctx_key

        if (
            not weight_key in df.columns
        ):  # not a full 'target_taxcode_distribution' dataframe
            return FRProblem(
                l_taxcodes, predctx_key=predctx_key, opmode_mapper=opmode_mapper, gen=0
            )

        if (
            predctx_key == "prediction_context" and predctx_key not in df.columns
        ):  # assume the same distribution across all opmodes
            J = len(l_taxcodes)
            K = opmode_mapper.n_opmodes()

            logg.info(
                "Field 'prediction_context' not detected in the dataframe.",
                logger=logger,
            )
            msg = (
                "Using the same distribution across all {} non-neutral "
                "opmodes.".format(K)
            )
            logg.info(msg, logger=logger)

            # get the global taxcode weight dist
            tw_df = (
                df.groupby("slice_code", dropna=True)[weight_key]
                .sum()
                .to_frame(weight_key)
            )
            df2 = pd.DataFrame(data={"slice_code": l_taxcodes})
            tw_df = df2.join(tw_df, on="slice_code", how="left")
            tw_df[weight_key] = tw_df[weight_key].fillna(0.0)
            tw_df[weight_key] /= tw_df[weight_key].sum()
            a_probs = tw_df[weight_key].values
            av_probs = np.tile(a_probs, (K + 1, 1))
            l_validTaxcodes = tw_df[tw_df[weight_key] > 0]["slice_code"].tolist()
            ll_validTaxcodes = [l_validTaxcodes] * K

            res = FRProblem(
                l_taxcodes,
                predctx_key=predctx_key,
                opmode_mapper=opmode_mapper,
                av_probs=av_probs,
                ll_validTaxcodes=ll_validTaxcodes,
                gen=2,
            )
            res.normalise()
            return res

        # tighten the dataframe
        df = df[["slice_code", predctx_key, weight_key]]

        # get global taxcode weight dist
        tw_df = (
            df.groupby("slice_code", dropna=False)[weight_key]
            .sum()
            .to_frame(weight_key)
        )
        df2 = pd.DataFrame(data={"slice_code": l_taxcodes})
        tw_df = df2.join(tw_df, on="slice_code", how="left")
        tw_df[weight_key] = tw_df[weight_key].fillna(0.0)
        tw_df[weight_key] /= tw_df[weight_key].sum()

        # cleaning up df
        df = df[df[predctx_key].notnull()].copy()
        if predctx_key == "prediction_context":
            df[predctx_key] = df[predctx_key].apply(unique_gpc)

        # add column 'opmode_weight'
        df = (
            df.groupby([predctx_key, "slice_code"], dropna=False)[weight_key]
            .sum()
            .to_frame(weight_key)
        )
        df = df.reset_index(drop=False)
        df_sum = (
            df.groupby(predctx_key, dropna=False)[weight_key]
            .max()
            .to_frame("opmode_weight")
        )
        df = df.join(df_sum, on=predctx_key)

        # filter out taxcodes with a small weight
        df = df[df[weight_key] >= df["opmode_weight"] * eps]

        J = len(l_taxcodes)
        K = opmode_mapper.n_opmodes()
        O = opmode_mapper.neutral_opmode()
        av_probs = np.empty((K + 1, J))
        av_probs[O, :] = tw_df[weight_key].to_numpy()
        ll_validTaxcodes = [None] * K
        data = []
        if J > 0 and K > 0:
            gen = 2
            for _, row in df.iterrows():
                k = opmode_mapper(row[predctx_key])
                if k < 0 or k == O:  # neutral opmode
                    continue
                k2 = k if k < O else k - 1
                taxcode = row["slice_code"]
                j = l_taxcodes.index(taxcode)
                av_probs[k2, j] = row[weight_key]
                if ll_validTaxcodes[k2] is None:
                    ll_validTaxcodes[k2] = [taxcode]
                else:
                    ll_validTaxcodes[k2].append(taxcode)

            for k in range(K):
                x = ll_validTaxcodes[k]
                if x is None:
                    ll_validTaxcodes[k] = []
                else:
                    ll_validTaxcodes[k] = sorted(list(set(x)))
                if logger:
                    data.append((k, len(ll_validTaxcodes[k])))
        else:
            gen = 0

        if logger and len(data) > 0:
            df2 = pd.DataFrame(columns=["opmode", "count"], data=data)
            with logger.scoped_debug(
                "The constructed FR problem has {} global taxcodes".format(J),
                curly=False,
            ):
                logger.debug(df2)
                logger.debug("The largest count is {}.".format(df2["count"].max()))

        res = FRProblem(
            l_taxcodes,
            predctx_key=predctx_key,
            opmode_mapper=opmode_mapper,
            av_probs=av_probs,
            ll_validTaxcodes=ll_validTaxcodes,
            gen=gen,
        )
        res.normalise()
        return res

    # ----- properties -----

    def n_taxcodes(self, opmode: int = -1) -> int:
        """Gets the number of taxcodes, globally or per opmode.

        Parameters
        ----------
        opmode : int
            the index of the opmode where we want to get the number of taxcodes. Only valid for
            gen1 or later. Default value -1 means globally.

        Returns
        -------
        int
            number of (valid) taxcodes
        """
        if opmode < 0 or self.gen < 1 or opmode == self.neutral_opmode():
            return len(self.l_taxcodes)

        k2 = self.ll_index(opmode)
        return len(self.ll_validTaxcodes[k2])

    def v_validTaxcodes(self, opmode: int = -1) -> np.ndarray:
        """Returns an int vector representing which taxcode is valid, globally or per opmode.

        Parameters
        ----------
        opmode : int
            the index of the opmode where we want to get the number of taxcodes. Only valid for
            gen2 or later. Default value -1 means globally.

        Returns
        -------
        numpy.ndarray
            an int32 vector with dimensionality equal to the global number of taxcodes, where the
            valid taxcodes have value 1, and invalid ones have value 0.
        """

        J = self.n_taxcodes()
        if opmode < 0 or self.gen <= 1 or opmode == self.neutral_opmode():
            return np.ones(J, dtype=np.int32)

        res = np.zeros(J, dtype=np.int32)
        k2 = self.ll_index(opmode)
        for taxcode in self.ll_validTaxcodes[k2]:
            res[self.l_taxcodes.index(taxcode)] = 1
        return res

    def n_opmodes(self) -> int:
        """Gets the number of non-neutral opmodes."""
        return self.opmode_mapper.n_opmodes()

    def neutral_opmode(self) -> int:
        """Gets the value of the neutral opmode."""
        return self.opmode_mapper.neutral_opmode()

    def ll_index(self, opmode):
        null_opmode = self.neutral_opmode()
        if opmode == null_opmode:
            return -1
        if opmode > null_opmode:
            return opmode - 1
        return opmode

    # ----- modification -----

    def normalise(self, eps: float = 1e-5):
        """Normalises each taxcode distribution per opmode to that they are indeed distributions.

        Parameters
        ----------
        eps : float
            threshold to check if the sum of values is zero
        """
        if self.gen < 1:
            return

        def normalise_av(k: int):
            the_sum = self.av_probs[k].sum()
            if abs(the_sum) < eps:
                warnings.warn(
                    "Not normalising opmode {} as it has {} sum of probabilities.".format(
                        k, the_sum
                    )
                )
            else:
                self.av_probs[k] /= the_sum

        K = self.n_opmodes()
        if self.gen == 1:
            for k in range(K + 1):
                normalise_av(k)
        else:
            for k in range(K + 1):
                if k != self.opmode_mapper.neutral_opmode():
                    self.av_probs[k] *= self.v_validTaxcodes(k)
                normalise_av(k)

    def resize_opmodes(self, new_n_opmodes: int):
        """Reduces the number of non-neutral opmodes to a given number."""
        if new_n_opmodes < 0:
            raise ValueError("Cannot resize to a negative number.")
        K = self.n_opmodes()
        if new_n_opmodes > K:
            raise ValueError("Cannot resize to a number larger than {}.".format(K))
        if new_n_opmodes == K:
            return  # nothing to resize
        if hasattr(self.opmode_mapper, "l_crids"):
            self.opmode_mapper.l_crids = self.opmode_mapper.l_crids[:new_n_opmodes]
        elif hasattr(self.opmode_mapper, "l_gpcs"):
            self.opmode_mapper.l_gpcs = self.opmode_mapper.l_gpcs[:new_n_opmodes]
        else:
            raise NotImplementedError
        if self.gen < 1:
            return

        # TODO: copy av_probs properly in light of neutral opmode. Right now this section only
        # works with neutral opmode of value 0 or N
        av_probs = self.av_probs[: new_n_opmodes + 1].copy()
        if self.opmode_mapper.neutral_opmode() > 0:
            av_probs[new_n_opmodes] = self.av_probs[K]
        self.av_probs = av_probs
        if self.gen < 2:
            return

        self.ll_validTaxcodes = self.ll_validTaxcodes[:new_n_opmodes]

    # ----- serialisation -----

    def to_json(self):
        """Converts the instance into a json object that can be serialised using json.dumps."""
        res = {
            "gen": self.gen,
            "l_taxcodes": self.l_taxcodes,
            "predctx_key": self.predctx_key,
        }
        if self.predctx_key in ["client_region_id", "prediction_context"]:
            res["opmode_mapper"] = self.opmode_mapper.to_json()
        if self.gen < 1:
            return res

        res["av_probs"] = self.av_probs.tolist()
        if self.gen < 2:
            return res

        res["ll_validTaxcodes"] = self.ll_validTaxcodes
        return res  # for now

    @staticmethod
    def from_json(json_dict):
        """Creates an FRProblem instance from a json object loaded using json.loads."""

        if not "gen" in json_dict:  # FRProblem
            l_taxcodes = json_dict["taxcode_list"]
            if "client_region_id_list" in json_dict:
                predctx_key = "client_region_id"
                opmode_mapper = Crid2OpmodeMapper(
                    json_dict["client_region_id_list"], silent=True
                )
            else:
                cpc_json = json_dict["cpc_indexer"]
                if cpc_json is None:
                    predctx_key = None
                    opmode_mapper = NullOpmodeMapper()
                else:
                    cpc_indexer = CPCIndexer.from_json(cpc_json)
                    predctx_key, opmode_mapper = extract_from_cpc_indexer(cpc_indexer)

            if opmode_mapper.n_opmodes() == 1:
                opmode_mapper = NullOpmodeMapper()
            elif opmode_mapper.n_opmodes() > 1:  # need to deal with weights
                raise NotImplementedError
            return FRProblem(
                l_taxcodes, predctx_key=predctx_key, opmode_mapper=opmode_mapper, gen=0
            )

        gen = json_dict["gen"]
        l_taxcodes = json_dict["l_taxcodes"]
        if "predctx_key" in json_dict:  # new version
            predctx_key = json_dict["predctx_key"]
            if predctx_key is None:
                opmode_mapper = NullOpmodeMapper()
            elif predctx_key == "client_region_id":
                opmode_mapper = Crid2OpmodeMapper.from_json(json_dict["opmode_mapper"])
            elif predctx_key == "prediction_context":
                opmode_mapper = Predctx2OpmodeMapper.from_json(
                    json_dict["opmode_mapper"]
                )
            else:
                raise OSError(
                    "Unable to import when `predctx_key` is '{}'.".format(predctx_key)
                )
        elif "cpc_indexer" in json_dict:  # old version
            cpc_indexer = CPCIndexer.from_json(json_dict["cpc_indexer"])
            predctx_key, opmode_mapper = extract_from_cpc_indexer(cpc_indexer)
        else:
            raise NotImplementedError
        if gen < 1:
            return FRProblem(
                l_taxcodes,
                predctx_key=predctx_key,
                opmode_mapper=opmode_mapper,
                gen=gen,
            )

        av_probs = np.array(json_dict["av_probs"])
        if gen < 2:
            return FRProblem(
                l_taxcodes,
                predctx_key=predctx_key,
                opmode_mapper=opmode_mapper,
                av_probs=av_probs,
                gen=gen,
            )

        ll_validTaxcodes = json_dict["ll_validTaxcodes"]
        return FRProblem(
            l_taxcodes,
            predctx_key=predctx_key,
            opmode_mapper=opmode_mapper,
            av_probs=av_probs,
            ll_validTaxcodes=ll_validTaxcodes,
            gen=gen,
        )

    # ----- utility -----

    def make_dist_df(self):
        """Makes a dataframe representing weight distributions.

        Returns
        -------
        df : pandas.DataFrame
            a dataframe with columns `['opcode', 'taxcode', 'weight']` that contains a taxcode
            distribution for each opmode, including the neutral opmode

        Notes
        -----
        The member function requires gen2 instances or later.
        """

        if self.gen < 2:
            raise ValueError(
                "Function is only valid for gen2 instance. Got gen {}.".format(self.gen)
            )

        data = []
        J = self.n_opmodes()
        O = self.opmode_mapper.neutral_opmode()
        K = self.n_taxcodes()
        for j in range(J + 1):
            j2 = self.ll_index(j)
            if j == O:
                l_validTaxcodes = self.l_taxcodes
            else:
                l_validTaxcodes = self.ll_validTaxcodes[j2]

            for taxcode in l_validTaxcodes:
                k = self.l_taxcodes.index(taxcode)
                data.append((j, taxcode, self.av_probs[j2, k]))

        return pd.DataFrame(columns=["opmode", "slice_code", "weight"], data=data)
