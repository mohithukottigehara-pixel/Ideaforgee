# CivicProof AI

CivicProof AI is a Streamlit MVP for understanding government notifications. It extracts notification details from PDF or pasted text, compares extracted identifiers and dates with a locally curated JSON reference set, and presents evidence, a plain-language explanation, eligibility guidance, and a checklist.

> **Important:** Automated analysis is informational. A reference match is not proof of authenticity, and a discrepancy is not proof of fraud. Always confirm decisions and deadlines with the issuing authority.

## Features

- PDF text extraction and pasted-text analysis (PDFs up to 10 MB).
- Structured extraction through Google Gemini using `google-genai`.
- Deterministic comparison with `data/official_references.json`.
- Official Match, Corroborated, Inconsistent, and Unverified statuses.
- Extracted dates, eligibility guidance, multilingual explanations (English, Kannada, Hindi), source passages, and action checklist.
- No live crawling or OCR; scanned PDFs without embedded text receive a clear message.
- Fictional demo reference clearly marked as simulated.

## Requirements

- Python 3.11 or compatible.
- A Gemini API key for AI extraction and explanations.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` in `.env` (or configure it using Streamlit secrets). Optionally set `GEMINI_MODEL`; the default is `gemini-2.5-flash`.

```bash
streamlit run app.py
```

Never commit `.env` or `.streamlit/secrets.toml`. For Streamlit Community Cloud, add `GEMINI_API_KEY` under **App settings → Secrets**.

## Add official reference documents

Add records to `data/official_references.json` using the example schema in that file. Use actual source documents and URLs only. Keep `related_document_ids` accurate and traceable. The included record is fictional test data and must not be presented as a real scheme.

Verification is intentionally deterministic: identifiers and dates are compared in Python. The Gemini model does not determine authenticity. A record absent from the curated data is reported as **Unverified**, which does not mean fake. The MVP only establishes version relationships when related records are present; it does not claim supersession from a mere similarity.

## Project structure

```text
app.py
requirements.txt
.env.example
.gitignore
modules/
  ai_analyzer.py
  citizen_assistant.py
  document_reader.py
  policy_compare.py
  verification.py
data/
  official_references.json
```

## Deployment

Create a GitHub repository, commit the source (excluding secrets), then create a Streamlit Community Cloud app pointed at `app.py`. Add `GEMINI_API_KEY` in the app's secret settings. The app reads its JSON reference file from the repository at runtime.

## Limitations

- The reference collection is local and small; the included reference is fictional.
- No OCR, live official-source discovery, or permanent upload storage is implemented.
- Applicability guidance is a cautious text comparison and is not an official determination.
- Translation quality depends on Gemini; preserve and consult the source notification for legally significant details.
