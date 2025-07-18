from fastapi import FastAPI
from app.api.v1.endpoints.auth import kakao_auth
from app.routers import system
from app.routers.v1_router import v1_router
from app.db import init_db
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()

app.include_router(kakao_auth.router, prefix="/login", tags=["auth"])
app.include_router(system.router, tags=["system"])
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello Graduation_BE"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
