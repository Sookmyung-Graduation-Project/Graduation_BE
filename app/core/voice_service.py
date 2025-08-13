from app.core.elevenlabs_client import ElevenLabsClient

class VoiceService:
    def __init__(self, client: ElevenLabsClient):
        self.client = client

    async def create_ivc(self, name: str, files: list[str], description: str | None = None) -> dict:
        return await self.client.create_ivc(name, files, description)

    async def tts(self, voice_id: str, text: str) -> bytes:
        return await self.client.tts(voice_id, text)
