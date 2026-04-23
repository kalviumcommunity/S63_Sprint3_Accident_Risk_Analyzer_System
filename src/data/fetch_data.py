"""Data fetching utilities for Phase 1.

Fetches records from MongoDB and converts them into a pandas DataFrame.
"""

from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd

from src.data.connect_mongodb import get_mongodb_collection


REQUIRED_COLUMNS = ["time", "weather", "road_type", "severity"]


def fetch_accident_documents(limit: int | None = None) -> List[Dict[str, Any]]:
    """Fetch accident documents from MongoDB.

    Args:
        limit: Optional row limit for quick testing.

    Returns:
        List of accident documents.
    """
    client, collection = get_mongodb_collection()
    try:
        cursor = collection.find({}, {"_id": 0})
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(cursor)
    finally:
        client.close()


def documents_to_dataframe(documents: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert MongoDB documents to DataFrame and align schema.

    Args:
        documents: List of MongoDB documents.

    Returns:
        Clean pandas DataFrame with expected columns.
    """
    df = pd.DataFrame(documents)

    if df.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    # Keep only columns expected in this project.
    existing_columns = [col for col in REQUIRED_COLUMNS if col in df.columns]
    df = df[existing_columns].copy()

    # Add missing project columns as NaN to keep schema stable.
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[REQUIRED_COLUMNS]


def load_accident_dataframe(limit: int | None = None) -> pd.DataFrame:
    """Fetch records from MongoDB and return a clean DataFrame."""
    docs = fetch_accident_documents(limit=limit)
    return documents_to_dataframe(docs)
