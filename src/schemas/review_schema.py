from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


Severity = Literal["Critical", "High", "Medium", "Low", "Info"]
Category = Literal["Bug", "Security", "Performance", "Quality"]


class ReviewFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue_title: str = Field(description="Short title of the issue")
    category: Category
    severity: Severity
    line_number: int | None = Field(
        default=None, ge=1, description="1-based source line, or null if uncertain"
    )
    description: str = Field(description="What is wrong and why it matters")
    suggested_fix: str = Field(description="A practical suggested correction")
    confidence: float = Field(ge=0.0, le=1.0)


class ReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_type: str
    overall_summary: str
    findings: list[ReviewFinding] = Field(default_factory=list)
    positive_observations: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class StaticFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: Literal["Ruff", "Bandit"]
    issue_title: str
    category: Category
    severity: Severity
    line_number: int | None = None
    description: str
    suggested_fix: str = "Review the tool message and update the code if appropriate."
    confidence: float = 1.0
    tool_code: str | None = None


class CodeReviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    review_type: str
    overall_summary: str
    findings: list[ReviewFinding | StaticFinding] = Field(default_factory=list)
    positive_observations: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
