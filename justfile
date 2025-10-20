set dotenv-load

infra-up:
    docker compose up -d postgres localstack
    @echo "Waiting for services to be healthy..."
    @docker compose ps postgres localstack

infra-down:
    docker compose down postgres localstack

infra-logs:
    docker compose logs -f postgres localstack

pg-up:
    docker compose up -d postgres

pg-down:
    docker compose down postgres

pg-logs:
    docker compose logs -f postgres

local:
    @echo "Starting local development server..."
    @echo "Make sure infrastructure is running: just infra-up"
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run entire app stack in Docker (app + infrastructure)
dev:
    docker compose up app --build

migrate:
    uv run alembic upgrade head

migrate-create:
    #!/usr/bin/env bash
    REVISION=$(uv run python -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:-3])")
    MIGRATION_NAME=$(gum input --placeholder "Enter migration name")
    uv run alembic revision --rev-id "${REVISION}" -m "${MIGRATION_NAME}"

migrate-down:
    uv run alembic downgrade -1

migrate-status:
    uv run alembic current

migrate-history:
    uv run alembic history --verbose

codegen-models:
    #!/usr/bin/env bash
    OUTPUT_FILE="${1:-app/models.py}"
    : "${POSTGRES_USER:?POSTGRES_USER is not set}"
    : "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}"
    : "${POSTGRES_DB:?POSTGRES_DB is not set}"
    : "${POSTGRES_HOST:?POSTGRES_HOST is not set}"
    : "${POSTGRES_PORT:?POSTGRES_PORT is not set}"
    DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    echo "Generating models from database: ${DATABASE_URL}"
    uv run sqlacodegen "${DATABASE_URL}" --outfile "${OUTPUT_FILE}"
    echo "Models generated to: ${OUTPUT_FILE}"
