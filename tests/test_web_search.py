import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import httpx
from langchain_core.messages import ToolMessage
from runtime_support import ScriptedModel, load_runtime

runtime = load_runtime()
from realtime_phone_agents.agent.tools import web_search as web
from realtime_phone_agents.config import Settings

REAL_ASYNC_CLIENT = httpx.AsyncClient


class MCPServer:
    """HTTP fixture using real MCP initialize/call/response parsing."""

    def __init__(self):
        self.requests = []
        self.calls = []
        self.mode = "success"
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.clients = []

    async def respond(self, request):
        self.requests.append(request)
        if request.method != "POST":
            return httpx.Response(405)
        payload = json.loads(request.content)
        method = payload["method"]
        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "initialize":
            result = {
                "protocolVersion": payload["params"]["protocolVersion"],
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "test-search", "version": "1"},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {"name": name, "inputSchema": {"type": "object"}}
                    for name in ("web_search", "web_fetch")
                ]
            }
        elif method == "tools/call":
            self.calls.append(payload["params"])
            self.started.set()
            if self.mode == "wait":
                await self.release.wait()
            if self.mode == "http_error":
                return httpx.Response(503)
            if self.mode == "quota":
                result = {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": "Anonymous free-tier quota exceeded. Try again later.",
                        }
                    ],
                }
            else:
                result = {
                    "isError": False,
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                {
                                    "results": [
                                        {
                                            "title": "Madrid Metro",
                                            "url": "https://www.metromadrid.es/en",
                                            "excerpts": [
                                                "Line four serves the Salamanca district."
                                            ],
                                        }
                                    ],
                                }
                            ),
                        }
                    ],
                }
        else:
            raise AssertionError("Unexpected MCP method: " + method)
        return httpx.Response(
            200, json={"jsonrpc": "2.0", "id": payload["id"], "result": result}
        )

    def client(self, **kwargs):
        client = REAL_ASYNC_CLIENT(
            transport=httpx.MockTransport(self.respond), **kwargs
        )
        self.clients.append(client)
        return client


class WebSearchTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.server = MCPServer()
        self.patches = [
            patch.dict(os.environ, {}, clear=True),
            patch.object(web.httpx, "AsyncClient", self.server.client),
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def agent(self, thread="conversation-a", tools=None, enabled=True):
        model = ScriptedModel()
        config = Settings(_env_file=None, web_search_enabled=enabled)

        class SpeechToText:
            def stt(self, audio):
                return "Tell me about the area's public transport"

        class TextToSpeech:
            async def stream_tts(self, text):
                yield text

        with (
            patch.object(runtime, "ChatGroq", return_value=model),
            patch.object(runtime, "settings", config),
        ):
            agent = runtime.FastRTCAgent(
                thread_id=thread,
                tools=tools,
                stt_model=SpeechToText(),
                tts_model=TextToSpeech(),
                voice_effect=object(),
                sound_effect_seconds=0,
            )

        return agent, model

    async def test_audio_handler_speaks_consumed_tool_result(self):
        agent, _ = self.agent()
        chunks = [chunk async for chunk in agent._process_audio((16000, None))]
        self.assertEqual(chunks[0], "Let me look for that in the system")
        self.assertIn("Line four", chunks[-1])
        self.assertIn("https://www.metromadrid.es/en", chunks[-1])

    async def turn(self, agent):
        return [
            chunk async for chunk in agent._process_with_agent("Tell me about the area")
        ]

    async def test_real_graph_consumes_search_and_fetch(self):
        agent, model = self.agent()
        await self.turn(agent)
        result = await agent._get_final_response()
        self.assertIn("https://www.metromadrid.es/en", result)
        self.assertIn("Line four", result)
        self.assertTrue(
            any(
                isinstance(row, list) and isinstance(row[-1], ToolMessage)
                for row in model.seen
            )
        )
        tools = next(row["tools"] for row in model.seen if isinstance(row, dict))
        self.assertEqual(tools, ["search_property_tool", "web_search", "web_fetch"])
        model.operation = "web_fetch"
        model.arguments = {
            "urls": ["https://www.metromadrid.es/en"],
            "objective": "Metro lines",
        }
        await self.turn(agent)
        model.operation = "web_search"
        model.arguments = {
            "objective": "More public transport",
            "search_queries": ["Salamanca bus transport"],
        }
        await self.turn(agent)
        ids = [c["arguments"]["session_id"] for c in self.server.calls]
        self.assertEqual(len(set(ids)), 1)
        UUID(ids[0])
        self.assertNotEqual(ids[0], "conversation-a")
        self.assertEqual(
            [c["name"] for c in self.server.calls],
            ["web_search", "web_fetch", "web_search"],
        )
        for request in self.server.requests:
            self.assertEqual(str(request.url), web.MCP_URL)
            self.assertEqual(request.headers["user-agent"], web.USER_AGENT)
            self.assertNotIn("authorization", request.headers)
        self.assertTrue(all(c.is_closed for c in self.server.clients))
        schema = web.web_search.tool_call_schema.model_json_schema()
        self.assertNotIn("config", schema["properties"])
        self.assertNotIn("session_id", schema["properties"])

    async def test_concurrent_conversations_and_reset(self):
        agent_a, _ = self.agent("same-local-label")
        agent_b, _ = self.agent("same-local-label")
        await asyncio.gather(self.turn(agent_a), self.turn(agent_b))
        old_a, old_b = [c["arguments"]["session_id"] for c in self.server.calls]
        self.assertNotEqual(old_a, old_b)
        await asyncio.gather(self.turn(agent_b), self.turn(agent_a))
        self.assertEqual(
            {c["arguments"]["session_id"] for c in self.server.calls}, {old_a, old_b}
        )
        agent_a.set_thread_id("new-conversation")
        await self.turn(agent_a)
        self.assertNotIn(
            self.server.calls[-1]["arguments"]["session_id"], {old_a, old_b}
        )
        agent_a.set_thread_id("same-local-label")
        await self.turn(agent_a)
        self.assertEqual(self.server.calls[-1]["arguments"]["session_id"], old_a)

    async def test_explicit_and_disabled_tools_preserve_choices(self):
        for supplied, enabled, expected in [
            ([], True, []),
            ([runtime.search_property_tool], True, ["search_property_tool"]),
            (None, False, ["search_property_tool"]),
        ]:
            with self.subTest(supplied=supplied, enabled=enabled):
                agent, _ = self.agent(tools=supplied, enabled=enabled)
                node = agent.react_agent.get_graph().nodes.get("tools")
                actual = [] if node is None else list(node.data.tools_by_name)
                self.assertEqual(actual, expected)
                if expected:
                    model = agent.react_agent.nodes["model"]
                    self.assertIsNotNone(model)
        self.assertEqual(self.server.requests, [])

        agent, model = self.agent(enabled=False)
        model.operation = "search_property_tool"
        model.arguments = {"query": "Madrid apartments"}
        await self.turn(agent)
        self.assertIn("Example property", await agent._get_final_response())
        self.assertEqual(self.server.requests, [])

    async def test_interleaved_threads_on_one_agent_keep_their_ids(self):
        agent, _ = self.agent("first-thread")
        self.server.mode = "wait"
        first = asyncio.create_task(self.turn(agent))
        await asyncio.wait_for(self.server.started.wait(), 2)
        first_id = self.server.calls[0]["arguments"]["session_id"]
        agent.set_thread_id("second-thread")
        self.server.mode = "success"
        await self.turn(agent)
        second_id = self.server.calls[1]["arguments"]["session_id"]
        self.assertNotEqual(first_id, second_id)
        self.server.release.set()
        await first
        await self.turn(agent)
        self.assertEqual(self.server.calls[-1]["arguments"]["session_id"], second_id)
        agent.set_thread_id("first-thread")
        await self.turn(agent)
        self.assertEqual(self.server.calls[-1]["arguments"]["session_id"], first_id)

    async def test_setting_default_and_environment_disable(self):
        self.assertTrue(Settings(_env_file=None).web_search_enabled)
        with patch.dict(os.environ, {"WEB_SEARCH_ENABLED": "false"}):
            self.assertFalse(Settings(_env_file=None).web_search_enabled)
        with tempfile.TemporaryDirectory() as tmp:
            saved = Path(tmp) / ".env"
            saved.write_text("WEB_SEARCH_ENABLED=false\n")
            self.assertFalse(Settings(_env_file=saved).web_search_enabled)

    async def test_errors_are_consumed_without_switching_identity(self):
        agent, _ = self.agent()
        for mode, text in [("quota", "quota exceeded"), ("http_error", "unavailable")]:
            self.server.mode = mode
            await self.turn(agent)
            self.assertIn(text, await agent._get_final_response())
        self.server.mode = "success"
        await self.turn(agent)
        self.assertIn("Line four", await agent._get_final_response())
        self.assertEqual(
            len({c["arguments"]["session_id"] for c in self.server.calls}), 1
        )
        self.assertTrue(all(c.is_closed for c in self.server.clients))

    async def test_timeout_and_cancellation_cleanup(self):
        agent, _ = self.agent()
        self.server.mode = "wait"
        with patch.object(web, "REQUEST_TIMEOUT", 0.05):
            await self.turn(agent)
        self.assertIn("timed out", await agent._get_final_response())
        self.server.started.clear()
        task = asyncio.create_task(self.turn(agent))
        await asyncio.wait_for(self.server.started.wait(), 2)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(all(c.is_closed for c in self.server.clients))
        self.server.mode = "success"
        await self.turn(agent)
        self.assertIn("Line four", await agent._get_final_response())
        self.assertEqual(
            len({c["arguments"]["session_id"] for c in self.server.calls}), 1
        )

    async def test_invalid_urls_and_schema_never_reach_transport(self):
        agent, model = self.agent()
        model.operation = "web_fetch"
        for url in [
            "file:///etc/passwd",
            "javascript:alert(1)",
            "https://user:pass@example.com",
            "https://example.com/ bad",
            "https://example.com:bad/",
            "https://example.com:99999/",
        ]:
            model.arguments = {"urls": [url]}
            await self.turn(agent)
            self.assertIn(
                "Only public HTTP or HTTPS", await agent._get_final_response()
            )
        model.arguments = {"urls": []}
        await self.turn(agent)
        self.assertIn("Invalid web tool arguments", await agent._get_final_response())
        self.assertEqual(self.server.requests, [])


if __name__ == "__main__":
    unittest.main()
