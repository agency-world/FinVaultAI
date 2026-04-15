# CLAUDE.md

Instructions for Claude Code when working in this repository.

## Project

**FinVault AI** — a fully local, air-gapped Streamlit workbench for financial analysis powered by Google Gemma 4 via LM Studio. See [README.md](README.md) for user-facing docs.

## Architecture

- `app.py` — Streamlit entry point. Wires sidebar + three feature tabs.
- `config/settings.py` — single source of truth for constants, prompts, LM Studio endpoint. Change behavior here before touching feature code.
- `core/` — feature engines:
  - `llm_client.py` — OpenAI-SDK client pointed at `localhost:1234/v1`
  - `report_generator.py` — report synthesis from CSV/Excel
  - `data_query.py` — NL-over-tabular-data Q&A
  - `ocr_engine.py` — Tesseract + Gemma vision parsing
- `ui/` — Streamlit views (`sidebar.py`, `tab_reports.py`, `tab_query.py`, `tab_ocr.py`)
- `utils/` — `data_loader.py`, `formatters.py`
- `scripts/` — `start.sh` launcher, sample data / screenshot / docx generators
- `sample_data/` — curated demo CSVs and source documents (committed)
- `docs/` — marketing and technical collateral

## Running

```bash
pip install -r requirements.txt
brew install tesseract          # macOS
# Start LM Studio, load a Gemma model, enable local server
streamlit run app.py            # or: ./scripts/start.sh
```

Default LM Studio endpoint: `http://localhost:1234/v1` (override in `config/settings.py`).

## Conventions

- **No cloud calls.** Every inference path must hit `LM_STUDIO_BASE_URL` only. Do not add dependencies that phone home.
- **Prompts live in `config/settings.py`** under `SYSTEM_PROMPT_*` and `PARSE_TEMPLATES`. Edit there, not inline in `core/`.
- **Uploaded data is session-scoped.** Never persist user uploads to disk outside an explicit user-initiated export.
- **Styling** is a single `st.markdown(...)` block at the top of `app.py`. Keep the indigo/dark theme (`#6366F1` accent, `#1e1b4b` → `#312e81` gradient) consistent when adding UI.
- **File types** allowed for upload are governed by `SUPPORTED_DATA_TYPES` and `SUPPORTED_IMAGE_TYPES` — update those constants rather than hardcoding extensions.

## What not to do

- Don't add authentication, telemetry, analytics, or remote logging — this app's whole premise is local-only.
- Don't commit real financial data. `.gitignore` excludes `uploads/`, `exports/`, `generated_reports/`.
- Don't swap the OpenAI SDK for a cloud provider SDK — the OpenAI-compatible interface is used specifically because LM Studio serves it locally.
- Don't introduce frameworks (FastAPI, Flask, React). This stays a Streamlit monolith.

## Testing

There is no test suite yet. When adding one, mock LM Studio responses at the `core/llm_client.py` boundary — do not require a running model for CI.

## Related resources

- `SKILLS.md` — product capabilities and prompt/parse templates
- `docs/FinVault_AI_Technical_Guide.docx` — architecture deep-dive
- `docs/FinVault_AI_Marketing_Deck.pptx` — product overview
