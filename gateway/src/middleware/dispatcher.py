from typing import (
    Dict,
    MutableMapping,
    Any
)

from fastapi.responses import Response
import httpx

from loguru import logger

from .common.types import (
    Scope,
    Receive,
    Send,
    ASGIApp
)
from .common import parse_headers, error_handler, handle_body, check_path


class DispatchMiddleware:
    def __init__(
        self,
        app: ASGIApp
    ) -> None:
        self.app = app

    @error_handler
    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        if scope.get('type') != 'http':
            return await self.app(scope, receive, send)
        if check_path(scope.get('path')):
            return await self.app(scope, receive, send)

        logger.info('dispatcher')

        *_, endpoint_url = map(
            lambda x: x.decode('utf-8'),
            scope.get('headers').pop(-1)
        )
        logger.info(f'{endpoint_url=}')

        headers: Dict[str, str] = parse_headers(scope.get('headers'))
        request_body: MutableMapping[str, Any] = await handle_body(receive)

        client: httpx.AsyncClient = scope.get('app').state.client
        response: httpx.Response = await client.request(
            method=scope.get('method'),
            url=endpoint_url,
            headers=headers,
            content=request_body.get('body'),
            timeout=10.0
        )

        response: Response = Response(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content
        )
        return await response(scope, receive, send)
