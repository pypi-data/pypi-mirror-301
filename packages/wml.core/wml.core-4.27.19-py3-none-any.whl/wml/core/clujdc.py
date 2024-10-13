# pylint: disable=import-outside-toplevel

"""Modules that are only available when the machine is in ClujDC.
"""

import socket


from . import home_dirpath


from mt import path


__api__ = [
    "web_http_prefix",
    "web_dirpath",
    "in_clujdc",
    "in_gh",
    "in_gh2",
    "as_filepath",
]


web_http_prefix = "http://clujdc.edge.winnowsolutions.com:8970/web"
web_dirpath = path.join(home_dirpath, "web")


in_clujdc = None
in_gh = None
in_gh2 = None


def init():
    global in_clujdc, in_gh, in_gh2
    if in_clujdc is not None:
        return

    hostname = socket.gethostname()
    in_gh = hostname.startswith("grasshopper") or (hostname == "trainer")
    in_gh2 = hostname.startswith("gh2")
    in_clujdc = in_gh or in_gh2


init()


def as_filepath(http_url: str) -> str:
    if not http_url.startswith(web_http_prefix):
        raise ValueError(f"Wrong clujdc http url: {http_url}")
    return web_dirpath + http_url[len(web_http_prefix) :]
