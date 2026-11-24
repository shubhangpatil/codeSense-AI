import json
import subprocess
import sys
import tempfile
from pathlib import Path
from config.settings import get_settings
from src.schemas.review_schema import StaticFinding


def _bandit_severity(value: str) -> str:
    return {
        "HIGH": "High",
        "MEDIUM": "Medium",
        "LOW": "Low",
    }.get((value or "").upper(), "Info")


def run_bandit(code: str) -> list[StaticFinding]:
    """Run Bandit on a temporary Python file; never execute submitted code."""
    timeout = get_settings().analyzer_timeout_seconds

    with tempfile.TemporaryDirectory(prefix="codesense_") as temp_dir:
        source_path = Path(temp_dir) / "submitted_code.py"
        source_path.write_text(code, encoding="utf-8")

        command = [
            sys.executable, "-m", "bandit",
            "-f", "json", "-q", str(source_path),
        ]

        try:
            completed = subprocess.run(
                command, capture_output=True, text=True,
                timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            return []

        # Bandit may return a non-zero code when it finds issues.
        try:
            payload = json.loads(completed.stdout or "{}")
        except json.JSONDecodeError:
            return []

        findings = []
        for item in payload.get("results", []):
            issue = item.get("issue_text", "Potential security issue")
            test_id = item.get("test_id")
            findings.append(
                StaticFinding(
                    source="Bandit",
                    issue_title=issue,
                    category="Security",
                    severity=_bandit_severity(item.get("issue_severity", "")),
                    line_number=item.get("line_number"),
                    description=issue,
                    suggested_fix=(
                        "Inspect the flagged code and follow the recommended "
                        "secure coding practice for this finding."
                    ),
                    confidence=1.0,
                    tool_code=test_id,
                )
            )
        return findings
