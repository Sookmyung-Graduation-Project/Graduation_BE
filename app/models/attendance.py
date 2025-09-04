# app/models/attendance.py

from beanie import Document, PydanticObjectId
from datetime import datetime
from pydantic import Field

class Attendance(Document):
    user_id: PydanticObjectId
    # 출석 기록 시각(UTC). 동일 일자 비교는 서버에서 일자 범위를 사용
    date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_present: bool = False

    class Settings:
        name = "attendance"
