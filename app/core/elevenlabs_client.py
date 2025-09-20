import os, httpx, mimetypes
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()
_BASE = "https://api.elevenlabs.io/v1"

class ElevenLabsClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set")

    async def create_ivc(self, name: str, files: List[str], description: Optional[str] = None) -> dict:
        headers = {"xi-api-key": self.api_key}
        data = {"name": name}
        if description:
            data["description"] = description
        multipart = []
        file_handles = []
        try:
            for p in files:
                ctype = mimetypes.guess_type(p)[0] or "audio/mpeg"
                fh = open(p, "rb")                 # 열어둔 핸들 추적
                file_handles.append(fh)
                multipart.append(("files", (os.path.basename(p), fh, ctype)))

            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(f"{_BASE}/voices/add", headers=headers, data=data, files=multipart)
                r.raise_for_status()
                return r.json()
        finally:
            for fh in file_handles:
                try: fh.close()
                except: pass

    async def tts(self, voice_id: str, text: str, *, model_id: str = "eleven_multilingual_v2") -> bytes:
        headers = {"xi-api-key": self.api_key, "accept": "audio/mpeg"}
        params = {"output_format": "mp3_44100_128"}
        payload = {"text": text, "model_id": model_id}
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.post(f"{_BASE}/text-to-speech/{voice_id}",
                                  headers=headers, params=params, json=payload)
            r.raise_for_status()
            return r.content
