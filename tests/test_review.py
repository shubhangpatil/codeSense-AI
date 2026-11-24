from unittest.mock import patch
from src.services.review_service import ReviewService
from src.schemas.review_schema import ReviewResult


def test_review_service_without_static_analysis():
    fake_result = ReviewResult(
        review_type="bugs",
        overall_summary="One possible issue.",
        findings=[],
        positive_observations=[],
        limitations=[],
    )

    service = ReviewService()
    with patch.object(service.orchestrator, "invoke", return_value=fake_result):
        report = service.review(
            code="print('hello')",
            language="python",
            review_type="bugs",
            include_static_analysis=False,
        )

    assert report.language == "python"
    assert report.overall_summary == "One possible issue."
