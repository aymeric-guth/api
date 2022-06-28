import asyncio
import pathlib
from typing import List, Callable, Any

# from asyncpg import Record
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from starlette.concurrency import run_in_threadpool


from loguru import logger
import av

import aiofiles
import pickle

from ..repositories.files import FileRepository
from ..models.nas import FileEntry
from ..dependencies import get_repository
from ..errors import EntityDoesNotExist
from .. import strings
from ..utils import lsfiles, timer, introspector


router = APIRouter(tags=["files"], prefix="/files")


async def cache_get():
    try:
        async with aiofiles.open('./cache.pckl', mode='rb') as f:
            return await pickle.load(f)
    except Exception:
        return None


async def cache_set(data):
    try:
        async with aiofiles.open('./cache.pckl', mode='wb') as f:
            await pickle.dump(data, f)
    except Exception:
        return None


@logger.catch
@router.get(
    "",
    status_code=HTTP_200_OK,
    # response_model=Response,
    name="files:get_list"
)
async def get_list(
    *,
    file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> Response:
    res = await cache_get()
    if res is not None:
        return Response(
            status_code=HTTP_200_OK,
            media_type='application/json',
            content=res
        )
    try:
        res = await file_repo.get()
        await cache_set(res)
        return Response(
            status_code=HTTP_200_OK,
            media_type='application/json',
            content=res
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR01
        )


@logger.catch
@router.patch(
    '',
    status_code=HTTP_200_OK,
    # response_model=None,
    name="files:reindex"
)
async def reindex(
    *,
    file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> None:
    files: list[lsfiles.PathGeneric] = await run_in_threadpool(
        lambda: lsfiles.iterativeDFS(
            lsfiles.filters.dotfiles,
            lsfiles.adapters.triplet,
            "/shared"
        )
    )
    if not files:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR01
        )
    try:
        await file_repo.set(files_list=files)
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Exception occured while updating database'
        )
    try:
        res = await file_repo.get()
        await cache_set(res)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR01
        )


@logger.catch
@router.delete(
    "",
    status_code=HTTP_204_NO_CONTENT,
    response_model=None,
    name="files:delete"
)
async def delete(
    *,
    file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> None:
    try:
        await file_repo.delete()
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR01
        )


def datagen(path: pathlib.Path):
    def inner():
        nonlocal path

        input_ = av.open(str(path))
        in_stream = input_.streams.audio[0]

        for packet in input_.demux(in_stream):
            # We need to skip the "flushing" packets that `demux` generates.
            if packet.dts is None:
                continue
            data = bytes(packet)
            yield data
    return inner


def _datagen(path):
    input_ = av.open(str(path))
    in_stream = input_.streams.audio[0]

    for packet in input_.demux(in_stream):
        # We need to skip the "flushing" packets that `demux` generates.
        if packet.dts is None:
            continue
        data = bytes(packet)
        yield data


@logger.catch
@router.post(
    '',
    status_code=HTTP_200_OK,
    # response_model=StreamingResponse,
    name="files:get"
)
async def get_file(
    *,
    file: FileEntry,
    file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> StreamingResponse:
    try:
        res = await file_repo.get_one(file=file)
    except EntityDoesNotExist as err:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='File does not exist'
        )
    gen = _datagen(pathlib.Path(f'{res.path}{res.filename}{res.extension}'))
    return StreamingResponse(
        gen,
        media_type='audio/opus'
    )
