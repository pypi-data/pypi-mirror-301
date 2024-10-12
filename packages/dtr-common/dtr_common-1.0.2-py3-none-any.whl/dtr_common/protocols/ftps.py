from .base import Base
from ..ftp.ftps import MYFTPS
from ..ftp.ftp_util import generate_tls_context
import re
import os
import fnmatch
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
from typing import Union
from datetime import datetime


class FTPSProtocol(Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cert_path = os.environ.get("DTR_CERT_PATH", "/usr/ssl/certs")

    @error_handler(error=ConnectionError)
    def connect(self, check_hostname: bool = False) -> None:
        ctx = generate_tls_context(certpath=self.cert_path, check_hostname=check_hostname)
        self.client = MYFTPS(context=ctx)
        self.client.connect(self.host, self.port)
        if self.credentials is not None:
            self.client.login(self.credentials["login"], self.credentials["password"])
        self.client.prot_p()

    def disconnect(self) -> None:
        if self.client:
          self.client.close()
        

    @error_handler(error=ListError)
    def files_infos(self, pattern: str) -> list[dict]:
        regex = fnmatch.translate(pattern)  # translate filename pattern into regex
        dict_files = list()
        if self.path is None:
            files = self.client.nlst()
        else:
            files = self.client.nlst(self.path)
        files = list(filter(lambda f: re.search(regex, f), files))
        dict_files = list(map(lambda f: {"file": f.split("/")[-1], "size":self.client.size(f)}, files))
        return dict_files
    
    @error_handler(error=UploadError)
    def upload(self, src: str, tmp_prefix_dest: Union[str, None], final_prefix_dest: Union[str, None]) -> None:
        start_time = datetime.utcnow()
        original_filename = src.strip("/").split("/")[-1]
        if tmp_prefix_dest is not None:
            filename = tmp_prefix_dest + original_filename 
        else:
            filename = original_filename 

        tmp_dest_path = f"{self.path}/{filename}" if self.path is not None else filename

        if self.path is not None:
            for dir in self.path.strip("/").split("/"):
                if dir not in self.client.nlst():
                    self.client.mkd(dir)
                self.client.cwd(dir)
            self.client.cwd("/")

        with open(src, "rb") as handler:
            self.client.storbinary(f"STOR {tmp_dest_path}", handler)

        final_dest_path= dest_path_renaming(self.path, tmp_dest_path, filename, tmp_prefix_dest, final_prefix_dest)
        
        try:
            self.logger.info("once the upload is over, we can rename the temporary file {} to {}".format(tmp_dest_path, final_dest_path))
            self.rename(tmp_dest_path, final_dest_path)
        except Exception as e:
            self.logger.info("An error occored while renaming file: {}: {}".format(final_dest_path, e))

        end_time = datetime.utcnow()
        total_time = end_time - start_time

        file_size = round(self.client.size(src) / 1024 / 1024)  # file in MB
        self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8

    @error_handler(error=DownloadError)
    def download(self, src: str, dest: str) -> None:
        start_time = datetime.utcnow()
        with open(dest, "wb") as handler:
            self.client.retrbinary(f"RETR {src}", handler.write)
            
        end_time = datetime.utcnow()
        total_time = end_time - start_time

        file_size = round(self.client.size(src) / 1024 / 1024)  # file in MB
        self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8

    @error_handler(error=RenameError)
    def rename(self, src: str, dest: str) -> None:
        self.client.rename(src, dest)

    @error_handler(error=PurgeError)
    def purge(self, src: str) -> None:
        self.client.delete(src)
