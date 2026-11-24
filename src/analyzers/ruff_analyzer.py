import json
import subprocess
import sys
import tempfile
from pathlib import Path
from config.settings import get_settings
from src.schemas.review_schema import StaticFinding


def run_ruff(code: str) -> list[StaticFinding]:
    """Run Ruff on a temporary source file. The source is never executed."""
    timeout = get_settings().analyzer_timeout_seconds

    with tempfile.TemporaryDirectory(prefix="codesense_") as temp_dir:
        source_path = Path(temp_dir) / "submitted_code.py"
        source_path.write_text(code, encoding="utf-8")

        command = [
            sys.executable, "-m", "ruff", "check",
            "--output-format", "json", str(source_path),
        ]

        try:
            completed = subprocess.run(
                command, capture_output=True, text=True,
                timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            return []

        try:
            items = json.loads(completed.stdout or "[]")
        except json.JSONDecodeError:
            return []

        findings = []
        for item in items:
            location = item.get("location") or {}
            code_id = item.get("code")
            findings.append(
                StaticFinding(
                    source="Ruff",
                    issue_title=item.get("message", "Ruff finding"),
                    category="Quality",
                    severity="Low",
                    line_number=location.get("row"),
                    description=item.get("message", "Static analysis finding"),
                    suggested_fix=(
                        item.get("fix", {}).get("message")
                        if item.get("fix") else
                        "Review the Ruff finding and update the source if appropriate."
                    ),
                    confidence=1.0,
                    tool_code=code_id,
                )
            )
        return findings
