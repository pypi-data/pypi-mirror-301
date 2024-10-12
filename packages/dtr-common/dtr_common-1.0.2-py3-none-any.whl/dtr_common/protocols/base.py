from abc import ABC, abstractmethod
from dtr_common.types.models import TargetJson
from typing import Optional
from logging import Logger
from datetime import datetime

class Base(ABC):
    def __init__(self, logger: Logger, target: TargetJson, path: str | None = None, 
                 data_rate: int | None = None, **kwargs) -> None:
        self.host = target["host"]
        self.port = target["port"]
        self.credentials = target["credentials"]
        self.path = path
        self.target = target
        self.client = None
        self.logger = logger
        self.data_rate = data_rate


    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def files_infos(self, pattern: str) -> list[dict]:
        pass


    @abstractmethod
    def upload(self, src: str, tmp_prefix_dest: Optional[str] = None, final_prefix_dest: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def download(self, src: str, dest: str) -> None:
        pass

    @abstractmethod
    def purge(self, src: str) -> None:
        pass

    @abstractmethod
    def rename(self, src: str, dest: str) -> None:
        pass
