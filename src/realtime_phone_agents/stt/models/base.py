from abc import ABC, abstractmethod
from typing import Union


class STTModel(ABC):
    """
    Abstract base class for Speech-to-Text models.
    
    All STT model implementations must inherit from this class
    and implement the stt method.
    """

    @abstractmethod
    async def stt(
        self,
        audio_data: Union[bytes, str],
        **kwargs
    ) -> str:
        """
        Convert speech audio to text.

        Args:
            audio_data: Audio data as bytes or path to audio file
            **kwargs: Additional model-specific parameters

        Returns:
            str: Transcribed text from the audio

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        pass
