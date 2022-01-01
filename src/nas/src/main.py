from asyncpg import create_pool
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware import cors, gzip
from loguru import logger

from .errors import http_error_handler, http422_error_handler
from .routes import router as api_router
from .config import (
    ALLOWED_HOSTS, 
    API_PREFIX, 
    DEBUG, 
    PROJECT_NAME, 
    VERSION, 
    DATABASE_URL, 
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT
)


app: FastAPI = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

# app.add_middleware(gzip.GZipMiddleware, minimum_size=500)
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.include_router(api_router, prefix=API_PREFIX)


@logger.catch
@app.on_event("startup")
async def start_app() -> None:
    logger.info("Connecting to database")
    app.state.pool = await create_pool(
        DATABASE_URL,
        min_size=MIN_CONNECTIONS_COUNT,
        max_size=MAX_CONNECTIONS_COUNT,
    )
    logger.info("Connection established")


@logger.catch
@app.on_event("shutdown")
async def stop_app() -> None:
    logger.info("Closing connection to database")
    await app.state.pool.close()
    logger.info("Connection closed")
