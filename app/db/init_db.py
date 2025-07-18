from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.voice import Voice
from app.models.book import Book
from app.models.user_favorite_books import UserFavoriteBooks
from app.models.user_recent_viewed_books import UserRecentViewedBooks
from app.models.attendance import Attendance
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client["graduation_db"]

async def init_db():
    await init_beanie(
        database=db,
        document_models=[
            User,
            Voice,
            Book,
            UserFavoriteBooks,
            UserRecentViewedBooks,
            Attendance,
        ],
    )
    print(" MongoDB + Beanie 초기화 완료")
