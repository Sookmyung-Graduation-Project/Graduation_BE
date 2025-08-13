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
    # 로그인 제공자 정보
    provider: LoginType
    provider_user_id: str  # 카카오 id, 구글 sub 등

    # 공통 프로필 
    nickname: str
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None

    # 앱 전용 필드
    user_role: UserRole = UserRole.parent # 기본값을 학부모로 설정
    child_age: Optional[int] = None
    default_voice_id: Optional[PydanticObjectId] = None

    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "users"
        # (provider, provider_user_id) 복합 유니크 인덱스 권장
        indexes = [
            [("provider", 1), ("provider_user_id", 1)],
            # 이메일은 제공 동의 범위에 따라 없을 수 있으므로 sparse 유니크
            {"fields": [("email", 1)], "unique": True, "sparse": True},
        ]