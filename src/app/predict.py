"""Prediction helpers for the Phase 6 Streamlit application."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import joblib
import pandas as pd


MODEL_PATH = Path("data/models/accident_random_forest_model.joblib")
RISK_LEVEL_MAP = {
    "Low": "Low Risk",
    "Medium": "Moderate Risk",
    "High": "High Risk",
}


def load_model_artifact(model_path: str | Path = MODEL_PATH) -> Dict[str, object]:
    """Load the trained model artifact from disk."""
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Model artifact not found at {path}. Run Phase 4 training first."
        )
    artifact = joblib.load(path)

    required_keys = {"model", "feature_columns", "target_map"}
    if not required_keys.issubset(artifact.keys()):
        raise ValueError("Model artifact is missing required keys.")

    return artifact


def build_encoded_input(
    time_value: str,
    weather_value: str,
    road_type_value: str,
    feature_columns: List[str],
) -> pd.DataFrame:
    """Build a one-row encoded input aligned to trained feature columns."""
    row = {column: 0 for column in feature_columns}

    candidate_features = [
        f"time_{time_value}",
        f"weather_{weather_value}",
        f"road_type_{road_type_value}",
    ]

    for feature in candidate_features:
        if feature in row:
            row[feature] = 1

    return pd.DataFrame([row], columns=feature_columns)


def predict_severity(
    time_value: str,
    weather_value: str,
    road_type_value: str,
    model_path: str | Path = MODEL_PATH,
) -> Dict[str, str]:
    """Predict accident severity and return user-friendly labels."""
    artifact = load_model_artifact(model_path)

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    target_map = artifact["target_map"]

    input_df = build_encoded_input(
        time_value=time_value,
        weather_value=weather_value,
        road_type_value=road_type_value,
        feature_columns=feature_columns,
    )

    prediction_index = int(model.predict(input_df)[0])
    severity_label = target_map.get(prediction_index, "Unknown")
    risk_level = RISK_LEVEL_MAP.get(severity_label, "Unknown Risk")

    return {
        "severity": severity_label,
        "risk_level": risk_level,
    }
