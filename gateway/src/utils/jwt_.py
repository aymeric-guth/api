from typing import (
    Dict,
    TypeVar,
    Any
)
import datetime

from fastapi import Header
from starlette.status import (
    HTTP_400_BAD_REQUEST
)

import jwt

from ..config import SECRET_KEY, ALGORITHM, AUTH_HEADER, AUTH_SCHEME, TOKEN_VALIDITY
from ..models import User, UserWithToken
import src.strings as strings
from ..errors import JWTException


T = TypeVar('T', bound='JWTUtil')


class JWTUtil(object):
    secret_key: str = str(SECRET_KEY)
    algorithm: str = ALGORITHM
    auth_header: str = AUTH_HEADER.lower()
    auth_scheme: str = AUTH_SCHEME
    token_validity: int = TOKEN_VALIDITY

    def __init__(self, token: str) -> None:
        self.token: str = token

    @classmethod
    def from_header(cls, headers: Header) -> T:
        auth_header = headers.get(cls.auth_header)
        if auth_header is None:
            raise JWTException(
                message=strings.AUTH_ERROR01,
                status_code=HTTP_400_BAD_REQUEST
            )
        elif auth_header[:7] != (cls.auth_scheme + " "):
            raise JWTException(
                message=strings.AUTH_ERROR02,
                status_code=HTTP_400_BAD_REQUEST
            )
        return cls(auth_header[7:])

    @classmethod
    def from_user(cls, user: User) -> T:
        expires_delta = datetime.timedelta(minutes=cls.token_validity)
        expires_at: datetime.datetime = datetime.datetime.utcnow() + expires_delta
        jwt_content: Dict[str, Any] = {
            "user_id": user.user_id,
            "username": user.username,
            "expires_at": expires_at.isoformat()
        }
        token: str = jwt.encode(jwt_content, cls.secret_key, algorithm=cls.algorithm)
        return cls(token)

    def check(self) -> None:
        try:
            decoded: Dict[str, str] = jwt.decode(
                self.token,
                str(self.secret_key),
                algorithms=[self.algorithm]
            )
        except jwt.exceptions.InvalidSignatureError:
            raise JWTException(
                message=strings.TOKEN_ERROR01,
                status_code=HTTP_400_BAD_REQUEST
            )
        except Exception:
            raise JWTException(
                message=strings.TOKEN_ERROR02,
                status_code=HTTP_400_BAD_REQUEST
            )

        try:
            expires_at: datetime.datetime = datetime.datetime.fromisoformat(decoded.get('expires_at'))
            delta: datetime.timedelta = expires_at - datetime.datetime.utcnow()
        except Exception:
            raise JWTException(
                message=strings.TOKEN_ERROR02,
                status_code=HTTP_400_BAD_REQUEST
            )
        if delta.total_seconds() < 0:
            raise JWTException(
                message=strings.TOKEN_ERROR03,
                status_code=HTTP_400_BAD_REQUEST
            )

    def get_user(self) -> User:
        decoded: Dict[str, str] = jwt.decode(
            self.token,
            str(self.secret_key),
            algorithms=[self.algorithm]
        )
        return User(
            user_id=decoded.get('user_id'),
            username=decoded.get('username')
        )

    def get_user_with_token(self) -> UserWithToken:
        decoded: Dict[str, str] = jwt.decode(
            self.token,
            str(self.secret_key),
            algorithms=[self.algorithm]
        )
        return UserWithToken(
            user_id=decoded.get('user_id'),
            username=decoded.get('username'),
            token=self.token
        )
