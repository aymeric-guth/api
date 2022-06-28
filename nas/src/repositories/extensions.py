from typing import List, Set

from asyncpg import Record
from loguru import logger

from . import queries
from .base import BaseRepository
from ..errors import EntityDoesNotExist


class ExtensionRepository(BaseRepository):
    async def get(self) -> List[str]:
        rows: List[Record] = await queries.extensions.get(self.connection)
        if not rows:
            raise EntityDoesNotExist()
        return [i[0] for i in rows]

    async def set(self, *, extensions: Set[str]) -> None:
        async with self.connection.transaction():
            await queries.extensions.reset(self.connection)
            await self.connection.copy_records_to_table(
                'extensions',
                records=((i,) for i in extensions),
                columns=['name']
            )
