from typing import Optional
import aiofiles
import aiofiles.ospath
import aiofiles.os
import lsfiles
import os
import shutil
import pickle

from starlette.concurrency import run_in_threadpool
from loguru import logger


from ...models.nas import FileEntry
from ... import strings


class FileServiceError(Exception):
    ...


class FileService:
    def __init__(self):
        ...

    async def delete_file(self, file: str) -> None:
        if not await aiofiles.ospath.exists(file):
            raise FileServiceError(strings.FILES_ERROR03)
        elif not await aiofiles.ospath.isfile(file):
            raise FileServiceError(strings.FILES_ERROR04)
        try:
            await aiofiles.os.remove(file)
        except OSError as err:
            raise FileServiceError(strings.FILES_ERROR05)

    async def delete_dir(self, file: str) -> None:
        try:
            if not await run_in_threadpool(lambda: lsfiles.is_leaf(file)):
                raise FileServiceError(strings.FILES_ERROR09)
        except lsfiles.LSFilesError as err:
            raise FileServiceError(strings.FILES_ERROR07)
        if not await aiofiles.ospath.isdir(file):
            raise FileServiceError(strings.FILES_ERROR08)

        try:
            await run_in_threadpool(lambda: shutil.rmtree(file))
        except OSError as err:
            raise FileServiceError(str(err))


    async def files_on_disk(self) -> list[lsfiles.PathGeneric]:
        files: list[lsfiles.PathGeneric] = await run_in_threadpool(
            lambda: lsfiles.iterativeDFS(
                lsfiles.filters.dotfiles,
                lsfiles.adapters.triplet,
                "/shared"
            )
        )
        if not files:
            raise FileServiceError(strings.FILES_ERROR01)
        return files

    async def cache_get(self) -> Optional[str]:
        try:
            async with aiofiles.open('./cache.pckl', mode='r') as f:
                return await f.read()
        except Exception:
            logger.exception('Exception occured while reading cache')
            return None

    async def cache_set(self, data: str) -> None:
        try:
            async with aiofiles.open('./cache.pckl', mode='w') as f:
                await f.write(data)
        except Exception:
            logger.exception('Exception occured while updating cache')
            return None

    async def cache_invalidate(self) -> None:
        return await self.cache_set('')
