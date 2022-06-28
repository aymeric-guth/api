from typing import Callable
from functools import wraps
import time

from loguru import logger


def timer(fnc: Callable):
    @wraps(fnc)
    async def inner(*args, **kwargs):
        start = time.time()
        res = await fnc(*args, **kwargs)
        logger.info(f'{fnc.__name__}: {time.time()-start}')
        return res
    return inner
