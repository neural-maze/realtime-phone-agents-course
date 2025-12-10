from fastrtc import Stream
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from loguru import logger
from typing import Any, Callable, Literal
from gradio.components.base import Component
from fastrtc.tracks import HandlerType
from fastrtc.utils import RTCConfigurationCallable


class VoiceAgentStream(Stream):
    
    def __init__(
        self,
        handler: HandlerType,
        *,
        additional_outputs_handler: Callable | None = None,
        mode: Literal["send-receive", "receive", "send"] = "send-receive",
        modality: Literal["video", "audio", "audio-video"] = "video",
        concurrency_limit: int | None | Literal["default"] = "default",
        time_limit: float | None = None,
        allow_extra_tracks: bool = False,
        rtp_params: dict[str, Any] | None = None,
        rtc_configuration: RTCConfigurationCallable | None = None,
        server_rtc_configuration: dict[str, Any] | None = None,
        track_constraints: dict[str, Any] | None = None,
        additional_inputs: list[Component] | None = None,
        additional_outputs: list[Component] | None = None,
        ui_args: Any | None = None,
        verbose: bool = True,
    ):
        """
        Initialize the VoiceAgentStream instance.

        Args:
            handler: The function to handle incoming stream data and return output data.
            additional_outputs_handler: An optional function to handle updates to additional output components.
            mode: The direction of the stream ('send', 'receive', or 'send-receive').
            modality: The type of media ('video', 'audio', or 'audio-video').
            concurrency_limit: Maximum number of concurrent connections. 'default' maps to 1.
            time_limit: Maximum execution time for the handler function in seconds.
            allow_extra_tracks: If True, allows connections with tracks not matching the modality.
            rtp_params: Optional dictionary of RTP encoding parameters.
            rtc_configuration: Optional Callable or dictionary for RTCPeerConnection configuration (e.g., ICE servers).
                               Required when deploying on Colab or Spaces.
            server_rtc_configuration: Optional dictionary for RTCPeerConnection configuration on the server side.
            track_constraints: Optional dictionary of constraints for media tracks (e.g., resolution, frame rate).
            additional_inputs: Optional list of extra Gradio input components.
            additional_outputs: Optional list of extra Gradio output components. Requires `additional_outputs_handler`.
            ui_args: Optional dictionary to customize the default UI appearance (title, subtitle, icon, etc.).
            verbose: Whether to print verbose logging on startup.
        """
        super().__init__(
            handler=handler,
            additional_outputs_handler=additional_outputs_handler,
            mode=mode,
            modality=modality,
            concurrency_limit=concurrency_limit,
            time_limit=time_limit,
            allow_extra_tracks=allow_extra_tracks,
            rtp_params=rtp_params,
            rtc_configuration=rtc_configuration,
            server_rtc_configuration=server_rtc_configuration,
            track_constraints=track_constraints,
            additional_inputs=additional_inputs,
            additional_outputs=additional_outputs,
            ui_args=ui_args,
            verbose=verbose,
        )

    async def handle_incoming_call(self, request: Request):
        """
        Handle incoming telephone calls (e.g., via Twilio).

        Generates TwiML instructions to connect the incoming call to the
        WebSocket handler (`/telephone/handler`) for audio streaming.

        Args:
            request: The FastAPI Request object for the incoming call webhook.

        Returns:
            An HTMLResponse containing the TwiML instructions as XML.
        """
        from twilio.twiml.voice_response import Connect, VoiceResponse

        response = VoiceResponse()
        response.say("Connecting to the AI assistant.")
        connect = Connect()
        
        # Get hostname from X-Forwarded-Host header (if behind proxy) or fallback to request hostname
        hostname = request.headers.get("x-forwarded-host", request.url.hostname)
        
        path = request.url.path.removesuffix("/telephone/incoming")
        connect.stream(url=f"wss://{hostname}{path}/telephone/handler")
        response.append(connect)
        response.say("The call has been disconnected.")
        return HTMLResponse(content=str(response), media_type="application/xml")
