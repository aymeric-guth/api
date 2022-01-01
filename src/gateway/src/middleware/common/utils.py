from typing import (
    List,
    Tuple,
    Dict,
    Callable,
    MutableMapping,
    Any,
    Optional
)
import re
from functools import wraps

from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_501_NOT_IMPLEMENTED
)
from httpx import TransportError

from loguru import logger

from .types import (
    Scope,
    Receive,
    Send,
)
from ...config import Services
from ...errors import MiddlewareException, JWTException


def parse_headers(
        raw_headers: List[Tuple[bytes, bytes]]
) -> Dict[str, str]:
    # moment opportun pour vérifier la validité des headers
    if raw_headers is None:
        raise MiddlewareException(
            message='Invalid headers',
            status_code=HTTP_400_BAD_REQUEST
        )
    return {
        k.decode('utf-8'): v.decode('utf-8')
        for k, v in raw_headers
    }


async def handle_body(
    receive: Receive
) -> MutableMapping[str, Any]:
    try:
        body = await receive()
        if body.get('more_body'):
            raise MiddlewareException(
                message='More body awailable, can\'t process request (NotImplementedError)',
                status_code=HTTP_501_NOT_IMPLEMENTED
            )
    except Exception as err:
        raise MiddlewareException(
            message='Body exception occured',
            status_code=HTTP_501_NOT_IMPLEMENTED
        )
    return body


@logger.catch
def error_handler(fnc: Callable) -> Callable:
    @wraps(fnc)
    async def inner(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        try:
            return await fnc(self, scope, receive, send)
        except (MiddlewareException, JWTException) as err:
            response: JSONResponse = JSONResponse(
                content={"errors": [err.message]},
                status_code=err.status_code
            )
            return await response(scope, receive, send)
        except TransportError as err:
            response: JSONResponse = JSONResponse(
                content={"errors": ['Internal communication error, service didn\'t respond', str(err)]},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
            return await response(scope, receive, send)
        except Exception as err:
            response: JSONResponse = JSONResponse(
                content={"errors": ['Unexpected error occurred', str(err)]},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
            await response(scope, receive, send)
            raise

    return inner


def check_path(path: str) -> Optional[bool]:
    # logger.info(f'{path=} {re.match(Services.PATTERN, path)}')

    if path is None or re.match(Services.PATTERN, path):
        return True
