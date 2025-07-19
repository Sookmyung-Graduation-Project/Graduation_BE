from fastapi import APIRouter
from app.api.v1.endpoints.auth import kakao_auth
from app.routers import system

v1_router = APIRouter()

# /login/kakao 경로와 /system 경로를 포함
v1_router.include_router(kakao_auth.router, tags=["auth"])
v1_router.include_router(system.router, tags=["system"])
