import json
from src.schemas.review_schema import CodeReviewReport


def report_to_json(report: CodeReviewReport) -> str:
    return report.model_dump_json(indent=2)


def report_to_markdown(report: CodeReviewReport) -> str:
    lines = [
        "# CodeSense AI – Code Review Report",
        "",
        f"- **Language:** {report.language}",
        f"- **Review type:** {report.review_type}",
        "",
        "## Summary",
        "",
        report.overall_summary,
        "",
        "## Findings",
        "",
    ]

    if not report.findings:
        lines.append("No findings were returned.")
    else:
        for index, finding in enumerate(report.findings, start=1):
            source = getattr(finding, "source", "Mistral AI")
            location = (
                f"Line {finding.line_number}"
                if finding.line_number is not None else "Line not specified"
            )
            lines.extend([
                f"### {index}. {finding.issue_title}",
                f"- **Source:** {source}",
                f"- **Category:** {finding.category}",
                f"- **Severity:** {finding.severity}",
                f"- **Location:** {location}",
                f"- **Confidence:** {finding.confidence:.0%}",
                "",
                finding.description,
                "",
                f"**Suggested fix:** {finding.suggested_fix}",
                "",
            ])

    lines.extend(["## Positive observations", ""])
    lines.extend([f"- {item}" for item in report.positive_observations] or ["- None provided"])
    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {item}" for item in report.limitations] or ["- None reported"])
    lines.extend([
        "",
        "> AI-generated reviews and static-analysis results require human verification. "
        "This report is not proof that code is secure or correct.",
    ])
    return "\n".join(lines)
