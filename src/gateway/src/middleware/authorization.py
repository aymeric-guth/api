from typing import List, Optional
import pickle

from loguru import logger

from ..config import Services
from ..models import User
from ..repositories import AuthorizationRepository
from .common import error_handler, check_path
from .common.types import (
    Scope,
    Receive,
    Send,
    ASGIApp
)


class AuthorizationMiddleware:
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
        send: Send,
    ) -> None:
        if scope.get('type') != 'http':
            return await self.app(scope, receive, send)
        _path: str = scope.get('path')
        if check_path(_path):
            return await self.app(scope, receive, send)

        logger.info('authorization')

        path: List[str] = _path.split('/')
        service_prefix: str = '/' + path[2]
        service_url: Optional[str] = Services.get(service_prefix)

        endpoint_url: str = service_url + '/' + '/'.join(path[3:])
        *_, user_header = scope.get('headers').pop(-1)
        user: User = pickle.loads(user_header)
        scope.get('headers').append((b'endpoint_url', endpoint_url.encode('utf-8')))

        async with scope.get('app').state.pool.acquire() as connection:
            auth_repo: AuthorizationRepository = AuthorizationRepository(connection)
            await auth_repo.check(user_id=user.user_id, service_route=service_prefix)

        return await self.app(scope, receive, send)
