# This file was auto-generated by Fern from our API Definition.

import typing

from ....core.api_error import ApiError
from ..types.request_validation_error import RequestValidationError


class HttpRequestValidationsError(ApiError):
    def __init__(self, body: typing.List[RequestValidationError]):
        super().__init__(status_code=422, body=body)
