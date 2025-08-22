from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
import httpx

from app.core.jwt import create_access_token
from app.schemas.auth import KakaoLoginRequest, KakaoLoginResponse
from app.models.user import User, LoginType, UserRole

router = APIRouter()
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

@router.post("/kakao", response_model=KakaoLoginResponse)
async def kakao_login(body: KakaoLoginRequest):
    headers = {"Authorization": f"Bearer {body.access_token}"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(KAKAO_USER_INFO_URL, headers=headers)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"카카오 API 요청 오류: {e}")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="잘못된 카카오 토큰")

    kakao_user = response.json()
    kakao_id = str(kakao_user.get("id"))
    props = kakao_user.get("properties", {}) or {}
    account = kakao_user.get("kakao_account", {}) or {}

    nickname = props.get("nickname", f"user-{kakao_id}")
    profile_image = props.get("profile_image") or props.get("profile_image_url") or ""
    email = account.get("email")

  
    user = await User.find_one({
        "provider": LoginType.kakao.value,
        "provider_user_id": kakao_id
    })

    if not user:
        try:
            user = User(
                provider=LoginType.kakao,
                provider_user_id=kakao_id,
                nickname=nickname,
                profile_image=profile_image,
                email=email,
                user_role=UserRole.parent,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            await user.insert()
        except Exception:
            user = await User.find_one({
                "provider": LoginType.kakao.value,
                "provider_user_id": kakao_id
            })
    else:
        user.nickname = nickname
        user.profile_image = profile_image
        user.email = email or user.email
        user.updated_at = datetime.utcnow()
        await user.save()

    jwt_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=1)
    )

    return KakaoLoginResponse(
        access_token=jwt_token,
        user_id=str(user.id),
        nickname=nickname,
        profile_image=profile_image
    )
