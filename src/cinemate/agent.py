"""LLM configuration. The LangChain agent itself is not implemented yet (Prompt 2)."""

from langchain_openai import ChatOpenAI

from cinemate.config import get_llm_api_key, get_model_name


def get_llm() -> ChatOpenAI:
    """Build the chat model from environment configuration (no hardcoded secrets)."""
    return ChatOpenAI(model=get_model_name(), api_key=get_llm_api_key(), temperature=0.3)
