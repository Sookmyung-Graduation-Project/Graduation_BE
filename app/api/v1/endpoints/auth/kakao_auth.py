from fastapi import APIRouter, HTTPException
import httpx
from datetime import timedelta

from app.core.jwt import create_access_token
from app.schemas.auth import KakaoLoginRequest, KakaoLoginResponse
from app.db.mongo import db

router = APIRouter()
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

@router.post("/kakao", response_model=KakaoLoginResponse)
async def kakao_login(body: KakaoLoginRequest):
    kakao_access_token = body.access_token

    headers = {"Authorization": f"Bearer {kakao_access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(KAKAO_USER_INFO_URL, headers=headers)

        print(f"Kakao /v2/user/me status: {response.status_code}")
        print(f"Kakao /v2/user/me response: {response.json()}")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Kakao token")

    kakao_user = response.json()
    kakao_id = str(kakao_user["id"])
    nickname = kakao_user["properties"]["nickname"]

    user = await db["users"].find_one({"kakao_id": kakao_id})

    if not user:
        await db["users"].insert_one({"kakao_id": kakao_id, "nickname": nickname})

    jwt_token = create_access_token(
        data={"sub": kakao_id},
        expires_delta=timedelta(hours=1)
    )

    return {
        "access_token": jwt_token,
        "user_id": kakao_id,
        "nickname": nickname
    }
