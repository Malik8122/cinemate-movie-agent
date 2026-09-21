# Phase 2 Progress

## Date
21 September 2026

## Completed
- Project structure (src layout, tests, notebooks, docs), `.gitignore`, `.env.example`, pinned `requirements.txt`.
- `config.py`: loads keys from environment/.env; clear error if missing, never prints secrets.
- `tmdb_client.py`: `search_movies(query, year=None)` against TMDB `/search/movie`, genre names via `/genre/movie/list`; results normalised to a `Movie` model.
- Error handling with distinct statuses: ok, no_results, invalid_request, auth_error, api_error, network_error, unexpected_response.
- `tools.py`: `search_movies` LangChain tool (`@tool`) returning readable text.
- `prompts.py`: CineMate system prompt as a `ChatPromptTemplate` with an (empty) chat-history placeholder.
- `agent.py`: `get_llm()` builds `ChatOpenAI` from env config.
- 16 mocked unit tests passing.

## In Progress
- Verifying the TMDB client/tool against the live API (needs `TMDB_API_KEY`).
- Verifying the LLM connection (needs `OPENAI_API_KEY` and `OPENAI_MODEL`).

## Pending
- LangChain agent wiring tool + prompt + LLM.
- Conversational memory and follow-up handling.
- Structured output / OutputParser.
- Evaluation, UI, demo.

## Technical Decisions
- Installed LangChain 1.4.2 (langchain-core 1.6.4, langchain-openai 1.6.2); uses current APIs (`langchain_core.tools.tool`, `ChatPromptTemplate`), no legacy `AgentExecutor`.
- TMDB client returns a `SearchResult` (success/status/message/movies) instead of raising, so the agent always gets a safe answer.
- Both TMDB auth styles supported (v3 API key as query param; v4 read token as Bearer header), chosen automatically from the single `TMDB_API_KEY` value.
- Only the top 5 results are returned to keep LLM context small.
- Project has its own git repo: the home directory `C:\Users\sanya` is itself a git repo, so commits from this folder would otherwise have gone there.

## Problems Encountered
- TMDB documentation site and API host were unreachable from the development sandbox (timeouts), so the endpoint/field names were written from prior knowledge of TMDB v3 and not checked against live docs or a real response.
- No API keys were configured in the environment.

## Solutions
- All unit tests use mocked HTTP; live tests are separate (`pytest -m live`) and skip without keys.
- Next step: run `python -m pytest -m live -v` and `python -m cinemate.app` with real keys and fix any field mismatches.

## Test Evidence
`python -m pytest` → 16 passed, 2 skipped (live tests, no key). Live TMDB and LLM output: not yet collected.
