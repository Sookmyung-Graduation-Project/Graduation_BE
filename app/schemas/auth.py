from pydantic import BaseModel

class KakaoLoginRequest(BaseModel):
    access_token: str

class KakaoLoginResponse(BaseModel):
    access_token: str
    user_id: str
    nickname: str
    profile_image: str 