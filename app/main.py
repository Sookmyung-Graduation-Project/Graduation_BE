from fastapi import FastAPI
from app.api.v1.endpoints.auth import kakao_auth
from app.routers import system

app = FastAPI()

app.include_router(kakao_auth.router, prefix="/login", tags=["auth"])
app.include_router(system.router, tags=["system"])
