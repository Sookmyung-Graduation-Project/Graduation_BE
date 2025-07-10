# app/models/user_favorite_books.py

from beanie import Document, PydanticObjectId
from datetime import datetime

class UserFavoriteBooks(Document):
    book_id: PydanticObjectId
    user_id: PydanticObjectId
    created_at: datetime = datetime.now()

    class Settings:
        name = "user_favorite_books"
