# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A LangChain course/learning project. It's early-stage: currently a single `main.py` entry point that loads environment variables via `python-dotenv` and reads `OPENAI_API_KEY`. Expect this to grow into multiple LangChain examples/scripts.

## Environment & dependencies

- Python >=3.13, managed with `uv` (dependencies declared in `pyproject.toml`, locked in `uv.lock`).
- Key dependencies: `langchain`, `langchain-openai`, `python-dotenv`, plus `black` and `isort` for formatting.
- Secrets (e.g. `OPENAI_API_KEY`) live in `.env`, loaded at runtime via `load_dotenv()`. Never commit `.env`.

## Common commands

```bash
uv sync              # install/update dependencies from uv.lock
uv run main.py        # run the main script
uv add <package>      # add a new dependency (updates pyproject.toml + uv.lock)
uv run black .         # format code
uv run isort .         # sort imports
```

There are no tests or lint/CI configuration in this repo yet.
