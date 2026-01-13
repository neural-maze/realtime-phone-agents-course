"""Google TTS model for Spanish voice synthesis."""

import io
import numpy as np
from typing import AsyncGenerator, Tuple
from pydub import AudioSegment

from gtts import gTTS

from realtime_phone_agents.tts.base import TTSModel


class GoogleTTSModel(TTSModel):
    """Google TTS model with Spanish support."""

    def __init__(self, lang: str = "es", tld: str = "es"):
        """
        Initialize Google TTS model.

        Args:
            lang: Language code (es for Spanish)
            tld: Top-level domain for accent (es=Spain, com.mx=Mexico)
        """
        self.lang = lang
        self.tld = tld
        self.sample_rate = 24000

    def set_voice(self, voice: str):
        """Set voice/accent - for gTTS this changes the tld."""
        if voice == "es-ES" or voice == "carmen":
            self.tld = "es"
        elif voice == "es-MX":
            self.tld = "com.mx"

    def tts(self, text: str) -> bytes:
        """Convert text to speech bytes."""
        tts = gTTS(text=text, lang=self.lang, tld=self.tld)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()

    async def stream_tts(self, text: str) -> AsyncGenerator[Tuple[int, np.ndarray], None]:
        """
        Stream TTS audio chunks.

        Note: gTTS doesn't support true streaming, so we generate the full audio
        and then yield it in chunks.

        Args:
            text: Text to synthesize

        Yields:
            Tuple of (sample_rate, audio_samples)
        """
        # Generate full audio
        tts = gTTS(text=text, lang=self.lang, tld=self.tld)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Convert MP3 to PCM using pydub
        audio = AudioSegment.from_mp3(fp)
        audio = audio.set_frame_rate(self.sample_rate)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)  # 16-bit

        # Get raw audio data
        raw_data = audio.raw_data
        audio_array = np.frombuffer(raw_data, dtype=np.int16)

        # Yield in chunks of ~0.2 seconds
        chunk_size = int(self.sample_rate * 0.2)
        for i in range(0, len(audio_array), chunk_size):
            chunk = audio_array[i:i + chunk_size]
            if len(chunk) > 0:
                yield (self.sample_rate, chunk)
