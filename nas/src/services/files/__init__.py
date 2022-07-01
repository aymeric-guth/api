import aiofiles
import aiofiles.ospath
import aiofiles.os
import lsfiles
import os
import shutil

from starlette.concurrency import run_in_threadpool

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
