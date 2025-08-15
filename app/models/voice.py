# app/models/voice.py

from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional

class Voice(Document):
    voice_name: str = "기본 음성"
    voice_id: str
    user_id: PydanticObjectId
    description: Optional[str] = None
    created_at: datetime = datetime.now()

    class Settings:
        name = "voice"
