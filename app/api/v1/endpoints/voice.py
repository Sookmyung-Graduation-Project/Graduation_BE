# app/api/v1/endpoints/voice/voice.py
from __future__ import annotations
from typing import Optional, List
import os, tempfile, shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.core.elevenlabs_client import ElevenLabsClient
from app.core.voice_service import VoiceService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter( tags=["voice"])

def get_service() -> VoiceService:
    return VoiceService(ElevenLabsClient())

@router.post("/ivc", summary="Instant Voice Cloning 생성")
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

        return await svc.create_ivc(name=name, files=tmp_paths, description=description)
    finally:
        for p in tmp_paths:
            try: os.remove(p)
            except: pass

@router.post("/tts", summary="Text to Speech 변환")
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
