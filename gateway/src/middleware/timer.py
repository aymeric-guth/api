import time

from .common.types import (
    Scope,
    Receive,
    Send,
    ASGIApp
)
from loguru import logger


class TimerMiddleware:
    def __init__(
            self,
            app: ASGIApp
    ) -> None:
        self.app = app

    async def __call__(
            self,
            scope: Scope,
            receive: Receive,
            send: Send
    ) -> None:
        if scope.get('type') != 'http':
            return await self.app(scope, receive, send)

        scope.get('headers').append((b'request_time_server', str(time.time()).encode('utf-8')))
        return await self.app(scope, receive, send)
