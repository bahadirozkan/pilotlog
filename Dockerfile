# pull offical base
FROM python:3.11.7-slim-bullseye AS builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev \
    build-essential \
    gettext \
    wget \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /code

COPY pyproject.toml poetry.lock /code/

# Install dependencies:
RUN poetry install
# copy project
COPY . .
