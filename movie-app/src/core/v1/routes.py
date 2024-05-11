from fastapi import APIRouter
from v1.users import router as users_router

# from v1.auth import router as login_router

api_router = APIRouter()
# api_router.include_router(login_router.router, tags=["login"])
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
