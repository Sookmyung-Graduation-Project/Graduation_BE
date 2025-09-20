import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB 설정
    mongo_url: str = "mongodb://localhost:27017"
    database_name: str = "graduation_db"

    # JWT 설정
    jwt_secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Kakao OAuth 설정
    kakao_client_id: Optional[str] = None
    kakao_client_secret: Optional[str] = None
    kakao_redirect_uri: Optional[str] = None

    # ChatGPT API 설정
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.8

    # ElevenLabs 설정
    elevenlabs_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
