import asyncio
from pathlib import Path
from typing import AsyncIterator, List

from realtime_phone_agents.background_effects.utils.audio_loader import load_audio_chunks

from .base import AudioChunk, BaseVoiceEffect

# Get the directory where this file is located
_EFFECTS_DIR = Path(__file__).parent
_DEFAULT_KEYBOARD_SOUND = str(_EFFECTS_DIR / "sounds" / "keyboard.mp3")


class KeyboardEffect(BaseVoiceEffect):
    """
    Streams a keyboard typing sound for up to `max_duration_s` seconds.
    """

    def __init__(
        self,
        path: str = _DEFAULT_KEYBOARD_SOUND,
        max_duration_s: float = 3.0,
        chunk_ms: int = 100,
        target_rate: int = 16000,
    ):
        self.path = path
        self.max_duration_s = max_duration_s
        self.chunks: List[AudioChunk] = load_audio_chunks(
            path=path,
            target_rate=target_rate,
            chunk_ms=chunk_ms,
        )

    async def stream(self) -> AsyncIterator[AudioChunk]:
        if self.max_duration_s <= 0:
            return

        total_samples = 0
        total_samples_allowed = None

        for sample_rate, chunk in self.chunks:
            # lazy initialize allowed sample budget
            if total_samples_allowed is None:
                total_samples_allowed = int(self.max_duration_s * sample_rate)

            if total_samples >= total_samples_allowed:
                break

            remaining_samples = total_samples_allowed - total_samples

            # Trim last chunk if needed
            if len(chunk) > remaining_samples:
                chunk = chunk[:remaining_samples]

            if len(chunk) == 0:
                break

            yield (sample_rate, chunk)
            total_samples += len(chunk)

            await asyncio.sleep(0)
