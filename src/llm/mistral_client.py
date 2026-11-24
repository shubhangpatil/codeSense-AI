
from langchain_ollama import ChatOllama

from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
)


def get_mistral_chat_model():
    """Initialize Ministral locally through Ollama."""

    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=OLLAMA_TEMPERATURE,
        num_ctx=4096,
        num_predict=1200,
        keep_alive="10m",
    )
