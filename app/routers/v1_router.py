from fastapi import APIRouter
from app.api.v1.endpoints.auth import kakao_auth
from app.routers import system  

v1_router = APIRouter()

v1_router.include_router(kakao_auth.router, prefix="/login", tags=["auth"])
v1_router.include_router(system.router, tags=["system"])
