"""Entry point. For now this is a smoke check of the foundation (tool + LLM).

Run:  python -m cinemate.app
The interactive agent app will be added once the agent works.
"""

from cinemate.config import ConfigError
from cinemate.tools import search_movies


def check_tool() -> None:
    print("=== TMDB tool: 'Inception' ===")
    print(search_movies.invoke({"query": "Inception"}))
    print("\n=== TMDB tool: nonexistent movie ===")
    print(search_movies.invoke({"query": "qzxwvbnm asdfghjkl 987654"}))


def check_llm() -> None:
    from cinemate.agent import get_llm
    from cinemate.prompts import CINEMATE_PROMPT

    print("\n=== LLM: prompt | model ===")
    chain = CINEMATE_PROMPT | get_llm()  # LCEL: prompt template piped into the model
    reply = chain.invoke({"input": "Say hello and introduce yourself in one sentence."})
    print(reply.content)


def main() -> None:
    try:
        check_tool()
        check_llm()
    except ConfigError as e:
        print(f"\nConfiguration problem: {e}")


if __name__ == "__main__":
    main()
