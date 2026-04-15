"""
Tab: Natural Language Data Query — FinVault AI
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from core.llm_client import LMStudioState
from core.data_query import ask
from utils.data_loader import load_uploaded, load_sample_csv, get_sample_files
from utils.formatters import dataframe_info


EXAMPLE_QUESTIONS = [
    "What is the total revenue for Q1 2026?",
    "Which category has the highest expenses?",
    "Show me all transactions above $50,000",
    "What is the net income (revenue minus all expenses)?",
    "Are there any months where the balance went negative?",
    "Summarize the cost of goods sold trend across months",
    "What percentage of total spend goes to employee salaries?",
    "Compare January vs. March revenue",
]


def render(state: LMStudioState):
    st.markdown(
        '<p style="color:#94a3b8;margin-top:-8px;margin-bottom:16px">'
        'Ask questions in plain English. The AI analyses your data '
        'and returns precise answers with calculations.</p>',
        unsafe_allow_html=True,
    )

    # ---- Data input ----
    col_up, col_sample = st.columns([3, 1])
    with col_up:
        uploaded = st.file_uploader(
            "Upload accounting data",
            type=["csv", "xlsx", "xls"],
            key="qry_upload",
        )
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        use_sample = st.checkbox("Use sample data", key="qry_sample")

    df: pd.DataFrame | None = None
    if use_sample:
        samples = get_sample_files()
        if samples:
            chosen = st.selectbox("Sample file", samples, key="qry_sample_file")
            df = load_sample_csv(chosen)
    elif uploaded:
        df = load_uploaded(uploaded)

    if df is None:
        st.markdown(
            '<div style="text-align:center;padding:50px 20px;'
            'border:1px dashed #334155;border-radius:12px;margin:20px 0">'
            '<div style="font-size:2.5rem;margin-bottom:8px">&#128172;</div>'
            '<div style="color:#e2e8f0;font-size:1rem;font-weight:600">No data loaded</div>'
            '<div style="color:#64748b;font-size:.85rem;margin-top:4px">'
            'Upload a CSV / Excel file or check <b>Use sample data</b> to begin querying</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    # ---- Preview (collapsed) ----
    with st.expander(f"Data Preview  ({dataframe_info(df)})", expanded=False):
        st.dataframe(df, use_container_width=True, height=220)

    # Column chips
    chip_html = " ".join(
        f'<span style="background:#1e1b4b50;border:1px solid #6366f130;'
        f'color:#a5b4fc;padding:2px 10px;border-radius:20px;'
        f'font-size:.7rem;font-family:monospace">{c}</span>'
        for c in df.columns
    )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 14px">{chip_html}</div>',
        unsafe_allow_html=True,
    )

    # ---- Chat history ----
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---- Example buttons ----
    with st.expander("Example questions", expanded=False):
        ecols = st.columns(2)
        for i, q in enumerate(EXAMPLE_QUESTIONS):
            col = ecols[i % 2]
            with col:
                if st.button(q, key=f"ex_{i}", use_container_width=True):
                    st.session_state["_pending_question"] = q
                    st.rerun()

    # ---- Chat input ----
    question = st.chat_input("Ask a question about your data ...")

    if "_pending_question" in st.session_state:
        question = st.session_state.pop("_pending_question")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Analysing ..."):
                temp = st.session_state.get("llm_temperature", 0.15)
                max_tok = st.session_state.get("llm_max_tokens", 2048)
                answer = ask(state, df, question, temp, max_tok)
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # ---- Clear ----
    if st.session_state.chat_history:
        if st.button("Clear conversation", key="qry_clear"):
            st.session_state.chat_history = []
            st.rerun()
