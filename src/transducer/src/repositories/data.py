import json
from typing import List, Any, Generator, Tuple

from asyncpg import Record
import asyncpg
from loguru import logger

from .base import BaseRepository
from ..errors import EntityDoesNotExist
from ..models.data import Transducer
from . import queries


class DataRepository(BaseRepository):
    async def get(self) -> List[Any]:
        rows: List[Any] = await queries.data.get(self.connection)
        if not rows:
            raise EntityDoesNotExist
        return rows

    async def insert(self, dataset: List[Transducer]) -> None:
        parsed = [
            (
                val.transducer_id,
                val.created_at,
                val.status,
                val.cause,
                val.mode,
                val.frequency,
                val.pe,
                val.ps,
                val.minutes,
                val.vah,
                val.temperature
            )
            for val in dataset
        ]

        async with self.connection.transaction():
            await self.connection.copy_records_to_table(
                table_name='model',
                columns=[
                    'transducer_id',
                    'created_at',
                    'status',
                    'cause',
                    'mode',
                    'frequency',
                    'pe',
                    'ps',
                    'minutes',
                    'vah',
                    'temperature'
                ],
                records=parsed
            )
