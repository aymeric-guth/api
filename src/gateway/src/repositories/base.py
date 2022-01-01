import pathlib

from asyncpg.connection import Connection
import aiosql


class BaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> Connection:
        return self._conn


queries = aiosql.from_path(pathlib.Path(__file__).parent / 'sql', 'asyncpg')
