
from src.analyzers.bandit_analyzer import run_bandit
from src.analyzers.ruff_analyzer import run_ruff

from src.chains.review_orchestrator import build_review_orchestrator

from src.schemas.review_schema import CodeReviewReport
from src.services.code_validator import validate_code


class ReviewService:

    def __init__(self) -> None:
        self.orchestrator = build_review_orchestrator()

    def review(
        self,
        code: str,
        language: str = "python",
        review_type: str = "full",
        include_static_analysis: bool = True,
    ) -> CodeReviewReport:

        # Validate input code before analysis.
        code = validate_code(code, language)

        valid_review_types = {
            "full",
            "bugs",
            "security",
            "performance",
            "quality",
        }

        if review_type not in valid_review_types:
            raise ValueError("Invalid review type selected.")

        # One LLM invocation for the selected review.
        ai_result = self.orchestrator.invoke(
            {
                "code": code,
                "language": language,
                "review_type": review_type,
            }
        )

        static_findings = []
        limitations = list(ai_result.limitations)

        # Run static analysis independently of the LLM.
        if include_static_analysis and language.lower() == "python":

            try:
                ruff_findings = run_ruff(code)
                static_findings.extend(ruff_findings)

            except Exception as exc:
                limitations.append(
                    f"Ruff analysis could not complete: {exc}"
                )

            try:
                bandit_findings = run_bandit(code)
                static_findings.extend(bandit_findings)

            except Exception as exc:
                limitations.append(
                    f"Bandit analysis could not complete: {exc}"
                )

        # Combine AI findings and static-analysis findings.
        return CodeReviewReport(
            language=language,
            review_type=review_type,
            overall_summary=ai_result.overall_summary,
            findings=[
                *ai_result.findings,
                *static_findings,
            ],
            positive_observations=ai_result.positive_observations,
            limitations=limitations,
        )
