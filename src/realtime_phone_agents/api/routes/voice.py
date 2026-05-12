from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, Request

from realtime_phone_agents.agent.fastrtc_agent import FastRTCAgent
from realtime_phone_agents.api.models import CallRequest
from realtime_phone_agents.config import settings
from realtime_phone_agents.telephony import get_telephony_provider

router = APIRouter(prefix="/call", tags=["voice"])


@router.post("")
async def start_call(call_request: CallRequest):
    """
    Initiates an outbound phone call to connect to the AI voice agent.

    Args:
        call_request: Call request containing from and to phone numbers

    Returns:
        Dictionary containing the provider call identifier
    """
    try:
        provider = get_telephony_provider(settings.telephony.provider)
        return provider.start_call(call_request).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initiate {settings.telephony.provider} call: {str(e)}",
        )


@router.post("/telnyx/events")
async def telnyx_events(request: Request):
    """
    Acknowledge Telnyx Voice API call events.

    Telnyx retries events unless the webhook returns a 2xx response. This endpoint
    intentionally keeps the first integration lightweight: the FastRTC media stream
    handles audio, while Voice API events are accepted for call lifecycle tracking.
    """
    await request.body()
    return {"received": True}


def mount_voice_stream(app: FastAPI):
    """
    Mount the FastRTC agent voice stream to the application.

    Args:
        app: FastAPI application instance
    """
    agent = FastRTCAgent(
        thread_id=str(uuid4()),
    )

    # Mount Websocket endpoint for telephone integrations
    agent.stream.mount(app, path="/voice")
