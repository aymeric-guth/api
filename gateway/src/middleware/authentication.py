from typing import Dict
import pickle

from loguru import logger

from ..repositories import UserRepository
from ..utils.jwt_ import JWTUtil
from ..models import User
from .common.types import Scope, Receive, Send, ASGIApp
from .common import parse_headers, error_handler, check_path


# https://github.com/abersheeran/asgi-ratelimit/blob/master/ratelimit/core.py
class AuthenticationMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @error_handler
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        if check_path(scope.get("path")):
            return await self.app(scope, receive, send)

        logger.info("authentication")

        headers: Dict[str, str] = parse_headers(scope.get("headers"))
        jwt_user = JWTUtil.from_header(headers)
        jwt_user.check()
        user: User = jwt_user.get_user()

        async with scope.get("app").state.pool.acquire() as connection:
            user_repo: UserRepository = UserRepository(connection)
            await user_repo.check(user=user)
        scope.get("headers").append((b"user", pickle.dumps(user)))

        return await self.app(scope, receive, send)
