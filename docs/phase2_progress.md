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
- `agent.py`: `get_llm()` builds `ChatGoogleGenerativeAI` (Gemini) from env config. (Switched from OpenAI to Gemini to use the free tier.)
- `agent.py`: `build_agent()` using LangChain 1.x `create_agent` (Gemini + `search_movies` + CineMate system prompt); `print_trace()`/`ask()` show each step ([USER], tool call, [TMDB] results, [CINEMATE] answer). `get_llm()` now uses `retries=1` (library default is 6, which burned free-tier quota).
- `notebooks/CineMate_Phase2.ipynb`: Kaggle notebook (clones the repo, reads Kaggle Secrets, runs TMDB / Gemini / tool / tool-calling / agent / no-result tests, prints a results table).
- Offline tests: 29 passing (includes the agent loop with a scripted fake model and mocked TMDB).

## In Progress
- Live run on Kaggle (TMDB, Gemini, tool calling, agent). **Not yet executed; no live results recorded.**

## Pending
- Conversational memory and follow-up handling.
- Structured output / OutputParser.
- Evaluation, UI, demo.

## Technical Decisions
- Installed LangChain 1.4.2 (langchain-core 1.6.4, langchain-google-genai 4.4.0); uses current APIs (`langchain_core.tools.tool`, `ChatPromptTemplate`), no legacy `AgentExecutor`.
- TMDB client returns a `SearchResult` (success/status/message/movies) instead of raising, so the agent always gets a safe answer.
- Both TMDB auth styles supported (v3 API key as query param; v4 read token as Bearer header), chosen automatically from the single `TMDB_API_KEY` value.
- Only the top 5 results are returned to keep LLM context small.
- Project has its own git repo: the home directory `C:\Users\sanya` is itself a git repo, so commits from this folder would otherwise have gone there.

## Problems Encountered
- TMDB documentation site and API host were unreachable from the development sandbox (timeouts), so the endpoint/field names were written from prior knowledge of TMDB v3 and not checked against live docs or a real response.
- No API keys were configured in the environment.

- TMDB timeouts on the development machine (21 Sep 2026): the home Wi-Fi's DNS resolver (router 192.168.29.1) returns an ISP sinkhole address (49.44.79.236) for `api.themoviedb.org`, `www.` and `developer.themoviedb.org`. TCP to it times out. Google/Cloudflare DNS return TMDB's real addresses (AWS CloudFront). A credential-free request straight to the real address got `401 {"status_code":7,"status_message":"Invalid API key..."}` in under 1 s, so TMDB itself is up, the endpoint `/3/search/movie` exists, and only local DNS is affected. Our code and API key were not the cause.
- Gemini `gemini-3.5-flash` hit `429 RESOURCE_EXHAUSTED`: free-tier limit of 20 requests/day/model (quota id `GenerateRequestsPerDayPerProjectPerModel-FreeTier`). `gemini-2.5-flash` returned model-not-found. `gemini-3.1-flash-lite` answered "CineMate Gemini test successful." locally (one call, verified).
- TMDB `/search/movie` matches titles only (not genre/rating/date range/runtime), so "recommend science-fiction movies" cannot be answered by a genre search. The system prompt now tells the agent to search specific titles and judge results itself; TMDB `/discover/movie` (genre, year, rating, runtime filters) is the better fit for later refinement/follow-ups and is a recommended next design decision.
- Earlier Gemini live tests: `503 UNAVAILABLE` (model overloaded) then `429 RESOURCE_EXHAUSTED` (quota) for `gemini-3.5-flash`. The key is accepted by Google; the model/quota is the issue.

## Solutions
- TMDB: run from an unaffected network (Google Colab, mobile hotspot, VPN) or switch the machine's DNS to a public resolver. Client now uses separate connect/read timeouts (4 s / 10 s) and returns "Unable to reach the movie database right now. Please try again." instead of hanging.
- All unit tests use mocked HTTP; live tests are separate (`pytest -m live`) and skip without keys.
- Live testing moves to Kaggle (network not affected by the local DNS block); secrets come from Kaggle Secrets, never the notebook.
- `.env.example` contains placeholders only; real keys live in `.env` (git-ignored) or Kaggle Secrets.

## Test Evidence
- `python -m pytest -m "not live"` → 29 passed (offline, mocked).
- Notebook logic dry-run locally with no secrets (all live sections skip cleanly) and with a scripted fake Gemini + mocked TMDB (9/9 pass). This checks the notebook code only and is **not** evidence that TMDB or Gemini work.
- Live TMDB / Gemini tool calling / agent output from Kaggle: **not yet collected.**
