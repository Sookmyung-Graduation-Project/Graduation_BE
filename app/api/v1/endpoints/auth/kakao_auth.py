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
    try:
        # 카카오 API 호출
        async with httpx.AsyncClient() as client:
            response = await client.get(KAKAO_USER_INFO_URL, headers=headers)

            # 디버깅 로그
            print(f"Kakao /v2/user/me status: {response.status_code}")
            print(f"Kakao /v2/user/me response: {response.json()}")

    except httpx.RequestError as e:
        # 요청 에러 발생 시 처리
        raise HTTPException(status_code=500, detail=f"카카오 API 요청 중 오류 발생: {str(e)}")
    
    # 응답 상태 코드가 200이 아니면 오류 처리
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="잘못된 카카오 토큰")

    # 카카오 사용자 정보 추출
    kakao_user = response.json()
    kakao_id = str(kakao_user["id"])
    nickname = kakao_user["properties"]["nickname"]

    # 데이터베이스에서 사용자 확인
    user = await db["users"].find_one({"kakao_id": kakao_id})

    # 사용자가 없으면 새로 삽입
    if not user:
        await db["users"].insert_one({"kakao_id": kakao_id, "nickname": nickname})

    # JWT 토큰 생성
    jwt_token = create_access_token(
        data={"sub": kakao_id},
        expires_delta=timedelta(hours=1)
    )

    # 응답 반환
    return KakaoLoginResponse(
        access_token=jwt_token,
        user_id=kakao_id,
        nickname=nickname
    )
