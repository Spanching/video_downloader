
FROM python:3.10-alpine

RUN apk update \
RUN apk add --no-cache gcc
RUN apk add --no-cache ffmpeg

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
COPY . /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

ENTRYPOINT ["python", "-m", "fragment_downloader"]
