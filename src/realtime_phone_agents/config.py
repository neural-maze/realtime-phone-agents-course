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


# --- Groq Configuration ---
class OpenAISettings(BaseModel):
    api_key: str = Field(default="", description="OpenAI API Key")
    model: str = Field(default="gpt-4o-mini", description="OpenAI Model to use")


# --- Superlinked Configuration ---
class SuperlinkedSettings(BaseModel):
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding Model to use for Superlinked")
    sqft_min_value: int = Field(default=20, description="Minimum value for appartment size in square feet")
    sqft_max_value: int = Field(default=2000, description="Maximum value for appartment size in square feet")
    price_min_value: int = Field(default=100000, description="Minimum value for appartment price in euros")
    price_max_value: int = Field(default=10000000, description="Maximum value for appartment price in euros")

# --- Qdrant Configuration ---
class QdrantSettings(BaseModel):
    host: str = Field(default="qdrant", description="Qdrant Host")
    port: int = Field(default=6333, description="Qdrant Port")
    api_key: str = Field(default="", description="Qdrant API Key")
    use_https: bool = Field(default=False, description="Use HTTPS for Qdrant")


# --- Settings Configuration ---
class Settings(BaseSettings):
    groq: GroqSettings = Field(default_factory=GroqSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    superlinked: SuperlinkedSettings = Field(default_factory=SuperlinkedSettings)
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)
    
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()
