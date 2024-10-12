import logging
import json
from typing import Optional


class JsonFormatter(logging.Formatter):
    def __init__(self, ssystem: str, component: str, version: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ssystem = ssystem
        self.component = component
        self.version = version

    def format(self, record):
        log_data = {
            "Header": {
                "type": "LOG",
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "ssystem": self.ssystem,
                "component": self.component,
                "component_version": self.version,
            },
            "Message": {
                "content": record.getMessage(),
            }
        }
        return json.dumps(log_data)


class JsonReportFormatter(logging.Formatter):
    def __init__(self, task: str, event: str, status: str,
                tpln_string: str, filename_string: str, source_url_string: str, 
                rest_id_string: str, src_ln_string: str,
                target_url_string: str, target_ln_string: str, 
                data_volume_mega_bytes: int, data_rate_mega_bytes_sec: int,
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.task = task
        self.event = event
        self.status = status
        self.tpln_string = tpln_string
        self.source_url_string = source_url_string
        self.filename_string = filename_string
        self.rest_id_string = rest_id_string
        self.src_ln_string = src_ln_string
        self.target_url_string = target_url_string
        self.target_ln_string = target_ln_string
        self.data_volume_mega_bytes = data_volume_mega_bytes
        self.data_rate_mega_bytes_sec = data_rate_mega_bytes_sec

    def format(self, record):
        log_data = {
            'Task': self.task,
            'event': self.event,
            'status': self.status,
            'message': record.getMessage(),
            "Additional_keys": {
                "input": {
                    "source_url_string": self.source_url_string,
                    "filename_string": self.filename_string,
                }
            }
        }
        if self.status == "OK" and self.task == "TransferTrigger":
            log_data["Additional_keys"]["output"] = {"filename_string": self.filename_string,
                                                     "rest_id_string": self.rest_id_string}
        elif self.status == "OK" and self.task == "TransferRequest":
            log_data["Additional_keys"]["output"] = {"rest_id_string": self.rest_id_string}
        elif self.task == "TransferRequest":
            log_data["Additional_keys"]["input"]["source_logical_name_string"] = self.src_ln_string
            log_data["Additional_keys"]["input"]["target_url_string"] = self.target_url_string
            log_data["Additional_keys"]["input"]["target_logical_name_string"] = self.target_ln_string
        elif self.task == "TransferTrigger":
            log_data["Additional_keys"]["input"]["tpln_string"] = self.tpln_string
        elif self.task == "FileDownload" and self.status is None:
            log_data["Additional_keys"]["input"]["target_url_string"] = self.target_url_string
        elif (self.task == "FileDownload" and self.status == "OK") or (self.status == "OK" and self.task == "FileUpload"):
            log_data["Additional_keys"]["data_volume_mega_bytes"] = self.data_volume_mega_bytes
            log_data["Additional_keys"]["data_rate_mega_bytes_sec"] = self.data_rate_mega_bytes_sec 
        else:
            pass    

        return json.dumps(log_data)
