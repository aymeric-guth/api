from fastapi import APIRouter

from . import data


router = APIRouter()
router.include_router(data.router)
