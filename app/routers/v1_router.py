from fastapi import APIRouter
from app.api.v1.endpoints.auth import kakao_auth
from app.api.v1.endpoints import voice 

v1_router = APIRouter()

# /login/kakao 경로와 /voice 경로를 포함
v1_router.include_router(kakao_auth.router, tags=["auth"])
v1_router.include_router(voice.router, prefix="/voice", tags=["voice"])