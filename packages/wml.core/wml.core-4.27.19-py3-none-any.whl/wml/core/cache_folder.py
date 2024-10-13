import json
import os

from mt import path

from .clujdc import in_clujdc
from . import logger


__all__ = ["CacheFolderManager"]


class CacheFolderManager(object):
    """Manages a cache folder (and all of its subfolders) to make sure its storage size is below a threshold.

    This is done by regularly removing files whose access time is too old."""

    def __init__(self, cache_dirpath, storage_limit=1073741824):
        """Initialises the manager.

        Parameters
        ----------
        cache_dirpath : str
            local path to the cache folder
        storage_limit : int
            default storage limit in bytes if the config json file does not exist in the cache
            folder. Default is 1GB.
        """
        path.make_dirs(cache_dirpath)
        self.cache_dirpath = cache_dirpath

        if in_clujdc:
            gid = os.getgid()
            if gid != 100:
                logger.error(
                    f"You are running a program ClujDC but your GID is {gid}, which does not correspond to group 'users'."
                )
                logger.error(
                    "Writing files to the cache folder using this GID will break the structure of the folder."
                )
                logger.error(
                    "Please stop the program and change your GID to 100 before restarting."
                )

        config_filepath = path.join(cache_dirpath, "config.json")
        default_cache_server = {"host": None, "port": 22, "username": None}
        if path.exists(config_filepath):
            conf = json.load(open(config_filepath, "rt"))
        else:
            conf = {
                "storage_limit": storage_limit,
                "cache_server": default_cache_server,
            }
            json.dump(conf, open(config_filepath, "wt"))

        self.storage_limit = conf["storage_limit"]
        self.cache_server_info = conf.get("cache_server", default_cache_server)
        self.source_ip = conf.get("source_ip", None)
        self.cache_server_conn = None  # not connected yet

    def get_file_from_cache_server(
        self, filepath: str, file_mode: int = 0o664, logger=None
    ) -> int:
        """Gets a file from the cache server.

        Parameters
        ----------
        filepath : str
            local filepath to the file to be downloaded from the cache server
        file_mode : int
            to be passed directly to `os.chmod()` if not None
        logger : mt.logg.IndentedLoggerAdapter, optional
            logger for debugging purposes

        Returns
        -------
        int
            number of bytes downloaded

        Raises
        ------
        ValueError
            if the file is not in the `.mlcore` folder
        OSError
            if the file is not found, the sftp server is not connected, or any other network/IO
            reason
        """

        pos = filepath.find(".mlcore/")
        if pos < 0:
            raise ValueError("File not in the '.mlcore' folder: '{}'.".format(filepath))

        remote_filepath = "/data/" + filepath[pos:]

        if self.cache_server_conn is None:  # initialise it
            if self.cache_server_info["host"] is not None:  # disable for now
                try:
                    import paramiko

                    ssh_client = paramiko.SSHClient()
                    ssh_client.load_system_host_keys()
                    ssh_client.connect(
                        self.cache_server_info["host"],
                        port=self.cache_server_info.get("port", 22),
                        username=self.cache_server_info.get("username", None),
                        key_filename=self.cache_server_info.get("key_filename", None),
                    )
                    sftp = ssh_client.open_sftp()
                    self.cache_server_conn = (ssh_client, sftp)
                    if logger:
                        logger.debug(
                            "Connected to cache server '{}'.".format(
                                self.cache_server_info["host"]
                            )
                        )
                except:
                    if logger:
                        logger.warn_last_exception()
                        logger.warn(
                            "Will not use cache server '{}'.".format(
                                self.cache_server_info["host"]
                            )
                        )
                    self.cache_server_conn = False
            else:
                self.cache_server_conn = False

        if not self.cache_server_conn:
            raise OSError("There is no cache server.")

        sftp = self.cache_server_conn[1]
        try:
            lstat = sftp.lstat(remote_filepath)
        except FileNotFoundError as e:
            msg = "No remote file '{}'".format(remote_filepath)
            raise FileNotFoundError(e.errno, msg, filepath)

        file_size = lstat.st_size
        filepath2 = filepath + ".mttmp"
        sftp.get(remote_filepath, filepath2)
        if file_mode is not None:
            path.chmod(filepath2, file_mode)
        path.rename(filepath2, filepath, overwrite=True)
        path.utime(filepath, (lstat.st_atime, lstat.st_mtime))

        return file_size

    def regulate(self, logger=None):
        """Invoke this member function regularly, but not too frequently, to clean up the folder."""
        files2 = []
        for root, dirs, files in path.walk(self.cache_dirpath):
            for file in files:
                file_path = path.join(root, file)
                file_size = path.getsize(file_path)
                file_atime = path.stat(file_path).st_atime
                file_record = (file_path, file_size, file_atime)
                files2.append(file_record)

        files2 = sorted(files2, key=lambda x: x[2])  # sort by access time
        if logger:
            logger.debug("Sorted files: {}".format(str(files2)))

        total_storage = sum((x[1] for x in files2))  # sum by size
        if logger:
            logger.debug("Total storage: {}".format(total_storage))

        files3 = []  # list of files to be removed
        for f in files2:
            if total_storage <= self.storage_limit:
                break
            files3.append(f[0])
            total_storage -= f[1]

        if logger:
            logger.debug("Files to be removed: {}".format(files3))
        for f in files3:
            path.remove(f)
