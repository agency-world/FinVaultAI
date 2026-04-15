"""
Sidebar component — FinVault AI
Connection status, Admin panel with model/token config.
"""

from __future__ import annotations

import streamlit as st

from config.settings import (
    APP_NAME, APP_VERSION,
    LM_STUDIO_BASE_URL,
    DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS,
    DEFAULT_TOP_P, DEFAULT_FREQUENCY_PENALTY, DEFAULT_PRESENCE_PENALTY,
)
from core.llm_client import connect, LMStudioState
from core.ocr_engine import is_tesseract_available


def render() -> LMStudioState:
    """Render the sidebar and return the current LMStudioState."""

    with st.sidebar:

        # ---- Logo / Branding ----
        st.markdown(
            '<div style="text-align:center;padding:8px 0 2px">'
            '<span style="font-size:2rem">&#x1f6e1;&#xfe0f;</span><br>'
            f'<span style="font-size:1.45rem;font-weight:800;'
            f'background:linear-gradient(135deg,#818cf8,#6366f1,#4f46e5);'
            f'-webkit-background-clip:text;-webkit-text-fill-color:transparent">'
            f'{APP_NAME}</span><br>'
            '<span style="font-size:.72rem;color:#94a3b8;letter-spacing:.5px">'
            'PRIVATE BY DESIGN</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="text-align:center;margin:6px 0 10px">'
            '<span style="background:linear-gradient(135deg,#22c55e33,#16a34a22);'
            'border:1px solid #22c55e44;color:#4ade80;padding:3px 12px;'
            'border-radius:20px;font-size:.7rem;font-weight:600;letter-spacing:.4px">'
            'OFFLINE &bull; AIR-GAPPED &bull; SECURE</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ===============================================================
        # CONNECTION
        # ===============================================================
        st.markdown(
            '<p style="font-size:.75rem;font-weight:700;color:#94a3b8;'
            'letter-spacing:1.2px;margin-bottom:4px">CONNECTION</p>',
            unsafe_allow_html=True,
        )

        base_url = st.text_input(
            "Endpoint",
            value=LM_STUDIO_BASE_URL,
            help="LM Studio local server URL",
            label_visibility="collapsed",
        )

        state = connect(base_url)

        if state.connected:
            model = st.selectbox(
                "Active Model",
                state.model_list,
                index=0,
                label_visibility="collapsed",
            )
            state.model_id = model

            # Status card
            st.markdown(
                '<div style="background:linear-gradient(135deg,#22c55e15,#16a34a10);'
                'border:1px solid #22c55e30;border-radius:10px;padding:10px 14px;'
                'margin:6px 0">'
                '<div style="display:flex;align-items:center;gap:8px">'
                '<span style="width:8px;height:8px;border-radius:50%;'
                'background:#22c55e;display:inline-block;box-shadow:0 0 6px #22c55e88"></span>'
                '<span style="color:#4ade80;font-size:.8rem;font-weight:600">Connected</span>'
                '</div>'
                f'<div style="color:#94a3b8;font-size:.72rem;margin-top:4px;'
                f'font-family:monospace">{model}</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        elif state.error:
            st.markdown(
                '<div style="background:#ef444415;border:1px solid #ef444430;'
                'border-radius:10px;padding:10px 14px;margin:6px 0">'
                '<div style="display:flex;align-items:center;gap:8px">'
                '<span style="width:8px;height:8px;border-radius:50%;'
                'background:#ef4444;display:inline-block"></span>'
                '<span style="color:#f87171;font-size:.8rem;font-weight:600">Disconnected</span>'
                '</div>'
                '<div style="color:#94a3b8;font-size:.7rem;margin-top:4px">'
                'Start LM Studio and load a model</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("No models loaded.")

        st.markdown("---")

        # ===============================================================
        # ADMIN SECTION
        # ===============================================================
        st.markdown(
            '<p style="font-size:.75rem;font-weight:700;color:#94a3b8;'
            'letter-spacing:1.2px;margin-bottom:4px">ADMIN</p>',
            unsafe_allow_html=True,
        )

        with st.expander("Model & Inference", expanded=True):
            # Model name display
            if state.connected:
                _model_display = state.model_id or "—"
                _family = "Gemma 4" if "gemma" in _model_display.lower() else "Unknown"
                st.markdown(
                    f'<div style="background:#1e1b4b40;border:1px solid #6366f130;'
                    f'border-radius:8px;padding:10px 12px;margin-bottom:10px">'
                    f'<div style="font-size:.65rem;color:#818cf8;font-weight:600;'
                    f'letter-spacing:.8px;margin-bottom:2px">ACTIVE MODEL</div>'
                    f'<div style="color:#e2e8f0;font-size:.85rem;font-weight:700">{_family}</div>'
                    f'<div style="color:#94a3b8;font-size:.68rem;font-family:monospace;'
                    f'word-break:break-all">{_model_display}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            temp = st.slider(
                "Temperature",
                0.0, 1.0, DEFAULT_TEMPERATURE, 0.05,
                help="Lower = deterministic (best for finance).",
            )
            max_tok = st.slider("Max Tokens", 256, 4096, DEFAULT_MAX_TOKENS, 128)
            top_p = st.slider("Top-P", 0.0, 1.0, DEFAULT_TOP_P, 0.05,
                               help="Nucleus sampling threshold.")

            st.session_state["llm_temperature"] = temp
            st.session_state["llm_max_tokens"] = max_tok
            st.session_state["llm_top_p"] = top_p

        with st.expander("System Health"):
            cols = st.columns(2)
            with cols[0]:
                _ocr_ok = is_tesseract_available()
                _ocr_color = "#4ade80" if _ocr_ok else "#f87171"
                _ocr_label = "Active" if _ocr_ok else "Missing"
                st.markdown(
                    f'<div style="text-align:center;padding:6px 0">'
                    f'<div style="font-size:.62rem;color:#94a3b8;letter-spacing:.6px">OCR ENGINE</div>'
                    f'<div style="color:{_ocr_color};font-size:.82rem;font-weight:700">{_ocr_label}</div>'
                    f'</div>', unsafe_allow_html=True,
                )
            with cols[1]:
                _conn_color = "#4ade80" if state.connected else "#f87171"
                _conn_label = "Online" if state.connected else "Offline"
                st.markdown(
                    f'<div style="text-align:center;padding:6px 0">'
                    f'<div style="font-size:.62rem;color:#94a3b8;letter-spacing:.6px">LLM SERVER</div>'
                    f'<div style="color:{_conn_color};font-size:.82rem;font-weight:700">{_conn_label}</div>'
                    f'</div>', unsafe_allow_html=True,
                )

            st.markdown(
                f'<div style="text-align:center;padding:4px 0">'
                f'<div style="font-size:.62rem;color:#94a3b8;letter-spacing:.6px">ENDPOINT</div>'
                f'<div style="color:#94a3b8;font-size:.68rem;font-family:monospace">{base_url}</div>'
                f'</div>', unsafe_allow_html=True,
            )

        with st.expander("About"):
            st.markdown(
                f'<div style="font-size:.75rem;color:#94a3b8;line-height:1.7">'
                f'<strong style="color:#e2e8f0">{APP_NAME}</strong> v{APP_VERSION}<br>'
                f'All inference runs locally via LM Studio.<br>'
                f'Zero data transmitted. Zero cloud dependencies.<br>'
                f'<span style="color:#818cf8">Designed for financial professionals.</span>'
                f'</div>', unsafe_allow_html=True,
            )

    return state
