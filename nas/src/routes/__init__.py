from fastapi import APIRouter

from . import files
from . import extensions
from . import playback
from . import caches
from . import purge


router = APIRouter()
router.include_router(files.router)
router.include_router(extensions.router)
router.include_router(playback.router)
router.include_router(caches.router)
router.include_router(purge.router)
