from fastapi import APIRouter

from . import login
from . import register


router = APIRouter(tags=["authentication"], prefix="/authentication")

router.include_router(login.router)
router.include_router(register.router)
