"""MeloTTS model for high-quality Spanish voice synthesis."""

import numpy as np
from typing import AsyncGenerator, Tuple
from loguru import logger

from realtime_phone_agents.tts.base import TTSModel


class MeloTTSModel(TTSModel):
    """MeloTTS model with Spanish support - high quality, runs on CPU."""

    def __init__(self, language: str = "ES", device: str = "auto"):
        """
        Initialize MeloTTS model.

        Args:
            language: Language code (ES for Spanish, EN for English)
            device: Device to use (auto, cpu, cuda)
        """
        self.language = language
        self.device = device
        self._model = None
        self._speaker_ids = None
        self.sample_rate = 44100  # MeloTTS uses 44.1kHz

    def _load_model(self):
        """Lazy load the model."""
        if self._model is None:
            logger.info(f"Loading MeloTTS model for language: {self.language}")
            from melo.api import TTS

            self._model = TTS(language=self.language, device=self.device)
            self._speaker_ids = self._model.hps.data.spk2id
            logger.info(f"MeloTTS loaded. Available speakers: {list(self._speaker_ids.keys())}")

    def set_voice(self, voice: str):
        """Set voice - MeloTTS uses speaker IDs."""
        # For Spanish, the default speaker is usually 'ES'
        pass

    def tts(self, text: str) -> bytes:
        """Convert text to speech bytes."""
        self._load_model()

        # Get the first available speaker for the language
        speaker_id = list(self._speaker_ids.values())[0]

        # Generate audio
        audio = self._model.tts_to_file(
            text,
            speaker_id,
            output_path=None,  # Return audio directly
            speed=1.0
        )

        return audio

    async def stream_tts(self, text: str) -> AsyncGenerator[Tuple[int, np.ndarray], None]:
        """
        Stream TTS audio chunks.

        Note: MeloTTS generates full audio, then we stream in chunks.

        Args:
            text: Text to synthesize

        Yields:
            Tuple of (sample_rate, audio_samples)
        """
        self._load_model()

        # Get the first available speaker for the language
        speaker_id = list(self._speaker_ids.values())[0]

        # Generate full audio (MeloTTS returns numpy array)
        audio_array = self._model.tts_to_file(
            text,
            speaker_id,
            output_path=None,
            speed=1.0
        )

        # Convert to int16 if needed
        if audio_array.dtype != np.int16:
            # Normalize to int16 range
            audio_array = (audio_array * 32767).astype(np.int16)

        # Yield in chunks of ~0.2 seconds
        chunk_size = int(self.sample_rate * 0.2)
        for i in range(0, len(audio_array), chunk_size):
            chunk = audio_array[i:i + chunk_size]
            if len(chunk) > 0:
                yield (self.sample_rate, chunk)
