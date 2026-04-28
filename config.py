"""Project-wide configuration and constants.

Centralizes paths and shared settings so every phase script can import
from a single location instead of hard-coding values.
"""

from __future__ import annotations

from pathlib import Path

# ── Project root ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent

# ── Data paths ────────────────────────────────────────────────────────
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw_data"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed_data"
MODEL_DIR = PROJECT_ROOT / "data" / "models"

ENCODED_DATASET_PATH = PROCESSED_DATA_DIR / "accident_encoded.csv"
CLEAN_DATASET_PATH = PROCESSED_DATA_DIR / "accident_clean.csv"
MODEL_ARTIFACT_PATH = MODEL_DIR / "accident_random_forest_model.joblib"

# ── EDA paths ─────────────────────────────────────────────────────────
EDA_PLOTS_DIR = PROJECT_ROOT / "02_Exploratory_Data_Analysis" / "plots"

# ── Dataset schema ────────────────────────────────────────────────────
FEATURE_COLUMNS = ["time", "weather", "road_type"]
TARGET_COLUMN = "severity"

# ── Target class mapping ─────────────────────────────────────────────
TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
INVERSE_TARGET_MAP = {v: k for k, v in TARGET_MAP.items()}

# ── Time / severity labels (shared by EDA & frontend) ────────────────
TIME_ORDER = ["Morning", "Afternoon", "Evening", "Night"]
WEATHER_OPTIONS = ["Clear", "Rain", "Fog"]
ROAD_TYPE_OPTIONS = ["Highway", "City", "Rural"]
SEVERITY_LEVELS = ["Low", "Medium", "High"]
