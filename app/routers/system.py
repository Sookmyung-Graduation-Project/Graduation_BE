from fastapi import APIRouter
from app.db.mongo import db  # 이미 초기화된 db를 import하면 됨

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello from FastAPI + MongoDB Atlas!"}

@router.get("/test")
async def test():
    collection = db["test_collection"]
    document = await collection.find_one({})
    if document:
        document["_id"] = str(document["_id"])
    return {"document": document}
