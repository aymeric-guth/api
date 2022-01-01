from starlette.status import HTTP_403_FORBIDDEN

from asyncpg import Record
from loguru import logger

from .base import BaseRepository, queries
from ..errors import MiddlewareException, EntityDoesNotExist


class AuthorizationRepository(BaseRepository):
    async def check(
        self,
        *,
        user_id: int,
        service_route: str
    ) -> None:
        rows: Record = await queries.authorizations.check(
            self.connection,
            user_id=user_id,
            service_route=service_route
        )
        if not rows:
            raise MiddlewareException(
                message='You are not allowed to use this service',
                status_code=HTTP_403_FORBIDDEN
            )

    async def check_delegate(
        self,
        *,
        user_id: int,
        service_id: int
    ) -> None:
        rows: Record = await queries.authorizations.check_delegate(
            self.connection,
            user_id=user_id,
            service_id=service_id
        )
        if not rows:
            raise EntityDoesNotExist

    async def create(
        self,
        *,
        user_id: int,
        service_id: int
    ) -> None:
        await queries.authorizations.create(
            self.connection,
            user_id=user_id,
            service_id=service_id
        )

    async def delete(
        self,
        *,
        user_id: int,
        service_id: int
    ) -> None:
        logger.info(f'executing query with parameters ({user_id=}, {service_id=})')
        await queries.authorizations.delete(
            self.connection,
            user_id=user_id,
            service_id=service_id
        )
