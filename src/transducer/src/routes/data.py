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

from ..repositories.data import DataRepository
from ..dependencies import get_repository
from ..models.data import Transducer
from ..errors import EntityDoesNotExist
from .. import strings


router = APIRouter(tags=["data"], prefix="/data")


@logger.catch
@router.get(
    "",
    status_code=HTTP_200_OK,
    # response_model=Response,
    name="files:get_list"
)
async def get_list(
    *,
    data_repo: DataRepository = Depends(get_repository(DataRepository))
) -> Response:
    try:
        res = await data_repo.get()
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
@router.post(
    "",
    status_code=HTTP_200_OK,
    # response_model=Response,
    name="files:get_list"
)
async def insert(
    *,
    dataset: List[Transducer],
    data_repo: DataRepository = Depends(get_repository(DataRepository))
) -> None:
    try:
        await data_repo.insert(dataset)
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
