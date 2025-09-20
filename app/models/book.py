# app/models/book.py

from beanie import Document, PydanticObjectId
from typing import List, Optional
from datetime import datetime


class Book(Document):
    user_id: PydanticObjectId
    book_title: str
    book_author: str
    book_contents: str
    age: int
    
    # 새로 추가된 필드들
    gender: Optional[str] = None
    age_group: Optional[str] = None
    lesson: Optional[str] = None
    animal: Optional[str] = None
    voice_option: Optional[str] = None
    
    # 생성된 동화 내용
    pages: Optional[List[str]] = None
    summary: Optional[str] = None
    characters: Optional[List[str]] = None
    setting: Optional[str] = None
    
    # 메타데이터
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "book"
