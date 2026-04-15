"""
LLM Client – thin wrapper around the OpenAI-compatible LM Studio API.
Handles connection, model discovery, chat completions, and vision requests.
"""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass, field
from typing import Optional

import streamlit as st
from openai import OpenAI
from PIL import Image

from config.settings import LM_STUDIO_BASE_URL, LM_STUDIO_API_KEY


# ---------------------------------------------------------------------------
# Connection state (cached in Streamlit session)
# ---------------------------------------------------------------------------
@dataclass
class LMStudioState:
    """Tracks the current LM Studio connection."""
    client: Optional[OpenAI] = None
    connected: bool = False
    model_id: Optional[str] = None
    model_list: list[str] = field(default_factory=list)
    error: Optional[str] = None


def connect(base_url: str = LM_STUDIO_BASE_URL) -> LMStudioState:
    """Attempt to connect to LM Studio and discover loaded models."""
    state = LMStudioState()
    state.client = OpenAI(base_url=base_url, api_key=LM_STUDIO_API_KEY)
    try:
        models = state.client.models.list()
        state.model_list = [m.id for m in models.data]
        if state.model_list:
            state.connected = True
            state.model_id = state.model_list[0]
        else:
            state.error = "Connected but no model loaded. Load a Gemma model in LM Studio."
    except Exception as exc:
        state.error = f"Cannot reach LM Studio at {base_url}: {exc}"
    return state


# ---------------------------------------------------------------------------
# Chat completion
# ---------------------------------------------------------------------------
def chat(
    state: LMStudioState,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.15,
    max_tokens: int = 2048,
) -> str:
    """Send a plain-text chat completion request."""
    if not state.connected or not state.model_id:
        return "⚠️ LM Studio is not connected. Please start LM Studio and load a Gemma model."
    try:
        resp = state.client.chat.completions.create(
            model=state.model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as exc:
        return f"❌ LM Studio error: {exc}"


# ---------------------------------------------------------------------------
# Vision completion (multimodal – Gemma 4 supports images)
# ---------------------------------------------------------------------------
def vision_chat(
    state: LMStudioState,
    system_prompt: str,
    user_text: str,
    image: Image.Image,
    temperature: float = 0.1,
    max_tokens: int = 2048,
) -> str:
    """Send an image + text to the model (multimodal chat)."""
    if not state.connected or not state.model_id:
        return "⚠️ LM Studio is not connected."

    # Encode image to base64 PNG
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    try:
        resp = state.client.chat.completions.create(
            model=state.model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                        {"type": "text", "text": user_text},
                    ],
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as exc:
        return f"❌ Vision request failed: {exc}"
