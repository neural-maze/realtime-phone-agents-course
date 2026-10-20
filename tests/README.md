# CPU web-tool tests

Run from the repository root in an isolated environment:

```bash
uv venv /tmp/phone-web-tests
uv pip install --python /tmp/phone-web-tests/bin/python --no-deps -e .
uv pip install --python /tmp/phone-web-tests/bin/python \
  'langchain>=1.0.7' 'langchain-groq>=1.0.1' 'mcp>=1.26,<2' \
  'httpx>=0.28.1,<1' 'pydantic-settings>=2.12.0' 'fastrtc>=0.0.33' numpy loguru
/tmp/phone-web-tests/bin/python -m unittest discover -s tests -v
```

These tests load the production FastRTCAgent and its tools, using real LangChain,
LangGraph and MCP clients. A scripted model chooses tools and echoes their
results; an HTTP fixture serves MCP responses. Audio models, property storage,
FastRTC audio transport and Opik are isolated to avoid GPU downloads, account setup and
the package initializer's avatar registration. No live model, telephone call or
network request is made by this suite.

Coverage includes the audio handler's response path, default/custom/disabled
tools, URLs and source excerpts, HTTP destination and User-Agent, anonymous
headers, MCP errors, timeouts, cancellation cleanup, and conversation identifiers
across follow-ups, concurrent connections sharing a mounted handler, programmatic
conversations and thread changes. Connection tests use FastRTC's real task-local
context, including the connection identifier used for Twilio streams.
