"""Phase 3 preprocessing utilities.

Handles missing values, performs categorical encoding, and prepares
ML-ready feature and target datasets.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


FEATURE_COLUMNS = ["time", "weather", "road_type"]
TARGET_COLUMN = "severity"
TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}


def clean_accident_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw accident data for preprocessing.

    Steps:
    - Keep expected columns only.
    - Drop duplicate rows.
    - Fill missing categorical values using mode (fallback: Unknown).
    """
    expected = FEATURE_COLUMNS + [TARGET_COLUMN]
    cleaned = df.copy()

    # Keep only expected project columns that exist.
    existing = [col for col in expected if col in cleaned.columns]
    cleaned = cleaned[existing].copy()

    # Add any missing columns to maintain stable schema.
    for col in expected:
        if col not in cleaned.columns:
            cleaned[col] = pd.NA

    cleaned = cleaned[expected]
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    for col in expected:
        if cleaned[col].isna().any() or (cleaned[col].astype(str).str.strip() == "").any():
            non_null_mode = cleaned[col].dropna().mode()
            fill_value = non_null_mode.iloc[0] if not non_null_mode.empty else "Unknown"
            cleaned[col] = cleaned[col].replace("", pd.NA).fillna(fill_value)

    return cleaned


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical feature columns using one-hot encoding."""
    return pd.get_dummies(df[FEATURE_COLUMNS], prefix=FEATURE_COLUMNS)


def build_ml_dataset(clean_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Create ML-ready X and y where y is numeric severity class."""
    x = encode_features(clean_df)
    y = clean_df[TARGET_COLUMN].map(TARGET_MAP)

    if y.isna().any():
        unknown_values = clean_df.loc[y.isna(), TARGET_COLUMN].unique().tolist()
        raise ValueError(
            f"Found unknown target class values in severity: {unknown_values}. "
            "Expected only Low/Medium/High."
        )

    y = y.astype(int)
    return x, y


def save_preprocessing_outputs(
    clean_df: pd.DataFrame,
    x: pd.DataFrame,
    y: pd.Series,
    output_dir: str | Path,
) -> None:
    """Save cleaned and ML-ready datasets to disk."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    clean_df.to_csv(output_path / "accident_clean.csv", index=False)

    encoded_df = x.copy()
    encoded_df["severity_target"] = y
    encoded_df.to_csv(output_path / "accident_encoded.csv", index=False)
