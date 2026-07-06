# syntax=docker/dockerfile:1
FROM ubuntu:24.04 AS build

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

# Use the system python and compile bytecode for faster container startup.
ENV UV_PYTHON_PREFERENCE=only-system \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-venv \
    build-essential \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /pythontemplate

WORKDIR /pythontemplate

RUN uv sync --no-default-groups \
    && rm -rf .git




FROM ubuntu:24.04

ENV PATH="/pythontemplate/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /pythontemplate /pythontemplate
WORKDIR /pythontemplate
