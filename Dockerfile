# === Builder Stage ===
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# === Runtime Stage ===
FROM python:3.13-slim-trixie AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app/.venv/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY . .

EXPOSE 8000

CMD ["python", "app/main.py"]
