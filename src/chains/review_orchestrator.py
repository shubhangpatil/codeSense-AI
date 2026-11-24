from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel
from src.chains.review_chain import build_review_chain
from src.schemas.review_schema import ReviewResult


def _combine_parallel_results(results: dict) -> ReviewResult:
    findings = []
    positives = []
    limitations = []
    summaries = []

    for name, result in results.items():
        if not isinstance(result, ReviewResult):
            result = ReviewResult.model_validate(result)
        summaries.append(f"{name.title()}: {result.overall_summary}")
        findings.extend(result.findings)
        positives.extend(result.positive_observations)
        limitations.extend(result.limitations)

    # Remove exact duplicate findings while preserving order.
    unique = []
    seen = set()
    for finding in findings:
        key = (
            finding.issue_title.strip().lower(),
            finding.line_number,
            finding.category,
        )
        if key not in seen:
            seen.add(key)
            unique.append(finding)

    return ReviewResult(
        review_type="full",
        overall_summary=" ".join(summaries),
        findings=unique,
        positive_observations=list(dict.fromkeys(positives)),
        limitations=list(dict.fromkeys(limitations)),
    )


def build_review_orchestrator():
    """Route a request to one focused chain or all four chains in parallel."""
    bug_chain = build_review_chain(
        "Bug and correctness review: logical errors, runtime exceptions, "
        "boundary conditions, and input validation."
    )
    security_chain = build_review_chain(
        "Security review: hardcoded secrets, unsafe operations, injection risks, "
        "and insecure patterns. Report only evidence visible in the code."
    )
    performance_chain = build_review_chain(
        "Performance review: inefficient algorithms, unnecessary work, "
        "memory use, and avoidable computations."
    )
    quality_chain = build_review_chain(
        "Code quality review: readability, naming, maintainability, structure, "
        "documentation, and best practices."
    )

    full_parallel = (
        RunnableParallel(
            bugs=bug_chain,
            security=security_chain,
            performance=performance_chain,
            quality=quality_chain,
        )
        | RunnableLambda(_combine_parallel_results)
    )

    return RunnableBranch(
        (lambda x: x.get("review_type") == "bugs", bug_chain),
        (lambda x: x.get("review_type") == "security", security_chain),
        (lambda x: x.get("review_type") == "performance", performance_chain),
        (lambda x: x.get("review_type") == "quality", quality_chain),
        full_parallel,
    )
