# CineMate – Agentic Movie Recommendation Assistant

## Project Overview

Choosing a movie is hard: catalogues are huge, and a plain chatbot can only guess from its
training data, so it may invent ratings, release dates or even movies that do not exist.

CineMate is an agentic LLM application built with LangChain. The user describes what they
want in natural language ("some science-fiction movies"). An LLM agent decides when it needs
facts, calls a TMDB tool to retrieve real movie data, and then explains personalised
recommendations grounded in that data. Follow-ups such as "only after 2020" or
"under 2 hours" will refine the results through conversational memory.

## Phase 2 Objective

Get the core end-to-end pipeline working with LangChain and TMDB:
natural-language request → LangChain agent → TMDB tool → TMDB API → real movie data → LLM → recommendation.
Memory, structured output, error-handling polish, evaluation and UI are added incrementally afterwards.

## Planned Architecture

```
User
 ↓
PromptTemplate
 ↓
LLM Agent
 ↓
TMDB Tool
 ↓
TMDB API
 ↓
Movie Data
 ↓
LLM
 ↓
Recommendation
```

Conversational memory and structured output (OutputParser) will be added in subsequent steps.

## Technology Stack

- Python 3.13
- LangChain (`langchain`, `langchain-core`, `langchain-openai`)
- LLM via the OpenAI API
- TMDB API (v3)

## Current Status

| Component | Status |
|---|---|
| Project structure | completed |
| Configuration (`config.py`) | completed |
| TMDB client | completed – unit-tested with mocks; **not yet verified against the live API** |
| LangChain tool | completed – unit-tested with mocks; **not yet verified against the live API** |
| Prompt template | basic version completed |
| LLM configuration | written; **not yet run against a real model** |
| Agent | not yet implemented |
| Memory | not yet implemented |
| Structured output | not yet implemented |
| UI | not yet implemented |

## Setup

```bash
# 1. clone
git clone https://github.com/Malik8122/cinemate-movie-agent.git
cd cinemate-movie-agent

# 2. create and activate an environment
python -m venv .venv
.venv\Scripts\activate          # Windows   (macOS/Linux: source .venv/bin/activate)

# 3. install requirements
pip install -r requirements.txt

# 4. configure secrets: copy the template, then edit .env with your own keys
copy .env.example .env          # macOS/Linux: cp .env.example .env

# 5. run the tests (no keys needed for unit tests)
python -m pytest
```

Optional, with real keys in `.env`:

```bash
python -m pytest -m live -v     # live TMDB checks
python -m cinemate.app          # smoke check: TMDB tool + LLM
```

`.env` is git-ignored; never commit real keys.
