from abc import ABC, abstractmethod
from typing import AsyncIterator, Tuple

import numpy as np

AudioChunk = Tuple[int, np.ndarray]  # (sample_rate, samples)


class BaseVoiceEffect(ABC):
    """
    Base class for any audio effect that streams audio chunks.
    Examples: keyboard clicks, hold music, notifications.
    """

    @abstractmethod
    async def stream(self) -> AsyncIterator[AudioChunk]:
        """
        Yields (sample_rate, chunk) pairs.
        Chunk is expected to be a float32 numpy array in [-1, 1].
        """
        ...
