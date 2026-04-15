"""
FinVault AI
===========
On-device financial intelligence. Private by design.

Features: Report Generation | NL Data Query | OCR Document Parsing
Engine:   Google Gemma 4 via LM Studio (100 % local)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from config.settings import APP_NAME, APP_TAGLINE, APP_VERSION

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_NAME} — Secure Financial AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS — dark theme with indigo accent
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ---- Hide streamlit defaults ---- */
    #MainMenu {visibility:hidden}
    header[data-testid="stHeader"] {background:transparent}

    /* ---- Typography ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {font-family:'Inter',sans-serif}

    /* ---- App header ---- */
    .fv-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
        border: 1px solid #6366f125;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .fv-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, #6366f115, transparent 70%);
    }
    .fv-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #c7d2fe, #a5b4fc, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }
    .fv-tagline {
        color: #94a3b8;
        font-size: .9rem;
        margin: 4px 0 0;
    }
    .fv-badge-row {
        display: flex;
        gap: 8px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .fv-badge {
        font-size: .68rem;
        font-weight: 600;
        padding: 3px 12px;
        border-radius: 20px;
        letter-spacing: .3px;
    }
    .fv-badge-green {
        background: #22c55e18;
        border: 1px solid #22c55e35;
        color: #4ade80;
    }
    .fv-badge-indigo {
        background: #6366f118;
        border: 1px solid #6366f135;
        color: #a5b4fc;
    }
    .fv-badge-amber {
        background: #f59e0b18;
        border: 1px solid #f59e0b35;
        color: #fbbf24;
    }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #1a1c2e;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: .85rem;
        color: #94a3b8;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        color: #fff !important;
    }

    /* ---- Buttons ---- */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all .2s;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338ca, #4f46e5);
        box-shadow: 0 4px 20px #6366f140;
    }

    /* ---- Metric cards ---- */
    [data-testid="stMetricValue"] {font-size:1.1rem;font-weight:700}

    /* ---- Expanders ---- */
    [data-testid="stExpander"] {
        border: 1px solid #334155;
        border-radius: 12px;
    }

    /* ---- Chat messages ---- */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        border: 1px solid #33415520;
    }

    /* ---- Footer ---- */
    .fv-footer {
        text-align: center;
        padding: 20px 0 10px;
        color: #475569;
        font-size: .72rem;
        border-top: 1px solid #1e293b;
        margin-top: 24px;
    }
    .fv-footer a {color:#818cf8;text-decoration:none}

    /* ---- Scrollbar ---- */
    ::-webkit-scrollbar {width:6px}
    ::-webkit-scrollbar-track {background:#0f1117}
    ::-webkit-scrollbar-thumb {background:#334155;border-radius:3px}

    /* ---- File uploader ---- */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Import modules
# ---------------------------------------------------------------------------
from ui.sidebar import render as render_sidebar
from ui.tab_reports import render as render_reports
from ui.tab_query import render as render_query
from ui.tab_ocr import render as render_ocr

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
lm_state = render_sidebar()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="fv-header">
    <div class="fv-title">{APP_NAME}</div>
    <div class="fv-tagline">{APP_TAGLINE}</div>
    <div class="fv-badge-row">
        <span class="fv-badge fv-badge-green">&#x2022; Air-Gapped</span>
        <span class="fv-badge fv-badge-indigo">&#x1f9e0; Gemma 4 Powered</span>
        <span class="fv-badge fv-badge-amber">&#x1f512; Zero Cloud</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_report, tab_query, tab_ocr = st.tabs([
    "Report Generator",
    "Data Query",
    "Document OCR",
])

with tab_report:
    render_reports(lm_state)

with tab_query:
    render_query(lm_state)

with tab_ocr:
    render_ocr(lm_state)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    f'<div class="fv-footer">'
    f'{APP_NAME} v{APP_VERSION} &mdash; '
    f'All processing runs locally. No data is transmitted. '
    f'Powered by Google Gemma via LM Studio.'
    f'</div>',
    unsafe_allow_html=True,
)
