"""
Report Generator – builds prompts for different financial report types
and calls Gemma to produce them.
"""

from __future__ import annotations

import pandas as pd

from config.settings import (
    SYSTEM_PROMPT_REPORT,
    REPORT_MAX_TOKENS,
    MAX_CSV_SIZE_FOR_PROMPT,
)
from core.llm_client import LMStudioState, chat


# ---------------------------------------------------------------------------
# Build the user prompt for a given report type
# ---------------------------------------------------------------------------
def _build_prompt(
    df: pd.DataFrame,
    report_type: str,
    custom_instructions: str = "",
) -> str:
    """Construct the user-facing prompt including data context."""

    csv_text = df.to_csv(index=False)
    if len(csv_text) > MAX_CSV_SIZE_FOR_PROMPT:
        csv_text = csv_text[:MAX_CSV_SIZE_FOR_PROMPT] + "\n... [truncated]"

    stats = df.describe(include="all").to_string()

    # Compute handy aggregates when known columns exist
    extras = ""
    cols_lower = {c.lower(): c for c in df.columns}
    if "debit" in cols_lower and "credit" in cols_lower:
        total_debit = df[cols_lower["debit"]].sum()
        total_credit = df[cols_lower["credit"]].sum()
        extras += (
            f"\n### Pre-computed Totals\n"
            f"- Total Debits : ${total_debit:,.2f}\n"
            f"- Total Credits: ${total_credit:,.2f}\n"
            f"- Net          : ${total_credit - total_debit:,.2f}\n"
        )
    if "category" in cols_lower:
        cat_col = cols_lower["category"]
        val_col = cols_lower.get("debit") or cols_lower.get("amount")
        if val_col:
            grp = df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)
            extras += f"\n### Spend by Category\n{grp.to_string()}\n"

    prompt = (
        f"Generate a **{report_type}** based on the following accounting data.\n\n"
        f"### Raw Data (CSV):\n```\n{csv_text}\n```\n\n"
        f"### Statistical Summary:\n```\n{stats}\n```\n"
        f"{extras}\n"
    )

    if custom_instructions:
        prompt += f"### Additional Instructions:\n{custom_instructions}\n\n"

    prompt += (
        "Produce a professional internal report suitable for C-suite distribution. "
        "Structure it with clear markdown headings, bullet points, and tables where useful. "
        "End with actionable recommendations."
    )
    return prompt


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate_report(
    state: LMStudioState,
    df: pd.DataFrame,
    report_type: str,
    custom_instructions: str = "",
    temperature: float = 0.15,
) -> str:
    """Generate a financial report using Gemma."""
    user_prompt = _build_prompt(df, report_type, custom_instructions)
    return chat(
        state,
        system_prompt=SYSTEM_PROMPT_REPORT,
        user_prompt=user_prompt,
        temperature=temperature,
        max_tokens=REPORT_MAX_TOKENS,
    )
