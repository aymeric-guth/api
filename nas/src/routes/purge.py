import asyncio
import pathlib
from typing import List, Callable, Any

# from asyncpg import Record
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
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
from ..services import FileService, FileServiceError


router = APIRouter(tags=["purge"], prefix="/purge")


@logger.catch
@router.delete(
    "/file",
    status_code=HTTP_200_OK,
    response_model=None,
    name="purge:delete-file"
)
async def delete_file(
    *,
    file: FileEntry,
    file_repo: FileRepository = Depends(get_repository(FileRepository)),
    file_service: FileService = Depends(FileService)
) -> None:
    try:
        await file_repo.get_one(file=file)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR02
        )
    try:
        await file_service.delete_file(str(file))
    except FileServiceError as err:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    await file_repo.delete_one(file=file)


@logger.catch
@router.delete(
    "/dir",
    status_code=HTTP_200_OK,
    response_model=None,
    name="purge:delete-dir"
)
async def delete_dir(
    *,
    file: FileEntry,
    file_repo: FileRepository = Depends(get_repository(FileRepository)),
    file_service: FileService = Depends(FileService)
) -> None:
    if file.filename != '' or file.extension != '':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.FILES_ERROR08
        )
    try:
        await file_repo.get_dir(file=file)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR02
        )
    try:
        await file_service.delete_dir(str(file))
    except FileServiceError as err:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    await file_repo.delete_path(file=file)
