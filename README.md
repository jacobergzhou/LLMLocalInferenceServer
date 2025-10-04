# LLM Inference Server

LLM Inference Server is a lightweight FastAPI application that exposes a REST health check and two WebSocket endpoints for streaming text responses. The server is designed as a foundation for experimenting with large-language-model serving patterns and will be expanded incrementally over time.

## Background

The project currently provides:
- `GET /health_check` for verifying service availability.
- `GET /websocket` for bidirectional message echoing.
- `GET /websocket/stream` for sending a fixed sequence of tokens at one-second intervals.

Future iterations will extend these endpoints into a more complete inference workflow.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for package management and running the application.

Install project dependencies with:

```bash
uv sync
```

## Running the Server

Start the FastAPI application with the auto-reloader:

```bash
uv run uvicorn app.main:app --reload
```

Then test the health endpoint:

```bash
curl http://127.0.0.1:8000/health_check
```

To interact with the WebSocket endpoints, use your preferred WebSocket client (e.g., `websocat`, browser dev tools, or a Python script).

## Incremental Updates

This README documents the current state of the project and will be kept up to date as new inference features and deployment instructions are added.
