#!/usr/bin/env python3
"""Wrapper to set CWD before Streamlit initializes (works around sandbox restrictions)."""
import os
import sys

# Force CWD to the project directory BEFORE streamlit imports
os.chdir("/Users/srijonm/Documents/LocalGemmaApp")
sys.path.insert(0, "/Users/srijonm/Documents/LocalGemmaApp")

# Add homebrew to PATH for tesseract
os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("PATH", "")

from streamlit.web.cli import main
sys.argv = ["streamlit", "run", "/Users/srijonm/Documents/LocalGemmaApp/app.py",
            "--server.headless", "true", "--server.port", "8501"]
main()
