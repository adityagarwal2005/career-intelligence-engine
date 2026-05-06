#!/usr/bin/env python
"""
Career Intelligence Suite - Main Entry Point

Run the Streamlit application with:
    python run.py
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
    
    print("Starting Career Intelligence Suite...")
    print(f"Local URL: http://127.0.0.1:8501")
    print("")
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path)],
        check=False
    )

if __name__ == "__main__":
    main()
