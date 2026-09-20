from fastapi import APIRouter

from .tests import qwiz_router
from .users import users_router
from .attempts import attempts_router
from .groups import groups_router

api_router = APIRouter()
api_router.include_router(qwiz_router)
api_router.include_router(users_router)
api_router.include_router(attempts_router)
api_router.include_router(groups_router)
