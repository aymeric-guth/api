import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from loguru import logger


router = APIRouter(prefix="/latency")


@logger.catch
@router.get(
    "/",
    status_code=200,
    response_model=None,
    name="latency:get"
)
async def get(
    request_time_client: float,
    request: Request
) -> JSONResponse:
    return JSONResponse(
        content={
            'request_time_client': request_time_client,
            'request_time_server': request.headers.get('request_time_server'),
            'response_time_server': time.time()
        }
    )
