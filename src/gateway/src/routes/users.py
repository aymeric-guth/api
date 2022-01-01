from fastapi import APIRouter, Depends, HTTPException, Path
from starlette.status import HTTP_404_NOT_FOUND

from loguru import logger

from ..dependencies import get_repository
from ..repositories import UserRepository
from ..models import User
from ..errors import EntityDoesNotExist


router = APIRouter(prefix="/users")


# authorisations nécessaires
@logger.catch
@router.delete(
    "",
    status_code=200,
    response_model=None,
    name="users:delete"
)
async def delete_user(
    user: User,
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> None:
    await user_repo.delete(user=user)


# authorisations nécessaires
@logger.catch
@router.get(
    "/",
    status_code=200,
    response_model=User,
    name="users:get"
)
async def get_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> User:
    logger.info(user_id)
    try:
        return await user_repo.by_id(user_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='User does not exists'
        )
