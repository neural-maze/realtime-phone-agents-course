"""Isolate audio, accounts and import-time registration; keep the real agent graph.

The package initializer versions all avatars with Opik on import. These CPU-only
scripted-model tests load the production modules without that account side effect.
LangChain, LangGraph, MCP and HTTPX are real, not stubs.
"""

import importlib
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

ROOT = Path(__file__).resolve().parents[1] / "src" / "realtime_phone_agents"


def module(name, **attrs):
    obj = types.ModuleType(name)
    obj.__dict__.update(attrs)
    sys.modules[name] = obj
    return obj


def load_runtime():
    package = module("realtime_phone_agents")
    package.__path__ = [str(ROOT)]
    module("realtime_phone_agents.agent.stream", VoiceAgentStream=lambda **kw: kw)
    module(
        "opik",
        track=lambda **kw: lambda fn: fn,
        opik_context=types.SimpleNamespace(
            update_current_trace=lambda **kw: None,
        ),
    )
    module("opik.integrations")
    module("opik.integrations.langchain", OpikTracer=lambda **kw: BaseCallbackHandler())
    for name, attr in (
        ("stt", "get_stt_model"),
        ("tts", "get_tts_model"),
        ("background_effects", "get_sound_effect"),
    ):
        module("realtime_phone_agents." + name, **{attr: lambda *a: None})
    module(
        "realtime_phone_agents.avatars.registry",
        get_avatar=lambda name: types.SimpleNamespace(
            get_system_prompt=lambda: "Use search_property_tool for listing details.",
        ),
    )
    service = types.SimpleNamespace(
        search_properties=AsyncMock(
            return_value=[
                {
                    "address": "Example property",
                    "price": 300000,
                }
            ]
        )
    )
    module(
        "realtime_phone_agents.infrastructure.superlinked.service",
        get_property_search_service=lambda: service,
    )
    runtime = importlib.import_module("realtime_phone_agents.agent.fastrtc_agent")
    # Keep FastRTC's real task-local connection context, but avoid constructing a
    # VAD/audio handler. The production stream closure still executes unchanged.
    runtime.ReplyOnPause = lambda handler: handler
    return runtime


class ScriptedModel(BaseChatModel):
    """Deterministic tool choice and result echo, with no live LLM inference."""

    operation: str = "web_search"
    arguments: dict = Field(
        default_factory=lambda: {
            "objective": "Find public transport in Salamanca Madrid",
            "search_queries": ["Salamanca Madrid metro lines"],
        }
    )
    seen: list = Field(default_factory=list)

    @property
    def _llm_type(self):
        return "scripted-tool-test"

    def bind_tools(self, tools, **kwargs):
        self.seen.append({"tools": [t.name for t in tools]})
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.seen.append(messages)
        if isinstance(messages[-1], ToolMessage):
            answer = AIMessage(content="Source result: " + str(messages[-1].content))
        else:
            answer = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": self.operation,
                        "args": self.arguments,
                        "id": "scripted-call",
                        "type": "tool_call",
                    }
                ],
            )
        return ChatResult(generations=[ChatGeneration(message=answer)])
