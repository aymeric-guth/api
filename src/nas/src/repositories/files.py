import json
from typing import List, Any, Generator, Tuple

from asyncpg import Record
import asyncpg
from loguru import logger

from .base import BaseRepository
from ..errors import EntityDoesNotExist
from . import queries
from ..models.nas import FileEntry
from ..utils import timer


class FileRepository(BaseRepository):
    async def get(self) -> str:
        return await queries.files.get_json(self.connection)

    async def set(self, *, files_list: List[Any]) -> None:
        async with self.connection.transaction():
            await queries.files.reset(self.connection)
            await self.connection.copy_records_to_table(
                table_name='files',
                records=files_list,
                columns=['path', 'filename', 'extension']
            )

    async def delete(self) -> None:
        await queries.files.reset(self.connection)
