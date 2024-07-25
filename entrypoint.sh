#!/bin/sh
# chmod +x entrypoint.sh
set -e

# Apply database migrations
poetry run alembic upgrade head

# Start FastAPI application
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
