import pytest
from pydantic import ValidationError
from src.schemas.review_schema import ReviewFinding, ReviewResult


def test_valid_finding():
    finding = ReviewFinding(
        issue_title="Possible division by zero",
        category="Bug",
        severity="High",
        line_number=4,
        description="The denominator may be zero.",
        suggested_fix="Check the denominator before division.",
        confidence=0.95,
    )
    assert finding.line_number == 4


def test_invalid_severity_rejected():
    with pytest.raises(ValidationError):
        ReviewFinding(
            issue_title="Example",
            category="Bug",
            severity="Urgent",
            line_number=None,
            description="Example",
            suggested_fix="Example",
            confidence=0.5,
        )


def test_empty_review_is_valid():
    result = ReviewResult(
        review_type="bugs",
        overall_summary="No issues found.",
    )
    assert result.findings == []
