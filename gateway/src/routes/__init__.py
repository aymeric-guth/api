from fastapi import APIRouter

from . import authentication
from . import users
from . import authorizations
from . import latency


router = APIRouter()

router.include_router(authentication.router)
router.include_router(users.router)
router.include_router(authorizations.router)
router.include_router(latency.router)
