"""
Data Loader – handles CSV / Excel uploads and sample data loading.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def load_uploaded(uploaded_file) -> Optional[pd.DataFrame]:
    """Load an uploaded file (CSV or Excel) into a DataFrame."""
    if uploaded_file is None:
        return None
    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Upload CSV or Excel.")
            return None
    except Exception as exc:
        st.error(f"Error reading file: {exc}")
        return None


def load_sample_csv(filename: str = "sample_accounts.csv") -> pd.DataFrame:
    """Load one of the bundled sample CSV files."""
    return pd.read_csv(SAMPLE_DATA_DIR / filename)


def get_sample_files() -> list[str]:
    """List available sample CSV / Excel files."""
    return sorted(
        p.name
        for p in SAMPLE_DATA_DIR.iterdir()
        if p.suffix in {".csv", ".xlsx", ".xls"}
    )
