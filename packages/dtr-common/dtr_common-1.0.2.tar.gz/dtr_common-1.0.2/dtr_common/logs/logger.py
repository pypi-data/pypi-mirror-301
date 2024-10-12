import logging
from dtr_common.logs import formatter as fmt


def create_logger(
    name: str, level: str, component: str, version: str, format: str = "json"
) -> logging.Logger:
    level = level.upper()
    if level == "DEBUG":
        lvl = logging.DEBUG
    elif level == "INFO":
        lvl = logging.INFO
    elif level == "WARNING":
        lvl = logging.WARNING
    elif level == "ERROR":
        lvl = logging.ERROR
    else:
        raise NameError(f"Unknown logging level: {level}")

    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(lvl)
    formatter = getattr(fmt, f"{format.capitalize()}Formatter")
    stream_handler.setFormatter(formatter(component, name, version))
    logger.addHandler(stream_handler)
    return logger


def create_rp_logger(name: str, task: str, event: str, status: str = None,
                     tpln_string: str = None, source_url_string: str = None,
                     filename_string: str = None, rest_id_string: str = None, 
                     src_ln_string: str = None, target_url_string: str = None,
                     target_ln_string: str = None, data_volume_mega_bytes: str = None, 
                     data_rate_mega_bytes_sec: str = None,
                     format: str = "json", level: str = logging.INFO) -> logging.Logger:
    report_handler = logging.StreamHandler()
    report_handler.setLevel(level)

    formatter = getattr(fmt, f"{format.capitalize()}ReportFormatter")
    report_handler.setFormatter(formatter(task, event, status,
                                          tpln_string, source_url_string, filename_string, 
                                          rest_id_string, src_ln_string,
                                          target_url_string, target_ln_string,
                                          data_volume_mega_bytes, data_rate_mega_bytes_sec))
    
    rp_logger = logging.getLogger(name)
    rp_logger.setLevel(level)
    rp_logger.addHandler(report_handler)
    return rp_logger

