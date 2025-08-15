# app/core/security.py
from datetime import datetime
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError   
import os
from app.models.user import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")  
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer(auto_error=True)

def decode_jwt(token: str) -> dict:
    try:
        # jose는 algorithms 파라미터가 list/tuple 가능
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    payload = decode_jwt(creds.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
