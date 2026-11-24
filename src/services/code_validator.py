from config.settings import get_settings


SUPPORTED_LANGUAGES = {"python"}


def validate_code(code: str, language: str = "python") -> str:
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Please provide source code to review.")

    normalized_language = language.strip().lower()
    if normalized_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Language '{language}' is not supported yet. "
            "Version 1 supports Python only."
        )

    max_chars = get_settings().max_code_chars
    if len(code) > max_chars:
        raise ValueError(
            f"Code is too large ({len(code)} characters). "
            f"Maximum allowed size is {max_chars} characters."
        )

    return code
