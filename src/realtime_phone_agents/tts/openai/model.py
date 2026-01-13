"""OpenAI TTS model."""

import os
import numpy as np
from typing import AsyncGenerator, Tuple
from openai import AsyncOpenAI
from loguru import logger

from realtime_phone_agents.tts.base import TTSModel


class OpenAITTSModel(TTSModel):
    """OpenAI TTS model (tts-1)."""

    def __init__(self, voice: str = "nova", model: str = "tts-1"):
        """
        Initialize OpenAI TTS.
        
        Args:
            voice: Voice ID (alloy, echo, fable, onyx, nova, shimmer)
            model: Model ID (tts-1, tts-1-hd)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            
        self.client = AsyncOpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        self.sample_rate = 24000

    def set_voice(self, voice: str):
        """Set voice."""
        self.voice = voice

    async def tts(self, text: str) -> bytes:
         # Note: This is a placeholder as the main usage is stream_tts
        return b""

    async def stream_tts(self, text: str) -> AsyncGenerator[Tuple[int, np.ndarray], None]:
        """Stream TTS audio."""
        try:
            async with self.client.audio.speech.with_streaming_response.create(
                model=self.model,
                voice=self.voice,
                input=text,
                response_format="pcm"
            ) as response:
                async for chunk in response.iter_bytes(chunk_size=4096):
                    if chunk:
                        # Convert bytes to numpy array
                        audio_array = np.frombuffer(chunk, dtype=np.int16)
                        yield (self.sample_rate, audio_array)
                        
        except Exception as e:
            logger.error(f"Error in OpenAI TTS stream: {e}")
