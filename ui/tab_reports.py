"""
Tab: Report Generator — FinVault AI
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.settings import REPORT_TYPES
from core.llm_client import LMStudioState
from core.report_generator import generate_report
from utils.data_loader import load_uploaded, load_sample_csv, get_sample_files
from utils.formatters import quick_metrics, dataframe_info


def render(state: LMStudioState):
    st.markdown(
        '<p style="color:#94a3b8;margin-top:-8px;margin-bottom:16px">'
        'Upload accounting data and generate professional internal reports '
        'powered by on-device AI.</p>',
        unsafe_allow_html=True,
    )

    # ---- Data input ----
    col_up, col_sample = st.columns([3, 1])
    with col_up:
        uploaded = st.file_uploader(
            "Upload accounting data",
            type=["csv", "xlsx", "xls"],
            key="rpt_upload",
        )
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        use_sample = st.checkbox("Use sample data", key="rpt_sample")

    df: pd.DataFrame | None = None
    if use_sample:
        samples = get_sample_files()
        if samples:
            chosen = st.selectbox("Sample file", samples, key="rpt_sample_file")
            df = load_sample_csv(chosen)
    elif uploaded:
        df = load_uploaded(uploaded)

    if df is None:
        # Empty state
        st.markdown(
            '<div style="text-align:center;padding:50px 20px;'
            'border:1px dashed #334155;border-radius:12px;margin:20px 0">'
            '<div style="font-size:2.5rem;margin-bottom:8px">&#128202;</div>'
            '<div style="color:#e2e8f0;font-size:1rem;font-weight:600">No data loaded</div>'
            '<div style="color:#64748b;font-size:.85rem;margin-top:4px">'
            'Upload a CSV / Excel file or check <b>Use sample data</b> to begin</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    # ---- Preview ----
    with st.expander(f"Data Preview  ({dataframe_info(df)})", expanded=True):
        st.dataframe(df, use_container_width=True, height=260)

    # ---- Quick metrics ----
    metrics = quick_metrics(df)
    if metrics:
        cols = st.columns(min(len(metrics), 5))
        for i, m in enumerate(metrics[:5]):
            with cols[i]:
                st.markdown(
                    f'<div style="background:#1e1b4b30;border:1px solid #6366f125;'
                    f'border-radius:10px;padding:12px 14px">'
                    f'<div style="font-size:.65rem;color:#818cf8;font-weight:600;'
                    f'letter-spacing:.6px;text-transform:uppercase">{m["label"]}</div>'
                    f'<div style="font-size:1.1rem;color:#e2e8f0;font-weight:700;'
                    f'margin-top:2px">{m["value"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ---- Chart ----
    cat_col = next((c for c in df.columns if c.lower() == "category"), None)
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if cat_col and num_cols:
        val_col = next((c for c in num_cols if "debit" in c.lower()), num_cols[0])
        chart_df = df.groupby(cat_col)[val_col].sum().reset_index()
        fig = px.bar(
            chart_df, x=cat_col, y=val_col,
            title=f"{val_col} by {cat_col}",
            color=cat_col,
            color_discrete_sequence=px.colors.sequential.Purples_r,
        )
        fig.update_layout(
            showlegend=False, height=340,
            margin=dict(t=40, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#94a3b8",
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---- Report config ----
    rcol1, rcol2 = st.columns([2, 3])
    with rcol1:
        report_type = st.selectbox("Report Type", REPORT_TYPES, key="rpt_type")
    with rcol2:
        extra = st.text_area(
            "Additional instructions (optional)",
            placeholder="e.g., Focus on Q1 trends, flag anomalies over $10k ...",
            key="rpt_extra",
            height=80,
        )

    # ---- Generate ----
    if st.button("Generate Report", type="primary", key="rpt_go", use_container_width=True):
        temp = st.session_state.get("llm_temperature", 0.15)
        with st.spinner("AI is analysing your data ..."):
            report = generate_report(state, df, report_type, extra, temp)

        st.markdown("---")
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">'
            '<span style="font-size:1.2rem">&#128196;</span>'
            '<span style="font-size:1.1rem;font-weight:700;color:#e2e8f0">Generated Report</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(report)

        st.download_button(
            "Download Report (.txt)",
            data=report,
            file_name=f"{report_type.lower().replace(' ', '_')}_report.txt",
            mime="text/plain",
            key="rpt_dl",
        )
