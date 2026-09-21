"""Live checks against real TMDB / LLM. Skipped automatically without keys.

Run with:  pytest -m live -v
"""

import os

import pytest

pytestmark = pytest.mark.live

# Captured at import time, before conftest swaps in a fake key for unit tests.
REAL_TMDB_KEY = os.environ.get("TMDB_API_KEY")


@pytest.mark.skipif(not REAL_TMDB_KEY, reason="TMDB_API_KEY not set")
def test_live_tmdb_known_movie(monkeypatch):
    from cinemate.tools import search_movies
    monkeypatch.setenv("TMDB_API_KEY", REAL_TMDB_KEY)
    assert "Inception" in search_movies.invoke({"query": "Inception"})


@pytest.mark.skipif(not REAL_TMDB_KEY, reason="TMDB_API_KEY not set")
def test_live_tmdb_nonexistent_movie(monkeypatch):
    from cinemate.tools import search_movies
    monkeypatch.setenv("TMDB_API_KEY", REAL_TMDB_KEY)
    assert "No movies found" in search_movies.invoke({"query": "qzxwvbnm asdfghjkl 987654"})
