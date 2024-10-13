"""Abstract classes representing parameters.
"""

import yaml

from mt import tp, path
from mt.base.str import text_filename


class BaseWranglingParams(yaml.YAMLObject):
    yaml_tag = "!BaseWranglingParams"

    """Basic parameters for wrangling the data for training models.

    Parameters
    ----------
    data_localpath : path
        path to the data folder
    wrangled_filename : str
        file name of the wrangled table. Default is 'event_munet_wrangled.pdh5'.
    preceding_model_name : str, optional
        name of the preceding model, if any. For Munet, this can be a Jolee Bindo model name. For
        VFR and MuSolo4, this can be a ChangeNet or NFD model name.
    wrangling_name : str, optional
        default name for the wrangling process. If not provided, the name will be calculated based
        on key parameters. See :func:`name`.
    """

    def __init__(
        self,
        data_localpath: str = "./data",
        wrangled_filename: str = "event_wrangled.pdh5",
        preceding_model_name: tp.Optional[str] = None,
        wrangling_name: tp.Optional[str] = None,
    ):
        self.data_localpath = data_localpath
        self.wrangled_filename = wrangled_filename
        self.preceding_model_name = preceding_model_name
        self.wrangling_name = wrangling_name

    def prepared_dirpath(self):
        dirpath = path.abspath(self.data_localpath)
        path.make_dirs(dirpath)
        return dirpath

    def wrangled_dirpath(self):
        return self.prepared_dirpath()  # base implementation

    def wrangled_filepath(self):
        if self.preceding_model_name:
            filename, fileext = path.splitext(self.wrangled_filename)
            filename = "{}_{}{}".format(
                filename, text_filename(self.preceding_model_name), fileext
            )
        else:
            filename = self.wrangled_filename
        return path.join(self.wrangled_dirpath(), self.wrangled_filename)
