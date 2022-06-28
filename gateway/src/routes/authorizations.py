from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from loguru import logger

from ..dependencies import get_repository
from ..repositories import UserRepository, AuthorizationRepository, ServiceRepository
from ..errors import EntityDoesNotExist
from ..models import AuthInRequest


router = APIRouter(prefix="/authorizations")


# authorizations check sur le middleware
@logger.catch
@router.post(
    "",
    status_code=201,
    response_model=None,
    name="authorizations:create"
)
async def create_authorization(
    auth: AuthInRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    service_repo: ServiceRepository = Depends(get_repository(ServiceRepository)),
    auth_repo: AuthorizationRepository = Depends(get_repository(AuthorizationRepository))
) -> None:
    try:
        await user_repo.by_id(user_id=auth.user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This user does not exist'
        )
    try:
        await service_repo.by_id(service_id=auth.service_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This service does not exist'
        )
    try:
        await auth_repo.check_delegate(user_id=auth.user_id, service_id=auth.service_id)
    except EntityDoesNotExist:
        await auth_repo.create(user_id=auth.user_id, service_id=auth.service_id)
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This authorization already exists'
        )


# authorizations check sur le middleware
@logger.catch
@router.delete(
    "",
    status_code=200,
    response_model=None,
    name="authorizations:delete"
)
async def delete_authorization(
    auth: AuthInRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    service_repo: ServiceRepository = Depends(get_repository(ServiceRepository)),
    auth_repo: AuthorizationRepository = Depends(get_repository(AuthorizationRepository))
) -> None:
    try:
        await user_repo.by_id(user_id=auth.user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This user does not exist'
        )
    try:
        await service_repo.by_id(service_id=auth.service_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This service does not exist'
        )
    try:
        await auth_repo.check_delegate(user_id=auth.user_id, service_id=auth.service_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='This authorization does not exist'
        )
    else:
        await auth_repo.delete(user_id=auth.user_id, service_id=auth.service_id)
