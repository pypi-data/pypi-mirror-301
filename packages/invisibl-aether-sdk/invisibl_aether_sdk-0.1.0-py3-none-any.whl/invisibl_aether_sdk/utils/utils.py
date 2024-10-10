import json
import logging
import logging.config
import os
from typing import Literal, Union

import requests


class Utils:
    @staticmethod
    def send_api_request(
        method: Literal[
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "CONNECT",
            "OPTIONS",
            "TRACE",
            "PATCH",
        ],
        url: str,
        request_payload: Union[dict, None],
        headers: Union[dict, None] = None,
        timeout: int = 62,
        auth: bool = False,
        user_id: Union[str, None] = None,
        api_key: Union[str, None] = None,
    ):
        if headers is None:
            headers = {}
        user_id = os.environ.get("AETHER_USER_ID", user_id)
        api_key = os.environ.get("AETHER_API_KEY", api_key)

        if auth:
            headers.update(
                {
                    os.environ.get("AUTH_API_KEY_HEADER", "x-api-key"): api_key,
                    os.environ.get("AUTH_USER_HEADER", "x-user-id"): user_id,
                }
            )
        if "User-Agent" not in headers:
            headers["User-Agent"] = os.environ.get("AETHER_USER_AGENT", "aether-sdk")

        return getattr(requests, method.lower())(
            url=url,
            json=request_payload,
            headers=headers,
            # timeout=timeout,
        )

    @staticmethod
    def setup_logger(
        name: str,
        log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITCAL"] = "INFO",
    ):
        log_format = {
            "timestamp": "%(asctime)s",
            "filename": "%(filename)s",
            "line": "%(lineno)d",
            "level": "%(levelname)s",
            "message": "%(message)s",
            "function_name": "%(funcName)s",
        }

        settings = {
            "version": 1,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "detailed",
                    "stream": "ext://sys.stdout",
                }
            },
            "formatters": {
                "detailed": {
                    "format": json.dumps(log_format),
                }
            },
            "loggers": {
                "extensive": {
                    "level": log_level,
                    "handlers": [
                        "console",
                    ],
                },
            },
        }

        logging.config.dictConfig(settings)
        return logging.getLogger(name)
