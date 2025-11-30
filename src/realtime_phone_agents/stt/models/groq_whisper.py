from openai import OpenAI
from realtime_phone_agents.stt.models.base import STTModel
from realtime_phone_agents.config import settings

from fastrtc import audio_to_bytes


class GroqWhisperSTT(STTModel):
    """Speech-to-Text model using Groq Whisper."""

    def __init__(self, model_name: str = settings.groq.stt_model):
        self.groq_client = OpenAI(api_key=settings.groq.api_key, base_url=settings.groq.base_url)
        self.model_name = model_name

    def stt(self, audio_data: bytes) -> str:
        """Convert speech audio to text."""
        
        response = self.groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_to_bytes(audio_data)),
            model=self.model_name,
            response_format="verbose_json"
        )
        return response.text
