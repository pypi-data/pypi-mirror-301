# pylint: disable=line-too-long

"""Some useful functions to represent contextual objects related to weather data.

This is particularly related to the `winnow_db.weather_info` table, fields 'temperature' and
'icon'.
"""

from mt import tp, np

__all__ = ["vectorise_weather", "weather_icon_list"]


weather_icon_list = [
    "clear-day",
    "clear-night",
    "cloudy",
    "fog",
    "partly-cloudy-day",
    "partly-cloudy-night",
    "rain",
    "sleet",
    "snow",
    "wind",
]


def vectorise_weather(
    temperature: tp.Optional[float] = None, icon: tp.Optional[str] = None
) -> np.ndarray:
    """Converts (temperature, icon) pair into a vectorised weather vector.

    Parameters
    ----------
    temperature : float, optional
        kitchen forecasted weather (in Celcius degree), if provided
    icon : str, optional
        value of the 'icon' field in the weather record

    Returns
    -------
    numpy.ndarray
        a 12-vector which is a concatenation of a 2-vector to represent the temperature followed by
        a 10-vector to represent the icon
    """

    res = np.zeros(12)

    if temperature is None:
        res[1] = 15.0  # (0,15) to represent unknown temperature

    try:
        icon_id = weather_icon_list.index(icon)
        res[2 + icon_id] = 1.0
    except ValueError:
        pass

    return res
