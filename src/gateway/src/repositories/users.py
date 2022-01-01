from starlette.status import HTTP_403_FORBIDDEN

from asyncpg import Record

from ..models import User, UserInRequest, UserInDB
from ..errors import EntityDoesNotExist, MiddlewareException
from .base import BaseRepository, queries


class UserRepository(BaseRepository):
    async def by_id(self, *, user_id: int) -> UserInDB:
        rows: Record = await queries.users.by_id(self.connection, user_id=user_id)
        if rows:
            return UserInDB(**rows)
        raise EntityDoesNotExist

    async def get_by_username(self, *, username: str) -> UserInDB:
        rows: Record = await queries.users.get_by_username(self.connection, username=username)
        if rows:
            return UserInDB(**rows)
        raise EntityDoesNotExist

    async def check(self, *, user: User) -> None:
        rows: Record = await queries.users.check(
            self.connection,
            user_id=user.user_id,
            username=user.username
        )
        if not rows:
            raise MiddlewareException(
                message=f'User {user.username} does not exists',
                status_code=HTTP_403_FORBIDDEN
            )

    async def create(self, *, user: UserInRequest) -> User:
        user.change_password(user.password)
        rows: Record = await queries.users.create(
            self.connection,
            username=user.username,
            salt=user.salt,
            hashed_password=user.hashed_password,
        )
        return User(**rows)

    async def delete(self, *, user: User) -> None:
        await queries.users.delete(
            self.connection,
            user_id=user.user_id,
            username=user.username
        )
