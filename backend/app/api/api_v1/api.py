from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, roles, permissions, config

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
