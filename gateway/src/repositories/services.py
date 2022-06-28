from starlette.status import HTTP_403_FORBIDDEN

from asyncpg import Record

from .base import BaseRepository, queries
from ..errors import MiddlewareException, EntityDoesNotExist


class ServiceRepository(BaseRepository):
    async def by_id(
        self,
        *,
        service_id: int
    ) -> None:
        rows: Record = await queries.services.by_id(
            self.connection,
            service_id=service_id
        )
        if not rows:
            raise EntityDoesNotExist
