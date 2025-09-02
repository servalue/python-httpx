"""Pytest configuration file."""

import sys
from pathlib import Path

# Add src directory to Python path so imports work
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))