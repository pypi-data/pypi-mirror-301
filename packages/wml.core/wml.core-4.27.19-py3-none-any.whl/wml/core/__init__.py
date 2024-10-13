import os
import tempfile

from mt import logg, path

from .version import version as __version__


# -----------------------------------------------------------------------------
# module initialisation
# -----------------------------------------------------------------------------


logger = logg.make_logger("mlcore")

# _mp.install(language_level=3)


def init():
    """Initialises the module if it has not been initialised."""
    if init._completed:
        return

    setattr(init, "_home_dirpath", path.join(path.expanduser("~"), ".mlcore"))
    path.make_dirs(init._home_dirpath)

    temp_dirpath = path.join(tempfile.gettempdir(), ".mlcore")
    path.make_dirs(temp_dirpath)
    setattr(init, "_temp_dirpath", temp_dirpath)

    debuglog_filepath = path.join(temp_dirpath, "debug.log")
    if path.exists(debuglog_filepath):
        path.remove(debuglog_filepath)
    setattr(init, "_debuglog_filepath", debuglog_filepath)

    on_winnow_edge = "BALENA" in os.environ
    setattr(init, "_on_winnow_edge", on_winnow_edge)

    init._completed = True


init._completed = False
init()

home_dirpath = init._home_dirpath
temp_dirpath = init._temp_dirpath

on_winnow_edge = init._on_winnow_edge

__all__ = ["logger", "home_dirpath", "temp_dirpath"]
