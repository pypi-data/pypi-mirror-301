import logging

from izihawa_loglib import error_log
from izihawa_utils.random import generate_request_id


class RequestContext:
    request_id_length: int = 12

    def __init__(self, request_id: str = None, **kwargs):
        self.request_id = request_id or RequestContext.generate_request_id(
            self.request_id_length
        )
        self.default_fields = {
            "request_id": self.request_id,
            **kwargs,
        }

    @staticmethod
    def generate_request_id(length):
        return generate_request_id(length)

    def add_default_fields(self, **fields):
        self.default_fields.update(fields)

    def statbox(self, **kwargs):
        logging.getLogger("statbox").info(msg={**self.default_fields, **kwargs})

    def user_log(self, **kwargs):
        logging.getLogger("user").info(msg={**self.default_fields, **kwargs})

    def debug_log(self, **kwargs):
        logging.getLogger("debug").debug(msg={**self.default_fields, **kwargs})

    def error_log(self, e, level=logging.ERROR, **fields):
        all_fields = {**self.default_fields, **fields}
        error_log(e, level=level, **all_fields)
