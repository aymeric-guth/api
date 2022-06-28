from typing import List, Callable, Any
import time
from fastapi import APIRouter, Body, Depends, Path, HTTPException
from starlette.status import HTTP_200_OK
from loguru import logger

from ..repositories.files import FileRepository
from ..dependencies import get_repository


router = APIRouter(tags=["caches"], prefix="/caches")


@logger.catch
@router.get(
    "",
    status_code=HTTP_200_OK,
    response_model=None,
    name="files:get_list"
)
async def get_cache(
        *,
        file_repo: FileRepository = Depends(get_repository(FileRepository))
) -> None:
    start = time.time()
    await file_repo.get()
    logger.info(time.time()-start)
