from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    """Request model for ingesting properties into the vector database."""
    data_path: str = Field(..., description="Path to the CSV file containing property data")


class SearchRequest(BaseModel):
    """Request model for searching properties."""
    query: str = Field(..., description="Natural language query for property search")
    limit: int = Field(default=3, ge=1, le=10, description="Maximum number of results to return")

