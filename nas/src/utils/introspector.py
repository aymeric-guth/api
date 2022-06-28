from typing import Callable
from functools import wraps

from loguru import logger


def introspector(fnc: Callable):
    @wraps(fnc)
    def inner(*args, **kwargs):
        try:
            logger.info(fnc.__name__)
        except AttributeError:
            pass
        return fnc(*args, **kwargs)
    return inner
