
from langchain_core.runnables import Runnable

from src.llm.mistral_client import get_mistral_chat_model
from src.prompts.review_prompts import REVIEW_PROMPT
from src.schemas.review_schema import ReviewResult


def build_review_chain(review_focus: str) -> Runnable:
    """Build one focused review chain with validated structured output."""

    model = get_mistral_chat_model()

    structured_model = model.with_structured_output(
        ReviewResult,
        method="json_schema"
    )

    prompt = REVIEW_PROMPT.partial(
        review_focus=review_focus
    )

    return prompt | structured_model
