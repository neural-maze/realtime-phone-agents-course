from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    """Request model for ingesting properties into the vector database."""

    data_path: str = Field(
        ..., description="Path to the CSV file containing property data"
    )


class SearchRequest(BaseModel):
    """Request model for searching properties."""

    query: str = Field(..., description="Natural language query for property search")
    limit: int = Field(
        default=3, ge=1, le=10, description="Maximum number of results to return"
    )


class CallRequest(BaseModel):
    """Request model for initiating a Twilio phone call."""

    from_number: str = Field(..., alias="from", description="Phone number to call from")
    to_number: str = Field(..., alias="to", description="Phone number to call to")
    voice_agent_url: str = Field(..., description="URL of the voice agent to connect to")

    class Config:
        populate_by_name = True
