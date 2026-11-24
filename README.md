# CodeSense AI

An AI-assisted code review prototype built with Python, LangChain and Mistral.

## Features

- Focused AI reviews for bugs, security, performance and code quality.
- LangChain LCEL composition, RunnableParallel, RunnableLambda and RunnableBranch.
- Pydantic structured output.
- Optional Ruff and Bandit static analysis for Python.
- Streamlit interface.
- Markdown and JSON report downloads.

## Important limitations

- Version 1 supports Python only.
- AI findings are suggestions, not proof of defects or vulnerabilities.
- Static analysis complements AI review; it does not guarantee security.
- Submitted code is never intentionally executed by this application.
- Do not submit confidential, classified, proprietary or secret-bearing code to an external API unless your organization explicitly authorizes it.
- This prototype is not a substitute for an approved secure software development process.

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your Mistral API key.

## Run

```powershell
streamlit run app.py
```

## Run tests

```powershell
pytest -q
```

## Architecture

Streamlit UI -> input validation -> LangChain review orchestrator -> Mistral structured review.
For Python, Ruff and Bandit run separately as static analyzers. Their findings are combined with AI findings in the final report.

## LangChain concepts demonstrated

- `ChatMistralAI`
- `ChatPromptTemplate`
- LCEL (`prompt | model`)
- `RunnableParallel`
- `RunnableLambda`
- `RunnableBranch`
- `.invoke()`

The current interface uses synchronous invocation. Streaming and batch examples can be added as follow-up learning exercises.
