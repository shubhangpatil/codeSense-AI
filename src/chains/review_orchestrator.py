
from langchain_core.runnables import RunnableBranch

from src.chains.review_chain import build_review_chain


def build_review_orchestrator():
    """
    Build review chains.

    Full review uses ONE LLM request for all four review areas.
    Focused reviews use one LLM request for the selected area.
    """

    bugs_chain = build_review_chain(
        """
        Focus only on bugs and correctness:
        - Logical errors
        - Runtime exceptions
        - Boundary conditions
        - Incorrect calculations
        - Missing input validation
        """
    )

    security_chain = build_review_chain(
        """
        Focus only on security:
        - Hardcoded credentials and secrets
        - SQL injection
        - Command injection
        - Unsafe deserialization
        - Insecure operations
        Report only vulnerabilities supported by the code.
        """
    )

    performance_chain = build_review_chain(
        """
        Focus only on performance:
        - Inefficient algorithms
        - Unnecessary loops and computations
        - Memory inefficiency
        - Repeated operations
        - Avoidable delays
        """
    )

    quality_chain = build_review_chain(
        """
        Focus only on code quality:
        - Readability
        - Naming conventions
        - Maintainability
        - Code organization
        - Documentation
        - Best practices
        """
    )

    # All four areas are reviewed in ONE model invocation.
    full_chain = build_review_chain(
        """
        Perform a complete Python code review covering all four areas:

        1. BUGS AND CORRECTNESS
           Find logical errors, runtime exceptions, boundary conditions,
           incorrect calculations, and missing input validation.

        2. SECURITY
           Find hardcoded credentials, injection risks, unsafe operations,
           insecure deserialization, and other vulnerabilities.

        3. PERFORMANCE
           Find inefficient algorithms, unnecessary computations,
           excessive memory usage, and avoidable operations.

        4. CODE QUALITY
           Find readability, maintainability, naming, documentation,
           and structural problems.

        IMPORTANT RULES:
        - Review all four areas in this single review.
        - Report only actionable findings.
        - Do not invent vulnerabilities or bugs.
        - Do not invent line numbers.
        - Use null for line_number when uncertain.
        - Avoid duplicate findings.
        - Keep descriptions and suggested fixes concise.
        - If no issues are found in an area, do not invent one.
        """
    )

    return RunnableBranch(
        (lambda x: x.get("review_type") == "bugs", bugs_chain),
        (lambda x: x.get("review_type") == "security", security_chain),
        (lambda x: x.get("review_type") == "performance", performance_chain),
        (lambda x: x.get("review_type") == "quality", quality_chain),
        full_chain,
    )
