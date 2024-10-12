import requests  # type: ignore[import]
from typing import Literal, cast, Optional
import socket
import logging
import time


def retry_request(
    url: str,
    logger: logging.Logger,
    rp_logger: Optional[logging.Logger | None] =  None,
    method: Literal["POST", "PUT", "DELETE", "GET"] = "GET",
    total: int = 5,
    timeout: int = 10,
    status_forcelist: list[int] = [500, 502, 503, 504],
    **kwargs,
) -> requests.Response:
    for _ in range(total):
        try:
            response = cast(requests.Response, getattr(requests, method.lower())(url, timeout = timeout, **kwargs))
            if response.status_code in status_forcelist:
                time.sleep(10)
                continue
            return response
        except socket.timeout as e:
            logger.error("Timeout connecting to: %s %s", url, e)
            rp_logger.info("Timeout connecting to: %s %s", url, e)
            time.sleep(10)
            continue
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s %s", url, e)
            rp_logger.info("Connection error: %s %s", url, e)
            time.sleep(10)
            continue
