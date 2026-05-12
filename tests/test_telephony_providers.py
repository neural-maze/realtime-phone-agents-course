from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from realtime_phone_agents.api.models import CallRequest
from realtime_phone_agents.config import TelnyxSettings, TelephonySettings
from realtime_phone_agents.telephony import providers
from realtime_phone_agents.telephony.providers import (
    TelnyxProvider,
    get_telephony_provider,
)


def test_get_telephony_provider_returns_telnyx_provider():
    provider = get_telephony_provider("telnyx")

    assert isinstance(provider, TelnyxProvider)


def test_telnyx_provider_posts_texml_call(monkeypatch):
    monkeypatch.setattr(
        providers,
        "settings",
        SimpleNamespace(
            telnyx=TelnyxSettings(
                api_key="test-api-key",
                account_sid="test-account-sid",
                application_sid="test-application-sid",
            ),
            telephony=TelephonySettings(provider="telnyx"),
        ),
    )

    response = Mock()
    response.json.return_value = {"sid": "call-123", "status": "queued"}
    response.raise_for_status.return_value = None
    post = Mock(return_value=response)
    monkeypatch.setattr(providers.requests, "post", post)

    result = TelnyxProvider().start_call(
        CallRequest(
            **{
                "from": "+15551234567",
                "to": "+15557654321",
                "voice_agent_url": "https://agent.example.com",
            }
        )
    )

    assert result.provider == "telnyx"
    assert result.call_id == "call-123"

    post.assert_called_once()
    url = post.call_args.args[0]
    payload = post.call_args.kwargs["json"]
    headers = post.call_args.kwargs["headers"]

    assert url == "https://api.telnyx.com/texml/Accounts/test-account-sid/Calls"
    assert payload == {
        "ApplicationSid": "test-application-sid",
        "To": "+15557654321",
        "From": "+15551234567",
        "Url": "https://agent.example.com/voice/telephone/incoming",
        "StatusCallback": "https://agent.example.com/call/telnyx/events",
        "StatusCallbackEvent": "initiated ringing answered completed",
    }
    assert headers["Authorization"] == "Bearer test-api-key"


def test_telnyx_provider_requires_credentials(monkeypatch):
    monkeypatch.setattr(
        providers,
        "settings",
        SimpleNamespace(
            telnyx=TelnyxSettings(),
            telephony=TelephonySettings(provider="telnyx"),
        ),
    )

    with pytest.raises(ValueError) as error:
        TelnyxProvider().start_call(
            CallRequest(
                **{
                    "from": "+15551234567",
                    "to": "+15557654321",
                    "voice_agent_url": "https://agent.example.com",
                }
            )
        )

    message = str(error.value)
    assert "TELNYX__API_KEY" in message
    assert "TELNYX__ACCOUNT_SID" in message
    assert "TELNYX__APPLICATION_SID" in message
