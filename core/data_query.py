"""
Data Query Engine – translates natural-language questions into
data-grounded answers using Gemma.
"""

from __future__ import annotations

import json

import pandas as pd

from config.settings import SYSTEM_PROMPT_QUERY, MAX_CSV_SIZE_FOR_PROMPT
from core.llm_client import LMStudioState, chat


def build_context(df: pd.DataFrame) -> str:
    """Build a concise data context string for the LLM."""
    col_info = {col: str(df[col].dtype) for col in df.columns}
    csv_text = df.to_csv(index=False)
    if len(csv_text) > MAX_CSV_SIZE_FOR_PROMPT:
        csv_text = csv_text[:MAX_CSV_SIZE_FOR_PROMPT] + "\n... [truncated]"

    return (
        f"### Dataset Columns & Types:\n```json\n{json.dumps(col_info, indent=2)}\n```\n\n"
        f"### Row Count: {len(df)}\n\n"
        f"### Data (CSV):\n```\n{csv_text}\n```"
    )


def ask(
    state: LMStudioState,
    df: pd.DataFrame,
    question: str,
    temperature: float = 0.15,
    max_tokens: int = 2048,
) -> str:
    """Answer a natural-language question about the dataframe."""
    context = build_context(df)
    user_prompt = (
        f"{context}\n\n"
        f"### Question:\n{question}\n\n"
        "Provide a clear, concise answer referencing specific numbers. "
        "Show calculation steps where applicable."
    )
    return chat(
        state,
        system_prompt=SYSTEM_PROMPT_QUERY,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
