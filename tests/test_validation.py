import pytest
from src.services.code_validator import validate_code


def test_valid_python_code():
    assert validate_code("print('hello')", "python") == "print('hello')"


def test_empty_code_rejected():
    with pytest.raises(ValueError):
        validate_code("   ", "python")


def test_unsupported_language_rejected():
    with pytest.raises(ValueError):
        validate_code("int main() {}", "cpp")
