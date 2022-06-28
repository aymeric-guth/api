from typing import Union

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_error_handler(
    _: Request, 
    exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        {"errors": [exc.detail]}, 
        status_code=exc.status_code
    )


async def http422_error_handler(
    _: Request, 
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}


class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


class MiddlewareException(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code


class JWTException(MiddlewareException):
    """"""
