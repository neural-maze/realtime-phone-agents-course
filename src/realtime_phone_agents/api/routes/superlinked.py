from fastapi import APIRouter, HTTPException, Request

from realtime_phone_agents.api.models import IngestRequest, SearchRequest

router = APIRouter(prefix="/superlinked", tags=["superlinked"])


@router.post("/ingest")
async def ingest_properties(ingest_request: IngestRequest, request: Request):
    """
    Ingest properties from a CSV file into the Superlinked vector database.
    
    Args:
        ingest_request: IngestRequest containing the path to the CSV file
        request: FastAPI request object to access app state
        
    Returns:
        Success message with the number of properties ingested
    """
    try:
        request.app.state.property_service.ingest_properties(ingest_request.data_path)
        return {
            "status": "success",
            "message": f"Properties ingested successfully from {ingest_request.data_path}",
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {ingest_request.data_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ingesting properties: {str(e)}"
        )


@router.post("/search")
async def search_properties(search_request: SearchRequest, request: Request):
    """
    Search for properties using natural language queries.
    
    Args:
        search_request: SearchRequest containing the query and result limit
        request: FastAPI request object to access app state
        
    Returns:
        List of matching properties with their details
    """
    try:
        properties = await request.app.state.property_service.search_properties(
            query=search_request.query,
            limit=search_request.limit
        )
        return {
            "status": "success",
            "query": search_request.query,
            "limit": search_request.limit,
            "count": len(properties),
            "properties": properties,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching properties: {str(e)}"
        )

