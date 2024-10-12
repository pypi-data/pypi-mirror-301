from .base import Base
import boto3
import fnmatch
import re
from dtr_common.exceptions.errors import ListError, ConnectionError, UploadError, DownloadError, PurgeError
from dtr_common.exceptions.handlers import error_handler
from typing import Optional
from datetime import datetime


class S3Protocol(Base):
    def __init__(self, bucket: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bucket = bucket

    @error_handler(error=ConnectionError)
    def connect(self) -> None:
        if self.credentials is None:
            raise ConnectionError("No credentials provided")
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.credentials["login"],
            aws_secret_access_key=self.credentials["password"],
            endpoint_url=f"http://{self.host}:{self.port}",
        )
        response = self.client.list_buckets()
        if not response:
            raise ConnectionError("Not valid credentials !")


    def disconnect(self) -> None:
        if self.client:
            self.client.close()

    @error_handler(error=ListError)
    def files_infos(self, pattern: str) -> list[dict]:
        regex = fnmatch.translate(pattern)
        dict_files = list()
        if self.path is None:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix="")
        else:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix=f"{self.path}/")

        if metadata.get("Contents", None) is not None:
            dict_files = list(map(lambda m: {"file": m["Key"].split("/")[-1], "size": round(m["Size"]*1.0/1024, 2)}, metadata["Contents"]))
            if self.path is None:
                dict_files = list(filter(lambda f: {"file": "/" not in f["file"], "size": f["size"]}, dict_files))
            dict_files = list(filter(lambda f: {"file": re.search(regex, f["file"]), "size": f["size"]}, dict_files))

            return dict_files
        return []


    @error_handler(error=UploadError)
    def upload(self, src: str, tmp_prefix_dest: Optional[str] = None, final_prefix_dest: Optional[str] = None ) -> None:
        paths = src.split("/")
        filename = paths[-1]
        start_time = datetime.utcnow()

        if self.path is None:
            dest = filename
        else:
            dest = f"{self.path}/{filename}"
        self.client.upload_file(src, self.bucket, dest)

        end_time = datetime.utcnow()
        total_time = end_time - start_time
        
        if self.path is None:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix="")
        else:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix=f"{self.path}/")

        response_contents = metadata.get("Contents", None) 
        if response_contents is not None:
            for rc in response_contents:
                file_size = round(rc.get('Size') / 1024 / 1024)  # file in MB
                self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8

    @error_handler(error=DownloadError)
    def download(self, src: str, dest: str) -> None:
        start_time = datetime.utcnow()
        self.client.download_file(self.bucket, src, dest)

        end_time = datetime.utcnow()
        total_time = end_time - start_time
        
        if self.path is None:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix="")
        else:
            metadata = self.client.list_objects(Bucket=self.bucket, Prefix=f"{self.path}/")

        response_contents = metadata.get("Contents", None) 

        if response_contents is not None:
            for rc in response_contents:
                file_size = round(rc.get('Size') / 1024 / 1024)  # file in MB
                self.data_rate = round(file_size / total_time.total_seconds()) / 2 * 8


    def rename(self, src: str, dest: str) -> None:
        return super().rename(src, dest)

    @error_handler(error=PurgeError)
    def purge(self, src: str) -> None:
        response = self.client.list_buckets()
        if response:
            self.client.delete_object(Bucket=self.bucket, Key=src)
        else:
            raise PurgeError("Not  valid credentials !")
        
