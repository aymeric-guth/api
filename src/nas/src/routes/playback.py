from typing import List
from fastapi import APIRouter, Body, Depends, Path, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from loguru import logger

from ..dependencies import get_repository
from ..models.nas import TCEntry
from ..repositories.playback import PlaybackRepository
from ..errors import EntityDoesNotExist


router = APIRouter(tags=["playback"], prefix="/playback")


@logger.catch
@router.get(
    "",
    status_code=HTTP_200_OK,
    response_model=List[TCEntry],
    name="playback:resume",
)
async def resume(
    *,
    playback_repo: PlaybackRepository = Depends(get_repository(PlaybackRepository))
) -> List[TCEntry]:
    try:
        return await playback_repo.get()
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Resume buffer is empty"
        )
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


@logger.catch
@router.post(
    "",
    status_code=HTTP_200_OK,
    response_model=None,
    name="playback:save"
)
async def save(
    *,
    params: List[TCEntry],
    playback_repo: PlaybackRepository = Depends(get_repository(PlaybackRepository))
) -> None:
    try:
        await playback_repo.save(params=params)
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


@logger.catch
@router.delete(
    "",
    status_code=HTTP_200_OK,
    response_model=None,
    name="playback:reset"
)
async def reset(
    *,
    playback_repo: PlaybackRepository = Depends(get_repository(PlaybackRepository))
) -> None:
    try:
        await playback_repo.reset()
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
