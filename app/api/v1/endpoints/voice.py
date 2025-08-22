
from __future__ import annotations
from typing import Optional, List
import os, tempfile, shutil
from datetime import datetime
from app.models.voice import Voice
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi import Body


from app.core.elevenlabs_client import ElevenLabsClient
from app.core.voice_service import VoiceService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter( tags=["voice"])

def get_service() -> VoiceService:
    return VoiceService(ElevenLabsClient())

@router.post("/ivc", summary="Instant Voice Cloning 생성, jwt 필요")
async def create_ivc(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    files: List[UploadFile] = File(...),
    svc: VoiceService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    if not files:
        raise HTTPException(400, "files required")

    tmp_paths: list[str] = []
    try:
        for uf in files:
            suffix = os.path.splitext(uf.filename or "")[1]
            fd, path = tempfile.mkstemp(prefix="ivc_", suffix=suffix)
            with os.fdopen(fd, "wb") as out:
                shutil.copyfileobj(uf.file, out)
            tmp_paths.append(path)

        
        result = await svc.create_ivc(name=name, files=tmp_paths, description=description)
        provider_voice_id = result.get("voice_id")
        if not provider_voice_id:
            raise HTTPException(502, "IVC provider did not return voice_id")
        
        
        voice_doc = Voice(
            voice_id=provider_voice_id,
            voice_name=name,
            user_id=current_user.id,   
            created_at=datetime.now(),
            default_id=False,
        )
        
        voice_doc.voice_id = provider_voice_id
        if description:
            voice_doc.description = description

        await voice_doc.insert()

        return {
            "ok": True,
            "voice": voice_doc.dict(),
            "provider_result": result
        }

    finally:
        for p in tmp_paths:
            try: os.remove(p)
            except: pass

@router.post("/tts", summary="Text to Speech 변환, jwt 필요")
async def tts(
    voice_id: str = Form(...),
    text: str = Form(...),
    svc: VoiceService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    if not text.strip():
        raise HTTPException(400, "text is empty")

    audio = await svc.tts(voice_id=voice_id, text=text)
    return StreamingResponse(
        iter([audio]),
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="speech.mp3"'},
    )

@router.post("/tts/test", summary="Text to Speech 변환, jwt 필요")
async def tts(
    voice_id: str = Form(...),
    svc: VoiceService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    
    fixed_text = "In a quiet village where the sky brushes the fields in hues of gold, young Mia discovered a map leading to forgotten treasures."

    if not fixed_text.strip():
        raise HTTPException(400, "text is empty")

    audio = await svc.tts(voice_id=voice_id, text=fixed_text)
    return StreamingResponse(
        iter([audio]),
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="speech.mp3"'},
    )


@router.post("/default", summary="기본 음성 설정 업데이트, jwt 필요")
async def update_default_voice(
    voice_id: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user)
):
    
    await Voice.find(
        Voice.user_id == current_user.id,
        Voice.default_id == True
    ).update({"$set": {"default_id": False}})

    
    updated = await Voice.find_one(Voice.voice_id == voice_id, Voice.user_id == current_user.id)
    if not updated:
        return {"error": "voice_id not found for current user"}

    updated.default_id = True
    await updated.save()

    
    current_user.default_voice_id = voice_id
    await current_user.save()

    return {"ok": True, "default_voice_id": voice_id}

@router.post("/name", summary="음성 이름 변경, jwt 필요")
async def update_voice_name(
    voice_id: str = Body(..., embed=True),
    new_name: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user)
):

    voice = await Voice.find_one(Voice.voice_id == voice_id, Voice.user_id == current_user.id)
    if not voice:
        return {"error": "voice_id not found for current user"}


    voice.voice_name = new_name
    await voice.save()

    return {"ok": True, "voice_id": voice_id, "new_name": new_name}

@router.post("/delete", summary="음성 삭제, jwt 필요")
async def delete_voice(
    voice_id: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user)
):

    voice = await Voice.find_one(Voice.voice_id == voice_id, Voice.user_id == current_user.id)
    if not voice:
        return {"error": "voice_id not found for current user"}

    await voice.delete()

    return {"ok": True, "voice_id": voice_id}