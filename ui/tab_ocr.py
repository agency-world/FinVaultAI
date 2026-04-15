"""
Tab: OCR — Invoice & Work-Order Processing — FinVault AI
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image

from config.settings import (
    DOC_TYPES,
    PARSE_TEMPLATES,
    SYSTEM_PROMPT_OCR_PARSE,
    SYSTEM_PROMPT_OCR_VISION,
    SUPPORTED_IMAGE_TYPES,
)
from core.llm_client import LMStudioState, chat, vision_chat
from core.ocr_engine import (
    is_tesseract_available,
    extract_with_details,
    preprocess_for_ocr,
)


SAMPLE_IMG_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def _list_sample_images() -> list[str]:
    return sorted(
        p.name for p in SAMPLE_IMG_DIR.iterdir()
        if p.suffix.lstrip(".").lower() in SUPPORTED_IMAGE_TYPES
    )


def render(state: LMStudioState):
    st.markdown(
        '<p style="color:#94a3b8;margin-top:-8px;margin-bottom:16px">'
        'Upload scanned invoices, work-orders, or receipts. '
        'Text is extracted locally with Tesseract, then the AI parses structured fields.</p>',
        unsafe_allow_html=True,
    )

    # ---- OCR engine status ----
    _ocr_ok = is_tesseract_available()
    if not _ocr_ok:
        st.markdown(
            '<div style="background:#f59e0b15;border:1px solid #f59e0b30;'
            'border-radius:10px;padding:12px 16px;margin-bottom:14px">'
            '<span style="color:#fbbf24;font-weight:600;font-size:.85rem">'
            'Tesseract OCR not detected</span> '
            '<span style="color:#94a3b8;font-size:.8rem">'
            '&mdash; AI vision will be used as fallback. '
            'Install for best accuracy: <code>brew install tesseract</code></span>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ---- Document type + Upload ----
    c1, c2 = st.columns([1, 2])
    with c1:
        doc_type = st.selectbox("Document Type", DOC_TYPES, key="ocr_doc_type")
    with c2:
        st.markdown("")  # spacer

    col_up, col_sample = st.columns([3, 1])
    with col_up:
        uploaded = st.file_uploader(
            "Drop images here",
            type=SUPPORTED_IMAGE_TYPES,
            accept_multiple_files=True,
            key="ocr_upload",
        )
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        use_sample = st.checkbox("Use sample docs", key="ocr_sample")

    images: list[tuple[str, Image.Image]] = []

    if use_sample:
        sample_names = _list_sample_images()
        if sample_names:
            chosen = st.multiselect("Pick samples", sample_names, default=sample_names[:1])
            for name in chosen:
                images.append((name, Image.open(SAMPLE_IMG_DIR / name)))

    if uploaded:
        for f in uploaded:
            images.append((f.name, Image.open(f)))

    if not images:
        st.markdown(
            '<div style="text-align:center;padding:50px 20px;'
            'border:1px dashed #334155;border-radius:12px;margin:20px 0">'
            '<div style="font-size:2.5rem;margin-bottom:8px">&#128196;</div>'
            '<div style="color:#e2e8f0;font-size:1rem;font-weight:600">No documents loaded</div>'
            '<div style="color:#64748b;font-size:.85rem;margin-top:4px">'
            'Upload scanned images or check <b>Use sample docs</b></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        _render_manual_fallback(state, doc_type)
        return

    # ---- Process each image ----
    for idx, (name, image) in enumerate(images):
        st.markdown("---")
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
            f'<span style="background:#6366f120;color:#a5b4fc;padding:2px 10px;'
            f'border-radius:8px;font-size:.75rem;font-weight:600">DOC {idx+1}</span>'
            f'<span style="color:#e2e8f0;font-size:.9rem;font-family:monospace">{name}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col_img, col_res = st.columns([1, 1])

        with col_img:
            st.image(image, caption=name, use_container_width=True)

        with col_res:
            enhance = st.checkbox(
                "Pre-process (sharpen & upscale)",
                key=f"enhance_{idx}",
                help="Grayscale, sharpen, upscale for low-quality scans",
            )

            if st.button("Extract & Parse", key=f"ocr_go_{idx}", type="primary",
                          use_container_width=True):
                proc_img = preprocess_for_ocr(image) if enhance else image

                # Step 1: OCR
                extracted_text = ""
                confidence = 0.0

                if _ocr_ok:
                    with st.spinner("Running Tesseract OCR ..."):
                        result = extract_with_details(proc_img)
                        extracted_text = result["text"]
                        confidence = result["confidence"]

                    # Confidence badge
                    _conf_color = "#4ade80" if confidence > 70 else "#fbbf24" if confidence > 40 else "#f87171"
                    st.markdown(
                        f'<div style="display:flex;gap:16px;margin:8px 0">'
                        f'<div style="background:#1e1b4b30;border:1px solid #6366f120;'
                        f'border-radius:8px;padding:6px 12px;text-align:center">'
                        f'<div style="font-size:.58rem;color:#94a3b8;letter-spacing:.5px">CONFIDENCE</div>'
                        f'<div style="color:{_conf_color};font-size:.9rem;font-weight:700">{confidence}%</div>'
                        f'</div>'
                        f'<div style="background:#1e1b4b30;border:1px solid #6366f120;'
                        f'border-radius:8px;padding:6px 12px;text-align:center">'
                        f'<div style="font-size:.58rem;color:#94a3b8;letter-spacing:.5px">WORDS</div>'
                        f'<div style="color:#a5b4fc;font-size:.9rem;font-weight:700">{result["word_count"]}</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    with st.spinner("Using AI vision for text extraction ..."):
                        extracted_text = vision_chat(
                            state, SYSTEM_PROMPT_OCR_VISION,
                            "Extract all text from this document. Preserve layout.",
                            proc_img,
                        )

                if not extracted_text or not extracted_text.strip():
                    st.warning("No text extracted. Try pre-processing or a higher-res image.")
                    continue

                st.markdown(
                    '<div style="font-size:.75rem;color:#818cf8;font-weight:600;'
                    'letter-spacing:.5px;margin:10px 0 4px">RAW OCR OUTPUT</div>',
                    unsafe_allow_html=True,
                )
                st.text_area("", extracted_text, height=160, key=f"raw_{idx}",
                             label_visibility="collapsed")

                # Step 2: Gemma parsing
                with st.spinner("AI is parsing structured fields ..."):
                    temp = st.session_state.get("llm_temperature", 0.15)
                    max_tok = st.session_state.get("llm_max_tokens", 2048)
                    user_prompt = (
                        f"{PARSE_TEMPLATES[doc_type]}\n\n"
                        f"### OCR Text:\n```\n{extracted_text}\n```"
                    )
                    parsed = chat(
                        state,
                        system_prompt=SYSTEM_PROMPT_OCR_PARSE,
                        user_prompt=user_prompt,
                        temperature=temp,
                        max_tokens=max_tok,
                    )

                st.markdown(
                    '<div style="font-size:.75rem;color:#818cf8;font-weight:600;'
                    'letter-spacing:.5px;margin:14px 0 6px">PARSED STRUCTURED DATA</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(parsed)

                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button(
                        "Download Raw Text", extracted_text,
                        file_name=f"{name}_raw.txt", mime="text/plain",
                        key=f"dl_raw_{idx}", use_container_width=True,
                    )
                with dc2:
                    st.download_button(
                        "Download Parsed Data", parsed,
                        file_name=f"{name}_parsed.txt", mime="text/plain",
                        key=f"dl_parsed_{idx}", use_container_width=True,
                    )

    _render_manual_fallback(state, doc_type)


def _render_manual_fallback(state: LMStudioState, doc_type: str):
    with st.expander("Or paste document text manually"):
        manual = st.text_area("Paste text here", height=180, key="manual_ocr")
        if manual and st.button("Parse Text", key="manual_parse"):
            with st.spinner("Parsing ..."):
                temp = st.session_state.get("llm_temperature", 0.15)
                user_prompt = (
                    f"{PARSE_TEMPLATES[doc_type]}\n\n"
                    f"### Document Text:\n```\n{manual}\n```"
                )
                parsed = chat(
                    state,
                    system_prompt=SYSTEM_PROMPT_OCR_PARSE,
                    user_prompt=user_prompt,
                    temperature=temp,
                )
            st.markdown("**Parsed Data**")
            st.markdown(parsed)
            st.download_button(
                "Download", parsed,
                file_name="parsed_manual.txt", mime="text/plain",
                key="dl_manual",
            )
