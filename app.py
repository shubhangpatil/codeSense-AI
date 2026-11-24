import streamlit as st

from src.services.review_service import ReviewService
from src.services.report_service import report_to_json, report_to_markdown
from src.utils.formatters import count_by_severity

st.set_page_config(
    page_title="CodeSense AI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CodeSense AI")
st.caption("AI-powered code review using LangChain and Mistral")

with st.sidebar:
    st.header("Review settings")
    language = st.selectbox("Programming language", ["Python"])
    review_type = st.selectbox(
        "Review type",
        ["full", "bugs", "security", "performance", "quality"],
        format_func=lambda x: {
            "full": "Full review",
            "bugs": "Bug and correctness",
            "security": "Security",
            "performance": "Performance",
            "quality": "Code quality",
        }[x],
    )
    include_static = st.checkbox("Run Ruff and Bandit", value=True)
    st.divider()
    st.caption("Submitted code is analysed as text. CodeSense AI does not execute it.")

default_code = '''def get_user(name, users=[]):
    users.append(name)
    return users

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
'''

uploaded = st.file_uploader("Upload a Python file (optional)", type=["py"])
if uploaded is not None:
    try:
        code_input = uploaded.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("The uploaded file must be UTF-8 encoded.")
        code_input = ""
else:
    code_input = default_code

code = st.text_area(
    "Paste your source code",
    value=code_input,
    height=300,
    help="Version 1 supports Python. Do not submit secrets or confidential source code.",
)

if st.button("🔍 Review code", type="primary", use_container_width=True):
    try:
        with st.spinner("Reviewing code with Mistral and static analysis..."):
            service = ReviewService()
            report = service.review(
                code=code,
                language=language.lower(),
                review_type=review_type,
                include_static_analysis=include_static,
            )
            st.session_state["last_report"] = report
    except Exception as exc:
        st.error(f"Review failed: {exc}")

report = st.session_state.get("last_report")

if report:
    st.divider()
    st.subheader("Review summary")
    counts = count_by_severity(report.findings)

    cols = st.columns(5)
    for col, (severity, count) in zip(cols, counts.items()):
        col.metric(severity, count)

    st.info(report.overall_summary)

    st.subheader(f"Findings ({len(report.findings)})")
    if not report.findings:
        st.success("No findings were returned. This does not guarantee the code is defect-free.")

    for index, finding in enumerate(report.findings, start=1):
        source = getattr(finding, "source", "Mistral AI")
        location = (
            f"Line {finding.line_number}"
            if finding.line_number is not None else "Line not specified"
        )
        with st.expander(
            f"{index}. [{finding.severity}] {finding.issue_title} — {source}",
            expanded=index == 1,
        ):
            st.write(f"**Category:** {finding.category}")
            st.write(f"**Location:** {location}")
            st.write(f"**Confidence:** {finding.confidence:.0%}")
            st.write(finding.description)
            st.markdown("**Suggested fix**")
            st.write(finding.suggested_fix)
            if getattr(finding, "tool_code", None):
                st.caption(f"Analyzer rule: {finding.tool_code}")

    if report.positive_observations:
        st.subheader("Positive observations")
        for item in report.positive_observations:
            st.write(f"✓ {item}")

    if report.limitations:
        st.subheader("Limitations")
        for item in report.limitations:
            st.warning(item)

    st.subheader("Export report")
    col1, col2 = st.columns(2)
    col1.download_button(
        "Download Markdown",
        data=report_to_markdown(report),
        file_name="codesense_review.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col2.download_button(
        "Download JSON",
        data=report_to_json(report),
        file_name="codesense_review.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption(
    "CodeSense AI is an assistive review tool. AI findings may be incorrect or incomplete. "
    "Always verify recommendations with a qualified reviewer and appropriate tests."
)
