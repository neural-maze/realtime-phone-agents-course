from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Health check endpoint to monitor service readiness."""
    try:
        return {
            "status": "healthy",
            "message": "Service is ready",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Service initialization failed: {str(e)}",
        }

