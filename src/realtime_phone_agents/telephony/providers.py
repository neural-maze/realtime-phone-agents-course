from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid4

import requests
from twilio.rest import Client

from realtime_phone_agents.api.models import CallRequest
from realtime_phone_agents.config import settings


@dataclass
class CallStartResult:
    provider: str
    call_id: str
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = {
            "provider": self.provider,
            "sid": self.call_id,
            "call_id": self.call_id,
        }
        if self.raw:
            result["raw"] = self.raw
        return result


class TelephonyProvider(Protocol):
    name: str

    def start_call(self, call_request: CallRequest) -> CallStartResult: ...


class TwilioProvider:
    name = "twilio"

    def start_call(self, call_request: CallRequest) -> CallStartResult:
        client = Client(
            settings.twilio.account_sid,
            settings.twilio.auth_token,
        )

        call = client.calls.create(
            to=call_request.to_number,
            from_=call_request.from_number,
            url=f"{call_request.voice_agent_url}/voice/telephone/incoming",
        )

        return CallStartResult(provider=self.name, call_id=call.sid)


class TelnyxProvider:
    name = "telnyx"
    api_base_url = "https://api.telnyx.com"

    def start_call(self, call_request: CallRequest) -> CallStartResult:
        self._validate_settings()

        payload: dict[str, Any] = {
            "ApplicationSid": settings.telnyx.application_sid,
            "To": call_request.to_number,
            "From": call_request.from_number,
            "Url": f"{call_request.voice_agent_url}/voice/telephone/incoming",
            "StatusCallback": f"{call_request.voice_agent_url}{settings.telnyx.webhook_path}",
            "StatusCallbackEvent": "initiated ringing answered completed",
        }

        response = requests.post(
            self._calls_url(),
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.telnyx.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()

        body = response.json()
        call_id = (
            body.get("sid")
            or body.get("call_sid")
            or body.get("CallSid")
            or body.get("status")
            or str(uuid4())
        )
        return CallStartResult(provider=self.name, call_id=call_id, raw=body)

    def _validate_settings(self) -> None:
        missing = []
        if not settings.telnyx.api_key:
            missing.append("TELNYX__API_KEY")
        if not settings.telnyx.account_sid:
            missing.append("TELNYX__ACCOUNT_SID")
        if not settings.telnyx.application_sid:
            missing.append("TELNYX__APPLICATION_SID")
        if missing:
            raise ValueError(f"Missing Telnyx configuration: {', '.join(missing)}")

    def _calls_url(self) -> str:
        return f"{self.api_base_url}/texml/Accounts/{settings.telnyx.account_sid}/Calls"


def get_telephony_provider(provider: str) -> TelephonyProvider:
    if provider == "twilio":
        return TwilioProvider()
    if provider == "telnyx":
        return TelnyxProvider()
    raise ValueError(f"Unsupported telephony provider: {provider}")
