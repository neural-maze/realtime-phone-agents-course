from uuid import uuid4

from fastapi import FastAPI

from realtime_phone_agents.agent.fastrtc_agent import FastRTCAgent


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
