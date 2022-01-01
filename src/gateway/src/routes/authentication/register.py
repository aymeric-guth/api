from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from loguru import logger

from ...dependencies import get_repository
from ...utils.jwt_ import JWTUtil
from ...repositories import UserRepository
from ...errors import EntityDoesNotExist
from ...models import (
    UserInRequest,
    UserWithToken,
    User
)
from ... import strings


router = APIRouter(prefix="/register")


@logger.catch
@router.post(
    "", 
    status_code=HTTP_201_CREATED, 
    response_model=UserWithToken, 
    name="auth:register"
)
async def register(
    user: UserInRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository))
) -> UserWithToken:
    try:
        await user_repo.get_by_username(username=user.username)
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR05
        )
    userJwt: User = await user_repo.create(user=user)
    return JWTUtil.from_user(userJwt).get_user_with_token()
