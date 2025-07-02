from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")


# MongoDB 클라이언트 초기화
client = AsyncIOMotorClient(MONGO_URL)
db = client.test  # 사용할 DB 이름 (필요에 따라 변경 가능)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + MongoDB Atlas!"}

@app.get("/test")
async def test():
    collection = db["test_collection"]
    document = await collection.find_one({})
    if document:
        document["_id"] = str(document["_id"])  # ObjectId 변환
    return {"document": document}
