build-dev:
    docker build -t model-serving-server .

dev:
    docker run -p 8000:8000 model-serving-server

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
