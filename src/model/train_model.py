"""Phase 4 machine learning utilities.

Loads the processed dataset, trains a RandomForestClassifier, evaluates it,
and saves the trained model artifact for later app usage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


TARGET_COLUMN = "severity_target"
MODEL_FILENAME = "accident_random_forest_model.joblib"
METRICS_FILENAME = "model_evaluation.txt"


def load_encoded_dataset(dataset_path: str | Path) -> pd.DataFrame:
    """Load the processed, encoded dataset from disk."""
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found at {path}. Run Phase 3 preprocessing first."
        )
    return pd.read_csv(path)


def build_feature_target_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Split encoded dataframe into features and target."""
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    x = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return x, y


def split_train_test(
    x: pd.DataFrame, y: pd.Series
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into train and test sets.

    A 50/50 split is used because the dataset is intentionally small.
    """
    return train_test_split(x, y, test_size=0.5, random_state=42, stratify=y)


def train_random_forest(x_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train the RandomForestClassifier model."""
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )
    model.fit(x_train, y_train)
    return model


def evaluate_model(
    model: RandomForestClassifier,
    x_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, object]:
    """Evaluate the trained model and return metrics."""
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, zero_division=0)
    matrix = confusion_matrix(y_test, predictions)

    return {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": matrix,
        "predictions": predictions,
    }


def save_model_and_report(
    model: RandomForestClassifier,
    feature_columns: list[str],
    metrics: Dict[str, object],
    model_dir: str | Path,
    report_dir: str | Path,
) -> None:
    """Persist the trained model and a readable evaluation report."""
    model_path = Path(model_dir)
    model_path.mkdir(parents=True, exist_ok=True)

    report_path = Path(report_dir)
    report_path.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "feature_columns": feature_columns,
        "target_map": {0: "Low", 1: "Medium", 2: "High"},
    }
    joblib.dump(artifact, model_path / MODEL_FILENAME)

    with open(report_path / METRICS_FILENAME, "w", encoding="utf-8") as file:
        file.write("Phase 4 - Model Evaluation\n")
        file.write("=" * 30 + "\n")
        file.write(f"Accuracy: {metrics['accuracy']:.4f}\n\n")
        file.write("Classification Report:\n")
        file.write(f"{metrics['classification_report']}\n")
        file.write("Confusion Matrix:\n")
        file.write(f"{metrics['confusion_matrix']}\n")
