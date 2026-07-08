# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository structure

This is a LangChain course repo where each git branch is a separate, self-contained lesson — branches are not layered on top of each other, and there is no shared library code between them. Each branch has its own `pyproject.toml`/`uv.lock` and a small number of standalone scripts.

- `project/hello-world` — repo default branch; basic `PromptTemplate` + `ChatOpenAI` example.
- `project/rag-gist` — **current branch**; RAG ingestion pipeline into Pinecone (see below).
- `project/react-search-agent` — LangChain agent (`create_agent`) with a Tavily web-search tool and structured (`AgentResponse`) output.
- `project/agents-under-the-hood` — raw ReAct loop / tool-calling internals without the framework agent abstraction.

If asked about functionality that isn't present on the checked-out branch, it likely lives on one of the others — check with `git show <branch>:<path>` rather than assuming it's missing from the course.

## This branch: project/rag-gist

Single-script RAG ingestion pipeline in `ingestion.py`:
1. Loads `mediumblog1.txt` via `UnstructuredLoader` (`chunking_strategy="basic"`).
2. Splits into 1000-char chunks with `CharacterTextSplitter` (`chunk_overlap=0`).
3. Embeds chunks with `OpenAIEmbeddings`.
4. Upserts into a Pinecone index (name from `INDEX_NAME` env var) via `PineconeVectorStore.from_documents`.

The file path passed to `UnstructuredLoader` is a hardcoded absolute path rather than a relative one — update it if the repo is cloned/moved elsewhere.

## Environment & dependencies

- Python >=3.11, managed with `uv` (deps declared in `pyproject.toml`, locked in `uv.lock`).
- Secrets load from `.env` via `python-dotenv` at import time. This branch requires `OPENAI_API_KEY`, `PINECONE_API_KEY`, and `INDEX_NAME`. (`.env` also carries `LANGSMITH_*`/`TAVILY_API_KEY` used by other branches — unused here.) Never commit `.env`.

## Common commands

```bash
uv sync                # install/update dependencies from uv.lock
uv run ingestion.py    # run the ingestion pipeline
uv add <package>       # add a dependency (updates pyproject.toml + uv.lock)
uv run black .          # format code
uv run isort .          # sort imports
```

No tests, lint config, or CI exist on this branch.
