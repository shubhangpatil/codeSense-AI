def severity_label(severity: str) -> str:
    return severity.upper()


def count_by_severity(findings) -> dict[str, int]:
    counts = {name: 0 for name in ["Critical", "High", "Medium", "Low", "Info"]}
    for finding in findings:
        if finding.severity in counts:
            counts[finding.severity] += 1
    return counts
