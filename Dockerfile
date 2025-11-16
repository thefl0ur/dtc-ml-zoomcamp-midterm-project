FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base

ARG MODEL_FILE="model/trained_model.json"

WORKDIR /app

COPY server/ pyproject.toml uv.lock .

COPY ${MODEL_FILE} model.json

RUN uv sync --locked --no-group dev

FROM base AS prod

RUN uv add uvicorn

EXPOSE 8081

CMD [".venv/bin/uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8081"]