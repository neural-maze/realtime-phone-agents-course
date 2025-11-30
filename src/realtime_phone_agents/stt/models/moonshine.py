from fastrtc import get_stt_model
from realtime_phone_agents.stt.models.base import STTModel


class MoonshineSTT(STTModel):
    """Speech-to-Text model using Moonshine."""

    def __init__(self):
        self.moonshine_client = get_stt_model()

    def stt(self, audio_data: bytes) -> str:
        return self.moonshine_client.stt(audio_data)
