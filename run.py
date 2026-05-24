#!/usr/bin/env python
"""
Career Intelligence Suite - Main Entry Point

This script is configured to run on Streamlit Cloud.
Locally, run with:
    streamlit run src/ui/app.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Streamlit application"""
    app_path = Path(__file__).parent / "src" / "ui" / "app.py"
    
    if not app_path.exists():
        print(f"Error: Application file not found at {app_path}")
        sys.exit(1)
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path)],
        check=False
    )

if __name__ == "__main__":
    main()
