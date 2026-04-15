# FinVault AI

**On-device financial intelligence. Private by design.**

FinVault AI is a fully local, air-gapped financial analysis workbench powered by Google Gemma 4 via LM Studio. It is built for finance professionals, auditors, and controllers who need to process sensitive accounting data under SOX-style controls — without ever sending data to the cloud.

> SOX-Compliant Secure AI in 30 Minutes: A Practical Guide to Financial Data Analysis with Local-First Gemma 4

---

## Features

- **Report Generator** — Executive summaries, ledger analysis, expense breakdowns, cash-flow summaries, variance reports, and monthly trend analyses grounded in your uploaded data.
- **Natural-Language Data Query** — Ask questions of CSV / Excel ledgers in plain English; the model shows its calculations step-by-step and flags anomalies.
- **Document OCR** — Extract structured fields from invoices, work orders, purchase orders, and receipts using Tesseract + Gemma vision parsing.
- **Zero Cloud** — All inference runs locally through LM Studio on `localhost:1234`. No telemetry, no external API calls.

## Requirements

- Python 3.9+
- [LM Studio](https://lmstudio.ai) with a Gemma model loaded and the local server enabled
- [Tesseract OCR](https://tesseract-ocr.github.io/) available on `PATH`

## Installation

```bash
git clone https://github.com/<your-org>/FinVaultAI.git
cd FinVaultAI
pip install -r requirements.txt
```

Install Tesseract (macOS):

```bash
brew install tesseract
```

## Running

1. Start LM Studio, load a Gemma model, and enable the local server (default `http://localhost:1234/v1`).
2. Launch the app:

```bash
streamlit run app.py
```

Or use the convenience launcher:

```bash
./scripts/start.sh
```

The UI opens at `http://localhost:8501`.

## Project layout

```
app.py              Streamlit entry point
config/settings.py  App constants, prompts, LM Studio endpoint
core/               llm_client, report_generator, data_query, ocr_engine
ui/                 sidebar + three feature tabs (reports, query, OCR)
utils/              data loaders, formatters
scripts/            launcher, sample generators, screenshotting
sample_data/        example CSVs, invoices, POs, receipts for demo
docs/               marketing / technical collateral
```

## Configuration

Override defaults in [`config/settings.py`](config/settings.py):

- `LM_STUDIO_BASE_URL` — point to a different LM Studio host/port
- `DEFAULT_TEMPERATURE`, `REPORT_MAX_TOKENS` — tune generation
- `SUPPORTED_DATA_TYPES`, `SUPPORTED_IMAGE_TYPES` — allowed uploads
- `REPORT_TYPES`, `DOC_TYPES`, `PARSE_TEMPLATES` — customize available reports and OCR extraction schemas

## Security posture

- No outbound network calls from the app process except to `localhost:1234` (LM Studio).
- Uploaded files are held in Streamlit's per-session memory and are not persisted unless you save them explicitly.
- `.gitignore` excludes `uploads/`, `exports/`, and `generated_reports/` so analyst data never enters version control.

## License

Proprietary — internal use. Contact the maintainer before redistribution.
