from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from realtime_phone_agents.infrastructure.superlinked.service import get_property_search_service
from realtime_phone_agents.api.routes import health, superlinked
from realtime_phone_agents.api.routes.voice import mount_voice_stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown events."""
    # Startup: Initialize PropertySearchService
    app.state.property_service = get_property_search_service()
    yield
    # Shutdown: Cleanup if needed
    # Add any cleanup logic here if necessary


app = FastAPI(
    title="Phone Calling Agent API",
    description="An AI-powered phone calling agent API using FastRTC",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(superlinked.router)

# Mount voice stream for Twilio integration
mount_voice_stream(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
