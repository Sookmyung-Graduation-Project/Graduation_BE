from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
from jose import jwt, JWTError, ExpiredSignatureError

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")

ISSUER = os.getenv("JWT_ISSUER", "your-service") 

def _ts(dt: datetime) -> int:
    return int(dt.timestamp())

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if "sub" in data and not isinstance(data["sub"], str):
        data = data.copy()
        data["sub"] = str(data["sub"])

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=30))

    to_encode = {
        **data,
        "iat": _ts(now),
        "nbf": _ts(now - timedelta(seconds=1)),  
        "exp": _ts(expire),
        "iss": ISSUER,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        issuer=ISSUER,               
        options={"verify_aud": False},
        leeway=60,                    
    )

def debug_print_exp(token: str) -> int:
    """
    주어진 JWT 토큰의 만료(exp)까지 남은 초를 로그로 찍고, 남은 초를 반환.
    """
    claims = jwt.get_unverified_claims(token)
    now = int(datetime.now(timezone.utc).timestamp())
    exp = int(claims["exp"])
    seconds_to_expire = exp - now
    print(f"[DEBUG] seconds_to_expire = {seconds_to_expire}")
    return seconds_to_expire