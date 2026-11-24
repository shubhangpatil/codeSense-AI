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
        code = validate_code(code, language)

        if review_type not in {
            "full", "bugs", "security", "performance", "quality"
        }:
            raise ValueError("Invalid review type selected.")

        ai_result = self.orchestrator.invoke(
            {
                "code": code,
                "language": language,
                "review_type": review_type,
            }
        )

        static_findings = []
        limitations = list(ai_result.limitations)

        if include_static_analysis and language.lower() == "python":
            try:
                static_findings.extend(run_ruff(code))
            except Exception as exc:
                limitations.append(f"Ruff analysis could not complete: {exc}")

            try:
                static_findings.extend(run_bandit(code))
            except Exception as exc:
                limitations.append(f"Bandit analysis could not complete: {exc}")

        return CodeReviewReport(
            language=language,
            review_type=review_type,
            overall_summary=ai_result.overall_summary,
            findings=[*ai_result.findings, *static_findings],
            positive_observations=ai_result.positive_observations,
            limitations=limitations,
        )
