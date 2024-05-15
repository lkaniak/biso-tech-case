from fastapi import APIRouter
from api.core.v1.users import router as users_router
from api.core.v1.auth import router as login_router
from api.core.v1.recommendation import router as recommendation_router


api_router = APIRouter()
api_router.include_router(login_router.router, tags=["login"])
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
api_router.include_router(
    recommendation_router.router, prefix="/recommend", tags=["recommend"]
)
