# app/models/user.py
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    parent = "parent"
    child = "child"

class LoginType(str, Enum):
    google = "google"
    kakao = "kakao"

class User(Document):
    username: str
    user_role: Optional[UserRole]
    child_age: Optional[int]
    email: EmailStr
    login_type: Optional[LoginType]
    default_voice_id: Optional[PydanticObjectId]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "user"  # collection name
