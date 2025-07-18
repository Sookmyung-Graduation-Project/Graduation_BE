# app/models/attendance.py

from beanie import Document, PydanticObjectId
from datetime import datetime, date

class Attendance(Document):
    user_id: PydanticObjectId
    date: date
    created_at: datetime = datetime.now()
    is_present: bool = False
    consecutive_days: int = 0

    class Settings:
        name = "attendance"
