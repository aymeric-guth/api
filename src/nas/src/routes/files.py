from typing import List, Callable, Any

# from asyncpg import Record
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)

from loguru import logger
import orjson

from ..repositories.files import FileRepository
from ..models.nas import FileEntry
from ..dependencies import get_repository
from ..errors import EntityDoesNotExist
from .. import strings
from ..utils import lsfiles, timer, introspector


router = APIRouter(tags=["files"], prefix="/files")


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
    try:
        res = await file_repo.get()
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
    "",
    status_code=HTTP_200_OK,
    # response_model=None,
    name="files:reindex"
)
async def reindex(
    *,
    file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> None:
    files_list: List[Any] = lsfiles.lsfiles(fnc=lsfiles.filter_none)("/shared")
    if not files_list:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.FILES_ERROR01
        )
    try:
        await file_repo.set(files_list=files_list)
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Exception occured while updating database'
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
