
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.ollama_base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )

        self.ollama_model = os.getenv(
            "OLLAMA_MODEL",
            "ministral-3:3b"
        )

        self.ollama_temperature = float(
            os.getenv("OLLAMA_TEMPERATURE", "0.1")
        )

        self.max_code_chars = int(
            os.getenv("MAX_CODE_CHARS", "20000")
        )

        self.analyzer_timeout_seconds = int(
            os.getenv("ANALYZER_TIMEOUT_SECONDS", "15")
        )

        # Uppercase aliases for existing imports
        self.OLLAMA_BASE_URL = self.ollama_base_url
        self.OLLAMA_MODEL = self.ollama_model
        self.OLLAMA_TEMPERATURE = self.ollama_temperature
        self.MAX_CODE_CHARS = self.max_code_chars
        self.ANALYZER_TIMEOUT_SECONDS = self.analyzer_timeout_seconds


def get_settings():
    return Settings()


_settings = get_settings()

OLLAMA_BASE_URL = _settings.OLLAMA_BASE_URL
OLLAMA_MODEL = _settings.OLLAMA_MODEL
OLLAMA_TEMPERATURE = _settings.OLLAMA_TEMPERATURE
MAX_CODE_CHARS = _settings.MAX_CODE_CHARS
ANALYZER_TIMEOUT_SECONDS = _settings.ANALYZER_TIMEOUT_SECONDS
