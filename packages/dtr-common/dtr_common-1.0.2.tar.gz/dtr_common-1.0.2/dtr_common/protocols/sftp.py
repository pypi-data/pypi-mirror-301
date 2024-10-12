from .base import Base
from paramiko import SSHClient, AutoAddPolicy
import fnmatch
import re, os
from dtr_common.exceptions.errors import (
    ListError,
    ConnectionError,
    UploadError,
    DownloadError,
    PurgeError,
    RenameError
)
from dtr_common.exceptions.handlers import error_handler
from ..utils import dest_path_renaming
from typing import Optional
from datetime import datetime

class SFTPProtocol(Base):

    def __init__(self, *args, **kwargs) -> None:
        super(*args, **kwargs)
        self.ssh = None

    @error_handler(error=ConnectionError)
    def connect(self) -> None:
        if self.credentials is None:
            raise ConnectionError("No credentials")
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.credentials["login"], self.credentials["password"], allow_agent = False)
        self.client = self.ssh.open_sftp()

    def disconnect(self) -> None:
        if self.client is not None:
            self.client.close()
        if self.ssh is not None:
            self.ssh.close()

    @error_handler(error=ListError)
    def files_infos(self, pattern: str) -> list[dict]:
        regex = fnmatch.translate(pattern)
        dict_files = list()
        if self.path is None:
            objects = self.client.listdir()
        else:
            objects = self.client.listdir(self.path)
            objects = list(map(lambda o: f"{self.path}/{o}", objects))
        files = list(filter(lambda o: re.search(regex, o), objects))
        dict_files = list(map(lambda f: {"file": f.split("/")[-1], "size":self.client.stat(f).st_size }, files))
        return dict_files
    

    @error_handler(error=UploadError)
    def upload(self, src: str, tmp_prefix_dest: Optional[str] = None, final_prefix_dest: Optional[str] = None) -> None:
        start_time = datetime.utcnow()
        original_filename = src.strip("/").split("/")[-1]
        if tmp_prefix_dest is not None:
            filename = tmp_prefix_dest + original_filename 
        else:
            filename = original_filename 

        tmp_dest_path = f"{self.path}/{filename}" if self.path is not None else filename

        if self.path is not None:
            for dir in self.path.strip("/").split("/"):
                if dir not in self.client.listdir():
                    self.client.mkdir(dir)
                self.client.chdir(dir)
            self.client.chdir(None)

        self.client.put(src, tmp_dest_path)

        final_dest_path= dest_path_renaming(self.path, tmp_dest_path, filename, tmp_prefix_dest, final_prefix_dest)
        try:
            self.logger.info("once the upload is over, we can rename the temporary file {} to {}".format(tmp_dest_path, final_dest_path))
            self.rename(tmp_dest_path, final_dest_path)
        except Exception as e:
            self.logger.info("An error occored while renaming temporary file {} to {}: {}".format(tmp_dest_path, final_dest_path, e))

        end_time = datetime.utcnow()
        total_time = end_time - start_time
        
        file_size = round(self.client.stat(src).st_size / 1024 / 1024)  # file in MB
        self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8

    @error_handler(error=DownloadError)
    def download(self, src: str, dest: str) -> None:
        start_time = datetime.utcnow()
        self.client.get(src, dest)

        end_time = datetime.utcnow()
        total_time = end_time - start_time

        file_size = round(self.client.stat(src).st_size / 1024 / 1024)  # file in MB
        self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8

    @error_handler(error=RenameError)
    def rename(self, src: str, dest: str) -> None:
        self.client.rename(src, dest)

    @error_handler(error=PurgeError)
    def purge(self, src: str) -> None:
        self.client.remove(src)
