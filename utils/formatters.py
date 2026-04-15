"""
Formatting helpers for the UI.
"""

from __future__ import annotations

import pandas as pd


def currency(value: float) -> str:
    """Format a number as USD currency string."""
    return f"${value:,.2f}"


def quick_metrics(df: pd.DataFrame) -> list[dict]:
    """
    Return a list of {label, value} dicts for numeric columns.
    Useful for st.metric cards.
    """
    metrics = []
    for col in df.select_dtypes(include="number").columns:
        total = df[col].sum()
        metrics.append({"label": col, "value": currency(total)})
    return metrics


def dataframe_info(df: pd.DataFrame) -> str:
    """One-line summary of a DataFrame."""
    return f"{len(df)} rows × {len(df.columns)} columns"
