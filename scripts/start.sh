#!/bin/bash
cd /Users/srijonm/Documents/LocalGemmaApp
export PATH="/opt/homebrew/bin:/Users/srijonm/Library/Python/3.9/bin:$PATH"
exec streamlit run app.py --server.headless true --server.port 8501
