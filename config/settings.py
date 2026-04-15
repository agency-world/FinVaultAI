"""
Application settings and constants — FinVault AI
"""

# ---------------------------------------------------------------------------
# App identity
# ---------------------------------------------------------------------------
APP_NAME = "FinVault AI"
APP_TAGLINE = "On-device financial intelligence. Private by design."
APP_VERSION = "3.0"

# ---------------------------------------------------------------------------
# LM Studio defaults
# ---------------------------------------------------------------------------
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"

# ---------------------------------------------------------------------------
# LLM defaults
# ---------------------------------------------------------------------------
DEFAULT_TEMPERATURE = 0.15
DEFAULT_MAX_TOKENS = 2048
REPORT_MAX_TOKENS = 3072
DEFAULT_TOP_P = 0.95
DEFAULT_FREQUENCY_PENALTY = 0.0
DEFAULT_PRESENCE_PENALTY = 0.0

# ---------------------------------------------------------------------------
# OCR settings
# ---------------------------------------------------------------------------
TESSERACT_CONFIG = "--psm 6 --oem 3"
SUPPORTED_IMAGE_TYPES = ["png", "jpg", "jpeg", "tiff", "bmp", "webp"]

# ---------------------------------------------------------------------------
# File upload limits
# ---------------------------------------------------------------------------
SUPPORTED_DATA_TYPES = ["csv", "xlsx", "xls"]
MAX_ROWS_PREVIEW = 500
MAX_CSV_SIZE_FOR_PROMPT = 8000

# ---------------------------------------------------------------------------
# Report types
# ---------------------------------------------------------------------------
REPORT_TYPES = [
    "Executive Summary",
    "Detailed Ledger Analysis",
    "Expense Breakdown",
    "Revenue vs. Expense Comparison",
    "Cash Flow Summary",
    "Monthly Trend Analysis",
    "Budget Variance Report",
]

# ---------------------------------------------------------------------------
# Document types for OCR
# ---------------------------------------------------------------------------
DOC_TYPES = [
    "Invoice",
    "Work Order",
    "Receipt",
    "Purchase Order",
    "General Document",
]

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_REPORT = (
    "You are an expert Certified Public Accountant (CPA) and financial analyst. "
    "You generate precise, professional internal financial reports. "
    "Use proper accounting terminology (GAAP/IFRS). "
    "Structure reports with clear sections: Executive Summary, Key Metrics, "
    "Detailed Analysis, Anomalies & Risks, and Recommendations. "
    "Always reference specific numbers from the data. "
    "Format monetary values with $ signs, commas, and two decimal places."
)

SYSTEM_PROMPT_QUERY = (
    "You are a financial data analyst AI. You have access to accounting data "
    "provided as CSV. Answer the user's question accurately using ONLY the data "
    "provided. Show your calculations step-by-step. "
    "Format monetary values as $X,XXX.XX. "
    "If the question cannot be answered from the data, say so clearly. "
    "If you spot anomalies or risks while answering, mention them briefly."
)

SYSTEM_PROMPT_OCR_PARSE = (
    "You are a financial document parser with expertise in invoices, work orders, "
    "purchase orders, and receipts. Extract structured data from OCR text accurately. "
    "Be precise with numbers, dates, and amounts. "
    "Return data in a clean, structured format with clear field labels. "
    "If a field is not found in the text, mark it as 'N/A'. "
    "Flag any suspicious or inconsistent values."
)

SYSTEM_PROMPT_OCR_VISION = (
    "You are an OCR assistant. Extract ALL text visible in this document image "
    "exactly as it appears. Preserve the layout, alignment, and structure as much "
    "as possible. Include every number, date, and text element."
)

# ---------------------------------------------------------------------------
# Parse templates per document type
# ---------------------------------------------------------------------------
PARSE_TEMPLATES = {
    "Invoice": (
        "Extract the following fields from this invoice:\n"
        "- Invoice Number\n- Invoice Date\n- Due Date\n"
        "- Vendor / Supplier Name & Address\n"
        "- Bill-To (Customer Name & Address)\n"
        "- Line Items table: Description | Qty | Unit Price | Amount\n"
        "- Subtotal\n- Tax (rate & amount)\n- Discount (if any)\n"
        "- Total Amount Due\n- Payment Terms\n- Bank / Payment Details"
    ),
    "Work Order": (
        "Extract the following fields from this work order:\n"
        "- Work Order Number\n- Date Issued\n- Requested By\n"
        "- Assigned To / Contractor\n- Priority Level\n"
        "- Description of Work\n- Location\n"
        "- Materials / Parts: Item | Qty | Cost\n"
        "- Labor: Description | Hours | Rate | Cost\n"
        "- Estimated Total Cost\n- Approved By\n- Status\n- Completion Date"
    ),
    "Receipt": (
        "Extract from this receipt:\n"
        "- Store / Vendor Name & Address\n- Date & Time\n"
        "- Items: Description | Qty | Price\n"
        "- Subtotal\n- Tax\n- Total\n- Payment Method\n"
        "- Transaction / Reference Number"
    ),
    "Purchase Order": (
        "Extract from this purchase order:\n"
        "- PO Number\n- PO Date\n- Vendor Name & Address\n"
        "- Ship-To Address\n- Bill-To Address\n"
        "- Line Items: Description | Qty | Unit Price | Total\n"
        "- Subtotal\n- Shipping\n- Tax\n- Grand Total\n"
        "- Delivery Date\n- Payment Terms\n- Authorized By"
    ),
    "General Document": (
        "Identify the document type and extract ALL key information including:\n"
        "- Document title/type\n- Reference numbers\n- Dates\n"
        "- Names and organizations\n- Monetary amounts\n"
        "- Line items or tables\n- Terms and conditions\n"
        "- Signatures or approvals"
    ),
}
