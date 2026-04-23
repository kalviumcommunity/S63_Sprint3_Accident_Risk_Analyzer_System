"""Phase 1 runner script.

Connects to MongoDB, fetches accident data, and prints DataFrame preview.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.fetch_data import load_accident_dataframe


def main() -> None:
    df = load_accident_dataframe()

    print("Phase 1 - Data Connection Result")
    print(f"Total rows fetched: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    main()
