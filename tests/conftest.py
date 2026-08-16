"""
Pytest Configuration & Fixtures for XYZ AI
Ensures isolated fresh database state for each test run.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "05_xyz_ai"))

import pytest
from shared.seed_data import generate_seed_data

@pytest.fixture(autouse=True)
def reset_database_state():
    """Resets the mock database to clean seed state before each test."""
    generate_seed_data()
    yield
