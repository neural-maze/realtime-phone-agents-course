from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Groq Configuration ---
class GroqSettings(BaseModel):
    api_key: str = Field(default="", description="Groq API Key")
    base_url: str = Field(
        default="https://api.groq.com/openai/v1", description="Groq Base URL"
    )
    model: str = Field(default="openai/gpt-oss-20b", description="Groq Model to use")
    stt_model: str = Field(
        default="whisper-large-v3", description="Groq STT Model to use"
    )


# --- OpenAI Configuration ---
class OpenAISettings(BaseModel):
    api_key: str = Field(default="", description="OpenAI API Key")
    model: str = Field(default="gpt-4o-mini", description="OpenAI Model to use")


# --- Superlinked Configuration ---
class SuperlinkedSettings(BaseModel):
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding Model to use for Superlinked",
    )
    sqft_min_value: int = Field(
        default=20, description="Minimum value for appartment size in square feet"
    )
    sqft_max_value: int = Field(
        default=2000, description="Maximum value for appartment size in square feet"
    )
    price_min_value: int = Field(
        default=100000, description="Minimum value for appartment price in euros"
    )
    price_max_value: int = Field(
        default=10000000, description="Maximum value for appartment price in euros"
    )


# --- Qdrant Configuration ---
class QdrantSettings(BaseModel):
    host: str = Field(default="qdrant", description="Qdrant Host")
    port: int = Field(default=6333, description="Qdrant Port")
    api_key: str = Field(default="", description="Qdrant API Key")
    cluster_url: str = Field(default="", description="Qdrant Cluster URL")
    use_qdrant_cloud: bool = Field(default=True, description="Use Qdrant Cloud")


# --- RunPod Configuration ---
class RunPodSettings(BaseModel):
    api_key: str = Field(default="", description="RunPod API Key")
    faster_whisper_gpu_type: str = Field(
        default="NVIDIA GeForce RTX 4090", description="Faster Whisper GPU Type"
    )
    orpheus_gpu_type: str = Field(
        default="NVIDIA GeForce RTX 5090", description="Orpheus GPU Type"
    )


# --- Faster Whisper STT Configuration ---
class FasterWhisperSettings(BaseModel):
    api_url: str = Field(
        default="http://localhost:8000", description="Faster Whisper API URL"
    )
    model: str = Field(
        default="Systran/faster-whisper-large-v3", description="Faster Whisper Model"
    )


# --- Orpheus TTS Configuration (RunPod) ---
class OrpheusTTSSettings(BaseModel):
    api_url: str = Field(
        default="http://localhost:8000", description="Orpheus TTS API URL"
    )
    model: str = Field(default="orpheus-3b-0.1-ft", description="Orpheus TTS Model")
    voice: str = Field(default="mia", description="Default voice")
    temperature: float = Field(default=0.6, description="Temperature for generation")
    top_p: float = Field(default=0.9, description="Top-p sampling parameter")
    max_tokens: int = Field(default=1200, description="Maximum tokens to generate")
    repetition_penalty: float = Field(default=1.1, description="Repetition penalty")
    sample_rate: int = Field(default=24000, description="Audio sample rate (Hz)")
    debug: bool = Field(default=False, description="Enable debug mode")


# --- Together AI TTS Configuration ---
class TogetherTTSSettings(BaseModel):
    api_key: str = Field(default="", description="Together AI API Key")
    api_url: str = Field(
        default="https://api.together.xyz/v1", description="Together AI API URL"
    )
    model: str = Field(
        default="canopylabs/orpheus-3b-0.1-ft", description="Together AI TTS Model"
    )
    voice: str = Field(default="tara", description="Default voice for TTS")
    sample_rate: int = Field(default=24000, description="Audio sample rate (Hz)")


# --- Opik Configuration ---
class OpikSettings(BaseModel):
    api_key: str = Field(default="", description="Opik API Key")
    project_name: str = Field(default="", description="Opik Project Name")


# --- Twilio Configuration ---
class TwilioSettings(BaseModel):
    account_sid: str = Field(default="", description="Twilio Account SID")
    auth_token: str = Field(default="", description="Twilio Auth Token")


# --- Settings Configuration ---
class Settings(BaseSettings):
    groq: GroqSettings = Field(default_factory=GroqSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    superlinked: SuperlinkedSettings = Field(default_factory=SuperlinkedSettings)
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    runpod: RunPodSettings = Field(default_factory=RunPodSettings)
    faster_whisper: FasterWhisperSettings = Field(default_factory=FasterWhisperSettings)
    orpheus: OrpheusTTSSettings = Field(default_factory=OrpheusTTSSettings)
    together: TogetherTTSSettings = Field(default_factory=TogetherTTSSettings)
    opik: OpikSettings = Field(default_factory=OpikSettings)
    twilio: TwilioSettings = Field(default_factory=TwilioSettings)

    stt_model: str = Field(
        default="whisper-groq",
        description="STT model to use (moonshine, whisper-groq, faster-whisper)",
    )
    tts_model: str = Field(
        default="together",
        description="TTS model to use (kokoro, orpheus-runpod, together)",
    )

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()
