from openai import OpenAI
from realtime_phone_agents.stt.models.base import STTModel
from realtime_phone_agents.config import settings

from fastrtc import audio_to_bytes


class FasterWhisperSTT(STTModel):
    """Speech-to-Text model using Groq Whisper."""

    def __init__(self):
        self.client = OpenAI(api_key="", base_url=f"{settings.runpod.faster_whisper_pod_url}/v1")

    def stt(self, audio_data: bytes) -> str:
        """Convert speech audio to text."""
        
        response = self.client.audio.transcriptions.create(
            file=("audio.wav", audio_to_bytes(audio_data)),
            model=settings.runpod.faster_whisper_model,
            response_format="verbose_json"
        )
        return response.text
