from typing import List

from fastapi import APIRouter, Body, Depends, Path, HTTPException
from loguru import logger
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK
)

from ..errors import EntityDoesNotExist
from ..strings import Extensions
from ..dependencies import get_repository
from ..repositories.extensions import ExtensionRepository


router = APIRouter(tags=["extensions"], prefix="/extensions")


@logger.catch
@router.get(
    "",
    status_code=HTTP_200_OK,
    response_model=List[str],
    name="extensions:get"
)
async def get_extensions(
    *,
    extRepo: ExtensionRepository = Depends(get_repository(ExtensionRepository)),
) -> List[str]:
    try:
        return await extRepo.get()
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=Extensions.ERROR01
        )


@logger.catch
@router.patch(
    "",
    status_code=HTTP_200_OK,
    response_model=None,
    name="extensions:set"
)
async def set_extensions(
    *,
    extensions: List[str],
    extRepo: ExtensionRepository = Depends(get_repository(ExtensionRepository)),
) -> None:
    try:
        await extRepo.set(extensions=set(extensions))
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Extensions.ERROR01
        )
