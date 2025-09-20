from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from fastapi import FastAPI
from app.api.v1.endpoints.auth import kakao_auth
from app.db.init_db import init_db
from app.api.v1.endpoints import voice
from app.api.v1.endpoints import attendance
from app.api.v1.endpoints import get_user_info
from app.routers import book_generation

import uvicorn

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await init_db()

# 직접 경로 포함
app.include_router(kakao_auth.router, prefix="/login", tags=["auth"])
app.include_router(voice.router, prefix="/voice", tags=["voice"])
app.include_router(get_user_info.router, tags=["user"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(book_generation.router, prefix="/book_generation", tags=["book-generation"]) 



@app.get("/")
async def root():
    return {"message": "Hello Graduation_BE"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
