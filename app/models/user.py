# app/models/user.py
from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document, PydanticObjectId, before_event
from beanie.odm.actions import Insert, Replace
from pydantic import EmailStr, Field

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
    user_role: UserRole = UserRole.parent
    child_age: Optional[int] = None
    default_voice_id: Optional[PydanticObjectId] = None

    # 타임스탬프 (UTC)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            [("provider", 1), ("provider_user_id", 1)],
            # email unique+sparse는 init 단계에서 보강 권장
        ]

    # 저장/수정 전 updated_at 자동 갱신
    @before_event([Insert, Replace])
    def _touch_updated_at(self):
        self.updated_at = datetime.utcnow()
