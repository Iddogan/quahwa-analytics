"""
Quahwa Analytics - Main Streamlit App Entry Point
This file is used by Streamlit Cloud deployment

Na cloud-u će omogućiti upload Excel fajlova.
Lokalno će automatski učitati iz data/ foldera.
"""
import sys
from pathlib import Path

# Add src and dashboard to path
src_path = Path(__file__).parent / 'src'
dashboard_path = Path(__file__).parent / 'dashboard'
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(dashboard_path))

# Run the complete app
exec(open(dashboard_path / 'app_complete.py', encoding='utf-8').read())
