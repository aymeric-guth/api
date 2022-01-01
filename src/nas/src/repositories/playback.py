from typing import List, Any, Tuple

from asyncpg import Record
from loguru import logger

from . import queries
from .base import BaseRepository
from ..errors import EntityDoesNotExist
from ..models.nas import TCEntry


class PlaybackRepository(BaseRepository):
    async def get(self) -> List[TCEntry]:
        rows: List[Record] = await queries.playback.get(self.connection)
        if not rows:
            raise EntityDoesNotExist
        return [TCEntry(**i) for i in rows]

    async def save(self, *, params: List[TCEntry]) -> None:
        async with self.connection.transaction():
            await queries.playback.reset(self.connection)
            await self.connection.copy_records_to_table(
                table_name='playback',
                records=(i.tuple() for i in params),
                columns=['path', 'filename', 'extension', 'tc']
            )

    async def reset(self) -> None:
        await queries.playback.reset(self.connection)
