FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y ffmpeg libgl1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache

# App code
COPY src/realtime_phone_agents realtime_phone_agents/

CMD ["/app/.venv/bin/uvicorn", "realtime_phone_agents.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]
