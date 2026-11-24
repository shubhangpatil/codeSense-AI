
from langchain_ollama import ChatOllama

from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
)


def get_mistral_chat_model():
    """Initialize Ministral 3B locally through Ollama."""

    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=OLLAMA_TEMPERATURE,
        num_ctx=8192,
        keep_alive="10m",
    )
