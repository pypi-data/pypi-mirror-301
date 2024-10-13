# pylint: disable=line-too-long

"""Some useful functions to represent contextual objects related to timestamp and utc
"""

from dateutil.tz import tzoffset

from mt import tp, np, pd

from .base import vectorise_periodic


__all__ = [
    "vectorise_timestamp",
    "vectorise_timestamp_with_utc",
    "vectorise_local_timestamp",
]


def vectorise_timestamp(ts: pd.Timestamp = None) -> np.ndarray:
    """Converts timestamp into a 12D vector.

    Parameters
    ----------
    ts : pandas.Timestamp, optional
        timestamp, with or without timezone

    Returns
    -------
    numpy.ndarray
        a 12-vector of (second_per_minute, minute_per_hour, hour_per_day, day_per_month,
        month_per_year, day_of_week_as_7D_one_hot)
    """

    if pd.isnull(ts):
        return np.zeros(12)

    second_per_minute = ts.second / 60
    minute_per_hour = ts.minute / 60

    if ts.tz is None:  # no timezone
        hour_per_day = -1  # hour cannot be trusted
        month_per_year = ts.month / 12  # estimate
        day_per_month = ts.day / ts.days_in_month  # estimate
        day_of_week = ts.day_of_week  # estimate
    else:
        ts2 = ts.tz_localize(None)
        hour_per_day = ts2.hour / 24
        month_per_year = ts2.month / 12
        day_per_month = ts2.day / ts2.days_in_month
        day_of_week = ts2.day_of_week

    res = np.array(
        [
            second_per_minute,
            minute_per_hour,
            hour_per_day,
            day_per_month,
            month_per_year,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
    )
    res[5 + day_of_week] = 1  # one-hot for day-of-week
    return res


def vectorise_timestamp_with_utc(
    ts: pd.Timestamp = None, utc: tp.Optional[float] = None
) -> np.ndarray:
    """Converts timestamp with optionally utc into a 14D vector.

    Parameters
    ----------
    ts : pandas.Timestamp, optional
        timestamp, with or without timezone
    utc : float, optional
        UTC offset (in hours)

    Returns
    -------
    numpy.ndarray
        a 12-vector of (utc_validity, utc, second_per_minute, minute_per_hour, hour_per_day,
        day_per_month, month_per_year, day_of_week_as_7D_one_hot)
    """

    vec = np.zeros(14)
    if not pd.isnull(utc):
        if (
            timestamp is not None and timestamp.tz is None
        ):  # insert utc to the current timestamp
            utc_offset = tzoffset(None, utc * 3600.0)
            timestamp = timestamp.tz_localize(utc_offset)
        vec[0] = 1.0
        vec[1] = utc

    vec[2:] = vectorise_timestamp(timestamp)

    return vec


def vectorise_local_timestamp(
    ts: tp.Optional[pd.Timestamp] = None,
    is_local: bool = True,
    utc_offset: tp.Optional[float] = None,
) -> np.ndarray:
    """Converts the local time of a timestamp with optionally an utc offset into a 14D vector.

    Parameters
    ----------
    ts : pandas.Timestamp, optional
        timestamp, with or without timezone
    is_local : bool
        whether or not `ts` is in local time. Only valid if no timezone is provided in `ts`.
    utc_offset : float, optional
        UTC offset (in hours) of the timezone. For example, Singapore has UTC offset 8.0.

    Returns
    -------
    numpy.ndarray
        a 14-vector of (utc_validity, utc, ts_validity, second_per_minute, minute_per_hour,
        hour_per_day, day_per_month, month_per_year, day_of_week)

    Notes
    -----
    If `ts` is None, only `utc_offset` is used, if itself is not None.
    If `ts` has timezone, both `is_local` and `utc_offset` are ignored.
    If `ts` has no timezone and is in local time, `utc_offset` is used if itself is not None.
    If `ts` has no timezone and is in UTC+0, we half-use `ts` if `utc_offset` is not None.
    """

    vec = np.zeros(14, dtype=np.float32)  # default
    no_utc = pd.isnull(utc_offset)

    if ts is None:  # no valid ts
        if not no_utc:
            vec[0:2] = vectorise_periodic(utc_offset / 24 + 0.5)
        return vec

    if ts.tz is not None:  # ts has timezone
        vec[0:2] = vectorise_periodic(
            ts.tz.utcoffset(None).total_seconds() / 86400 + 0.5
        )
        vec[2:4] = vectorise_periodic(ts.second / 60)
        vec[4:6] = vectorise_periodic(ts.minute / 60)
        vec[6:8] = vectorise_periodic(ts.hour / 24)
        vec[8:10] = vectorise_periodic(ts.month / 12)
        vec[10:12] = vectorise_periodic(ts.day / ts.days_in_month)
        vec[12:14] = vectorise_periodic(ts.day_of_week / 7)
        return vec

    if is_local:  # ts in local time, maybe coming from the system
        if utc_offset is not None:
            vec[0:2] = vectorise_periodic(utc_offset / 24 + 0.5)
        vec[2:4] = vectorise_periodic(ts.second / 60)
        vec[4:6] = vectorise_periodic(ts.minute / 60)
        vec[6:8] = vectorise_periodic(ts.hour / 24)
        vec[8:10] = vectorise_periodic(ts.month / 12)
        vec[10:12] = vectorise_periodic(ts.day / ts.days_in_month)
        vec[12:14] = vectorise_periodic(ts.day_of_week / 7)
        return vec

    # ts with UTC+0, maybe coming from the muv1 database

    if no_utc:  # we don't know the UTC offset
        vec[2:4] = vectorise_periodic(ts.second / 60)
        vec[4:6] = vectorise_periodic(ts.minute / 60)
        vec[8:10] = vectorise_periodic(ts.month / 12)
        vec[10:12] = vectorise_periodic(ts.day / ts.days_in_month)
        return vec

    vec[0:2] = vectorise_periodic(utc_offset / 24 + 0.5)
    ts = ts.tz_localize(
        tzoffset(None, 0.0)
    )  # make it tz-aware so tz_convert can be invoked
    ts = ts.tz_convert(tzoffset(None, utc_offset * 3600.0))  # convert to local time
    vec[2:4] = vectorise_periodic(ts.second / 60)
    vec[4:6] = vectorise_periodic(ts.minute / 60)
    vec[6:8] = vectorise_periodic(ts.hour / 24)
    vec[8:10] = vectorise_periodic(ts.month / 12)
    vec[10:12] = vectorise_periodic(ts.day / ts.days_in_month)
    vec[12:14] = vectorise_periodic(ts.day_of_week / 7)
    return vec
