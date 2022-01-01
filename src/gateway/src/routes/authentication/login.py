from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from loguru import logger

from ...dependencies import get_repository
from ...utils.jwt_ import JWTUtil
from ...repositories import UserRepository
from ...errors import EntityDoesNotExist
from ...models import (
    UserInRequest,
    UserWithToken,
    UserInDB
)
from ... import strings


router = APIRouter(prefix="/login")


@logger.catch
@router.post(
    "",
    response_model=UserWithToken, 
    name="auth:login"
)
async def login(
    user_login: UserInRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserWithToken:
    try:
        user: UserInDB = await user_repo.get_by_username(username=user_login.username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR01
        )
    if not user.check_password(user_login.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR02
        )
    jwt_user: JWTUtil = JWTUtil.from_user(user)
    return jwt_user.get_user_with_token()
