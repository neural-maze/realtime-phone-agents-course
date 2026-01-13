"""Edge TTS model for Spanish voice synthesis."""

import asyncio
import io
import numpy as np
from typing import AsyncGenerator, Tuple

import edge_tts

from realtime_phone_agents.tts.base import TTSModel


class EdgeTTSModel(TTSModel):
    """Edge TTS model with Spanish voice support."""

    def __init__(self, voice: str = "es-ES-ElviraNeural"):
        """
        Initialize Edge TTS model.

        Args:
            voice: Voice to use. Spanish options:
                - es-ES-ElviraNeural (female, Spain - RECOMENDADO, voz natural y profesional)
                - es-ES-AlvaroNeural (male, Spain)
                - es-ES-AbrilNeural (female, Spain - voz joven)
                - es-ES-ArnauNeural (male, Spain - voz joven)
                - es-MX-DaliaNeural (female, Mexico)
                - es-MX-JorgeNeural (male, Mexico)
        """
        self.voice = voice
        self.sample_rate = 24000

    def set_voice(self, voice: str):
        """Set the voice to use."""
        self.voice = voice

    def tts(self, text: str) -> bytes:
        """Convert text to speech bytes."""
        return asyncio.run(self._tts_async(text))

    async def _tts_async(self, text: str) -> bytes:
        """Async implementation of TTS."""
        communicate = edge_tts.Communicate(text, self.voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data

    async def stream_tts(self, text: str) -> AsyncGenerator[Tuple[int, np.ndarray], None]:
        """
        Stream TTS audio chunks.

        Args:
            text: Text to synthesize

        Yields:
            Tuple of (sample_rate, audio_samples)
        """
        communicate = edge_tts.Communicate(text, self.voice)

        audio_buffer = b""
        chunk_size = 4800  # 0.2 seconds at 24kHz

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer += chunk["data"]

                # Process complete chunks
                while len(audio_buffer) >= chunk_size * 2:  # *2 for 16-bit audio
                    # Extract chunk
                    chunk_data = audio_buffer[:chunk_size * 2]
                    audio_buffer = audio_buffer[chunk_size * 2:]

                    # Convert to numpy array
                    audio_array = np.frombuffer(chunk_data, dtype=np.int16)
                    yield (self.sample_rate, audio_array)

        # Process remaining audio
        if audio_buffer:
            audio_array = np.frombuffer(audio_buffer, dtype=np.int16)
            if len(audio_array) > 0:
                yield (self.sample_rate, audio_array)
