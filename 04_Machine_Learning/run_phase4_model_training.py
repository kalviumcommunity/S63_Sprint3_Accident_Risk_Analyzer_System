"""Phase 4 runner: train and evaluate the machine learning model."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.fetch_data import load_accident_dataframe
from src.preprocessing.preprocess_data import build_ml_dataset, clean_accident_data, save_preprocessing_outputs
from src.model.train_model import (
    build_feature_target_split,
    evaluate_model,
    load_encoded_dataset,
    save_model_and_report,
    split_train_test,
    train_random_forest,
)


PROCESSED_DATASET_PATH = PROJECT_ROOT / "data" / "processed_data" / "accident_encoded.csv"
MODEL_OUTPUT_DIR = PROJECT_ROOT / "data" / "models"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "04_Machine_Learning"


def get_or_create_encoded_dataset() -> Path:
    """Return the encoded dataset path, generating it if required."""
    if PROCESSED_DATASET_PATH.exists():
        return PROCESSED_DATASET_PATH

    raw_df = load_accident_dataframe()
    clean_df = clean_accident_data(raw_df)
    x, y = build_ml_dataset(clean_df)
    save_preprocessing_outputs(
        clean_df=clean_df,
        x=x,
        y=y,
        output_dir=PROJECT_ROOT / "data" / "processed_data",
    )
    return PROCESSED_DATASET_PATH


def main() -> None:
    dataset_path = get_or_create_encoded_dataset()
    encoded_df = load_encoded_dataset(dataset_path)

    x, y = build_feature_target_split(encoded_df)
    x_train, x_test, y_train, y_test = split_train_test(x, y)
    model = train_random_forest(x_train, y_train)
    metrics = evaluate_model(model, x_test, y_test)

    save_model_and_report(
        model=model,
        feature_columns=list(x.columns),
        metrics=metrics,
        model_dir=MODEL_OUTPUT_DIR,
        report_dir=REPORT_OUTPUT_DIR,
    )

    print("Phase 4 completed.")
    print(f"Dataset used: {dataset_path}")
    print(f"Train shape: {x_train.shape}")
    print(f"Test shape: {x_test.shape}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Model saved to: {MODEL_OUTPUT_DIR / 'accident_random_forest_model.joblib'}")
    print(f"Report saved to: {REPORT_OUTPUT_DIR / 'model_evaluation.txt'}")


if __name__ == "__main__":
    main()
