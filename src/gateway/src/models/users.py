from pydantic import validator

from ..utils.security import generate_salt, verify_password, get_password_hash
from .base import Base


class User(Base):
    user_id: int
    username: str


class UserWithToken(User):
    token: str


class UserInDB(User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

    def check_username(self, username: str) -> bool:
        return self.username != username


class UserInRequest(Base):
    username: str
    password: str
    salt: str = ""
    hashed_password: str = ""

    @validator('username')
    def check_username(cls, v) -> str:
        if len(v) < 3 or len(v) > 20:
            raise ValueError('user name should be between 3 and 20 ASCII characters')
        return v

    @validator('password')
    def check_password(cls, v) -> str:
        if len(v) < 8:
            raise ValueError('Password should be 8 characters long')
        return v

    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)
