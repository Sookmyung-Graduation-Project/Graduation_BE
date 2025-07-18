# app/models/voice.py

from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import Optional

class Voice(Document):
    voice_name: str = "기본 음성"
    user_id: PydanticObjectId
    created_at: datetime = datetime.now()

    class Settings:
        name = "voice"
