# SKILLS.md

FinVault AI's product skills — what the app does, how each capability is wired, and where to extend it.

All skills run locally through LM Studio (`http://localhost:1234/v1`) using the OpenAI-compatible API. No external calls.

---

## 1. Report Generator

**Purpose:** Produce structured internal financial reports from uploaded ledger data.

- **Entry point:** [`ui/tab_reports.py`](ui/tab_reports.py)
- **Engine:** [`core/report_generator.py`](core/report_generator.py)
- **Inputs:** CSV / XLSX / XLS (see `SUPPORTED_DATA_TYPES`)
- **Report types** (from `config/settings.py` → `REPORT_TYPES`):
  - Executive Summary
  - Detailed Ledger Analysis
  - Expense Breakdown
  - Revenue vs. Expense Comparison
  - Cash Flow Summary
  - Monthly Trend Analysis
  - Budget Variance Report
- **System prompt:** `SYSTEM_PROMPT_REPORT` — CPA persona, GAAP/IFRS terminology, structured sections (Executive Summary, Key Metrics, Detailed Analysis, Anomalies & Risks, Recommendations).
- **Tuning knobs:** `REPORT_MAX_TOKENS` (default 3072), `DEFAULT_TEMPERATURE` (default 0.15).

**Extending:** add a new label to `REPORT_TYPES` and, if it needs tailored framing, extend the prompt assembly in `core/report_generator.py`.

---

## 2. Natural-Language Data Query

**Purpose:** Let users ask questions of their tabular data in plain English and get step-by-step numeric answers.

- **Entry point:** [`ui/tab_query.py`](ui/tab_query.py)
- **Engine:** [`core/data_query.py`](core/data_query.py)
- **Inputs:** same formats as Report Generator
- **System prompt:** `SYSTEM_PROMPT_QUERY` — answers **only** from the provided data, shows calculations, formats money as `$X,XXX.XX`, flags anomalies.
- **Data window:** `MAX_CSV_SIZE_FOR_PROMPT` (8,000 chars) bounds the slice sent to the model.
- **Preview:** first `MAX_ROWS_PREVIEW` (500) rows shown to the user.

**Extending:** for larger datasets, introduce a retrieval step (RAG over row chunks) in `core/data_query.py` rather than raising the prompt cap.

---

## 3. Document OCR & Parsing

**Purpose:** Digitize financial documents and extract structured fields.

- **Entry point:** [`ui/tab_ocr.py`](ui/tab_ocr.py)
- **Engine:** [`core/ocr_engine.py`](core/ocr_engine.py)
- **Pipeline:**
  1. Tesseract extracts raw text (`TESSERACT_CONFIG = "--psm 6 --oem 3"`)
  2. Gemma vision fallback parses scans where OCR confidence is low (`SYSTEM_PROMPT_OCR_VISION`)
  3. Gemma parses OCR text into structured fields (`SYSTEM_PROMPT_OCR_PARSE`)
- **Supported image types:** `png, jpg, jpeg, tiff, bmp, webp`
- **Document types** (from `DOC_TYPES`) with tailored extraction templates in `PARSE_TEMPLATES`:
  - **Invoice** — invoice #, dates, vendor, bill-to, line items, subtotal/tax/total, payment terms, bank details
  - **Work Order** — WO #, requester, assignee, priority, materials, labor, estimated cost, status
  - **Receipt** — vendor, date/time, items, subtotal/tax/total, payment method
  - **Purchase Order** — PO #, vendor, ship-to/bill-to, line items, shipping/tax, delivery date
  - **General Document** — generic key-information extractor

**Extending:** to add a new document type, append it to `DOC_TYPES` and add a matching entry in `PARSE_TEMPLATES`. No code changes required in `core/ocr_engine.py`.

---

## Cross-cutting guarantees

- **Local-only:** every call goes to `LM_STUDIO_BASE_URL`. No network traffic to Anthropic, OpenAI, Google, or any SaaS.
- **Session-scoped data:** uploads live in Streamlit session state only; nothing persists to disk unless the user explicitly exports.
- **Deterministic-leaning generation:** `DEFAULT_TEMPERATURE = 0.15` to favor precise, reproducible accounting output.
- **Air-gap compatible:** once LM Studio and Tesseract are installed, the app runs with no network connection.

---

## Roadmap of future skills

| Quarter | Focus |
|---------|-------|
| Q2 2026 | Core platform — Reports, Query, OCR (shipped) |
| Q3 2026 | RAG pipeline, anomaly detection |
| Q4 2026 | Enterprise features, multi-user |
| Q1 2027 | Observability, advanced agents |

See [`docs/FinVault_AI_Technical_Guide.docx`](docs/FinVault_AI_Technical_Guide.docx) for detailed roadmap commitments.
