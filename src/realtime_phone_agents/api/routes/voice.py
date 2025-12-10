from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException
from twilio.rest import Client

from realtime_phone_agents.agent.fastrtc_agent import FastRTCAgent
from realtime_phone_agents.api.models import CallRequest
from realtime_phone_agents.config import settings

router = APIRouter(prefix="/call", tags=["voice"])


@router.post("")
async def start_call(call_request: CallRequest):
    """
    Initiates a Twilio phone call to connect to the AI voice agent.

    Args:
        call_request: Call request containing from and to phone numbers

    Returns:
        Dictionary containing the Twilio call SID
    """
    try:
        client = Client(
            settings.twilio.account_sid,
            settings.twilio.auth_token,
        )

        call = client.calls.create(
            to=call_request.to_number,
            from_=call_request.from_number,
            url=f"{call_request.voice_agent_url}/voice/telephone/incoming",
        )

        return {"sid": call.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")


def mount_voice_stream(app: FastAPI):
    """
    Mount the FastRTC agent voice stream to the application.

    Args:
        app: FastAPI application instance
    """
    agent = FastRTCAgent(
        thread_id=str(uuid4()),
    )

    # Mount Websocket endpoint for Twilio Integration
    agent.stream.mount(app, path="/voice")
