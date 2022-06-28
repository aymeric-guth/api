import sys
import logging
from typing import List, Dict, Optional, Set

from starlette.config import Config
from starlette.status import HTTP_404_NOT_FOUND
from starlette.datastructures import CommaSeparatedStrings, Secret

from asyncpg import Record
from loguru import logger

from .errors import MiddlewareException
from .utils.logging import InterceptHandler


config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME")
API_PREFIX: str = "/api"
VERSION: str = config("DEBUG", cast=str, default="v0.0.1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

DB_USER: str = config("DB_USER", cast=str)
DB_PASSWORD: str = config("DB_PASSWORD", cast=str)
DB_HOST: str = config("DB_HOST", cast=str)
DB_PORT: str = config("DB_PORT", cast=str)
DB_NAME: str = config("DB_NAME", cast=str)
DATABASE_URL: str = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
ALGORITHM: str = config("ALGORITHM", cast=str)
AUTH_HEADER: str = config("AUTH_HEADER", cast=str)
AUTH_SCHEME: str = config("AUTH_SCHEME", cast=str)
TOKEN_VALIDITY: int = 60 * 24 * 14

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]


# logger.configure(handlers=[{"sink": "/logs/app.log", "level": LOGGING_LEVEL}])
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])


# SERVICES
class SERVICES(object):
    BASE: str = 'http://{}:8080'
    AUTHENTICATION: str = f'{API_PREFIX}/authentication'
    USERS: str = f'{API_PREFIX}/users'
    AUTHORIZATIONS: str = f'{API_PREFIX}/authorizations'
    LATENCY: str = f'{API_PREFIX}/latency'
    DOCS: str = f'{API_PREFIX}/docs'
    PATTERN: str = f'{AUTHENTICATION}.*|{AUTHORIZATIONS}.*|{USERS}.*|{LATENCY}.*|{DOCS}.*'

    NAS_IP: str = config('IP_NAS', cast=str)
    NAS: str = config('PREFIX_NAS', cast=str)
    NAS_BASE: str = f'{BASE.format(NAS_IP)}{NAS}'

    _services: Dict[str, str] = {
        NAS: NAS_BASE,
    }

    def get(self, value) -> Optional[str]:
        try:
            return SERVICES._services[value]
        except KeyError as err:
            raise MiddlewareException(
                message='Unknown service',
                status_code=HTTP_404_NOT_FOUND
            )

    def __contains__(self, value) -> bool:
        return value in SERVICES._services

    def __eq__(self, other: Record) -> bool:
        for i, *_ in other:
            logger.info(i)
            if i not in self:
                return False
        return True


Services: SERVICES = SERVICES()
