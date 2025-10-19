FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD . .
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["uv", "run", "python", "app/main.py"]
