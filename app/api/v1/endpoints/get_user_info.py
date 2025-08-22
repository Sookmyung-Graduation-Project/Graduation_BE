from app.models.voice import Voice
from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me", summary="User 정보 조회, jwt 필요")
async def get_my_info(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "provider": current_user.provider,
        "provider_user_id": current_user.provider_user_id,
        "nickname": current_user.nickname,
        "profile_image": current_user.profile_image,
        "email": current_user.email,
        "user_role": current_user.user_role,
        "child_age": current_user.child_age,
        "default_voice_id": str(current_user.default_voice_id) if current_user.default_voice_id else None,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
    }

@router.get("/user/myvoice", summary="내 보이스 목록, jwt 필요")
async def list_my_voices(current_user: User = Depends(get_current_user)):
    docs = await Voice.find(Voice.user_id == current_user.id).to_list()
    return [{
        "_id": str(d.id),
        "voice_name": d.voice_name,
        "voice_id": d.voice_id,
        "description": d.description,
        "created_at": d.created_at.isoformat() if d.created_at else None,
        "default_id": d.default_id,
    } for d in docs]
