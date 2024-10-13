"""Dataframe snapshotting service."""

from mt import tp, logg, pd, path

from .s3 import list_objects, cache_localpath, cache, upload

__api__ = [
    "get_s3url",
    "list_names",
    "list_ids",
    "latest_id",
    "make_new_id",
    "save",
    "load",
]


def get_s3url(df_name: str, sn_id: int) -> str:
    """Gets the s3url of a dataframe snapshot.

    Parameters
    ----------
    df_name : str
        dataframe name
    sn_id : int
        snapshot id

    Returns
    -------
    s3url : str
        s3cmd url to the snapshot parquet file
    """

    return f"s3://vision-ml-datasets/snapshots/dataframes/{df_name}/sn{sn_id}.parquet"


def list_names(show_progress: bool = False) -> list:
    """Returns the list of names of the dataframes that have snapshots.

    Parameters
    ----------
    show_progress : bool
        show a progress spinner in the terminal

    Returns
    -------
    list
        list of dataframe names available in S3
    """

    s3url = f"s3://vision-ml-datasets/snapshots/dataframes/"
    l_s3urls = list_objects(s3url, show_progress=show_progress)
    l_postfixes = [x[len(s3url) :] for x in l_s3urls]
    l_names = [x[: x.index("/")] for x in l_postfixes]
    return list(frozenset(l_names))


def list_ids(df_name: str, show_progress: bool = False) -> list:
    """Returns the list of snapshots available for a given dataframe.

    Parameters
    ----------
    df_name : str
        dataframe name
    show_progress : bool
        show a progress spinner in the terminal

    Returns
    -------
    list
        list of snapshot ids available for the dataframe
    """

    s3url = f"s3://vision-ml-datasets/snapshots/dataframes/{df_name}/"
    l_s3urls = list_objects(s3url, show_progress=show_progress)
    l_filenames = [x[len(s3url) :] for x in l_s3urls]
    l_ids = [
        int(x[2:-8])
        for x in l_filenames
        if x.startswith("sn") and x.endswith(".parquet")
    ]
    return l_ids


def latest_id(df_name: str) -> int:
    """Returns the list of snapshots available for a given dataframe.

    Parameters
    ----------
    df_name : str
        dataframe name

    Returns
    -------
    list
        list of snapshot ids available for the dataframe

    Raises
    ------
    IndexError
        if there is not snapshot available
    """

    l_ids = list_ids(df_name, show_progress=False)
    if l_ids:
        return max(l_ids)
    raise IndexError(f"No snapshot available for dataframe '{df_name}'.")


def make_new_id(df_name: str) -> int:
    """Makes a new snapshot id based on the current date.

    Parameters
    ----------
    df_name : str
        dataframe name

    Returns
    -------
    int
        a snapshot id based on the current date
    """
    ts = pd.Timestamp.utcnow()
    return (ts.year % 100) * 10000 + ts.month * 100 + ts.day


def save(
    df: pd.DataFrame,
    df_name: str,
    sn_id: tp.Optional[int] = None,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
):
    """Snapshots a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        the dataframe to be saved
    df_name : str
        dataframe name
    sn_id : int, optional
        snapshot id to which the dataframe will be saved. If not provided, the id will be
        automatically generated.
    """

    if sn_id is None:
        sn_id = make_new_id(df_name)

    msg = f"Snapshotting dataframe {df_name} with id {sn_id}"
    with logg.scoped_info(msg, logger=logger):
        s3url = get_s3url(df_name, sn_id)
        filepath = cache_localpath(s3url)
        path.make_dirs(path.dirname(filepath))
        pd.dfsave(df, filepath, show_progress=bool(logger), pack=False)
        upload(filepath, s3url, logger=logger)


def load(
    df_name: str,
    sn_id: tp.Optional[int] = None,
    logger: tp.Optional[logg.IndentedLoggerAdapter] = None,
) -> pd.DataFrame:
    """Loads a dataframe snapshot.

    Parameters
    ----------
    df_name : str
        dataframe name
    sn_id : int, optional
        snapshot id to which the dataframe will be saved. If not provided, the id corresponding to
        the latest snapshot will be used.

    Returns
    -------
    pandas.DataFrame
        the snapnotted dataframe
    """

    if sn_id is None:
        sn_id = latest_id(df_name)

    msg = f"Loading a dataframe {df_name} with snapshot id {sn_id}"
    with logg.scoped_info(msg, logger=logger):
        s3url = get_s3url(df_name, sn_id)
        filepath = cache(s3url, logger=logger)

        return pd.dfload(filepath, show_progress=bool(logger), unpack=False)
