import os
from typing import Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(dotenv_path=".env")

class Settings:
    # MongoDB 설정
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "graduation_db")

    # JWT 설정
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Kakao OAuth 설정
    kakao_client_id: Optional[str] = os.getenv("KAKAO_CLIENT_ID")
    kakao_client_secret: Optional[str] = os.getenv("KAKAO_CLIENT_SECRET")
    kakao_redirect_uri: Optional[str] = os.getenv("KAKAO_REDIRECT_URI")

    # OpenAI 설정
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", 2000))
    openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", 0.8))

    # ElevenLabs 설정
    elevenlabs_api_key: Optional[str] = os.getenv("ELEVENLABS_API_KEY")


settings = Settings()
