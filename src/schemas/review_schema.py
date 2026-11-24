
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator


Severity = Literal["Critical", "High", "Medium", "Low", "Info"]
Category = Literal["Bug", "Security", "Performance", "Quality"]


class ReviewFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue_title: str = Field(
        description="Short title of the issue"
    )

    category: Category
    severity: Severity

    line_number: int | None = Field(
        default=None,
        ge=1,
        description="1-based source line, or null if uncertain"
    )

    description: str = Field(
        description="What is wrong and why it matters"
    )

    suggested_fix: str = Field(
        description="A practical suggested correction"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0. Example: 0.90 means 90%."
    )

    @field_validator("confidence", mode="before")
    @classmethod
    def normalize_confidence(cls, value):
        """Convert percentage confidence into a 0-1 decimal."""
        if isinstance(value, (int, float)) and 1 < value <= 100:
            return value / 100

        return value


class ReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_type: str
    overall_summary: str

    findings: list[ReviewFinding] = Field(
        default_factory=list
    )

    positive_observations: list[str] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )


class StaticFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: Literal["Ruff", "Bandit"]
    issue_title: str
    category: Category
    severity: Severity
    line_number: int | None = None
    description: str

    suggested_fix: str = (
        "Review the tool message and update the code if appropriate."
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0
    )

    tool_code: str | None = None


class CodeReviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    language: str
    review_type: str
    overall_summary: str

    findings: list[ReviewFinding | StaticFinding] = Field(
        default_factory=list
    )

    positive_observations: list[str] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )
