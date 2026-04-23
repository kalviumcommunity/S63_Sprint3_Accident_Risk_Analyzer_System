"""Phase 3 runner: data preprocessing."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.fetch_data import load_accident_dataframe
from src.preprocessing.preprocess_data import (
    build_ml_dataset,
    clean_accident_data,
    save_preprocessing_outputs,
)


def main() -> None:
    raw_df = load_accident_dataframe()
    clean_df = clean_accident_data(raw_df)
    x, y = build_ml_dataset(clean_df)

    save_preprocessing_outputs(
        clean_df=clean_df,
        x=x,
        y=y,
        output_dir=PROJECT_ROOT / "data" / "processed_data",
    )

    print("Phase 3 completed.")
    print(f"Raw records: {len(raw_df)}")
    print(f"Clean records: {len(clean_df)}")
    print(f"Feature matrix shape (X): {x.shape}")
    print(f"Target vector shape (y): {y.shape}")
    print("Saved: data/processed_data/accident_clean.csv")
    print("Saved: data/processed_data/accident_encoded.csv")


if __name__ == "__main__":
    main()
