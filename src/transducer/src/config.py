import sys
import logging
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from .utils.logging import InterceptHandler


config = Config(".env")

API_PREFIX: str = config("API_PREFIX", cast=str)
VERSION: str = config("VERSION", cast=str, default="v0.0.1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

DB_USER: str = config("DB_USER", cast=str)
DB_PASSWORD: str = config("DB_PASSWORD", cast=str)
DB_HOST: str = config("DB_HOST", cast=str)
DB_PORT: str = config("DB_PORT", cast=str)
DB_NAME: str = config("DB_NAME", cast=str)
DATABASE_URL: str = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int)

PROJECT_NAME: str = config("PROJECT_NAME")
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
