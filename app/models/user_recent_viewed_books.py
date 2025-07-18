# app/models/user_recent_viewed_books.py

from beanie import Document, PydanticObjectId
from datetime import datetime

class UserRecentViewedBooks(Document):
    book_id: PydanticObjectId
    user_id: PydanticObjectId
    created_at: datetime = datetime.now()

    class Settings:
        name = "user_recent_viewed_books"
