# app/models/book.py

from beanie import Document, PydanticObjectId


class Book(Document):
    user_id: PydanticObjectId
    book_title: str
    book_author: str
    book_contents: str
    age: int

    class Settings:
        name = "book"
