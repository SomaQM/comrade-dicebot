FROM python:3.14 as builder

RUN pip install poetry==2.3.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.14-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    SQLITE_PATH=/data/comrade-dicebot.db

RUN useradd comrade-dicebot && mkdir -p /app /data

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY src/comrade-dicebot /app/comrade-dicebot

RUN chown -R comrade-dicebot:comrade-dicebot /app /data

USER comrade-dicebot
WORKDIR /app

VOLUME ["/data"]

ENTRYPOINT ["python", "-m", "comrade-dicebot"]
