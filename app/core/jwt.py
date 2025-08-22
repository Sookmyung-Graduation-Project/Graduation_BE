from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt
import os

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")

ISSUER = os.getenv("JWT_ISSUER", "your-service")  # 선택

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    # sub는 문자열 권장
    if "sub" in data and not isinstance(data["sub"], str):
        data = data.copy()
        data["sub"] = str(data["sub"])

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=30))

    to_encode = {
        **data,
        "iat": now,
        "nbf": now,        
        "exp": expire,
        "iss": ISSUER,     
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
