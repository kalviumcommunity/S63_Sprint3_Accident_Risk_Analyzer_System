"""MongoDB connection utilities for Phase 1.

This module centralizes environment loading and database connection.
"""

from __future__ import annotations

import os
from typing import Tuple

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection


def get_mongodb_collection() -> Tuple[MongoClient, Collection]:
    """Create and return MongoDB client and target collection.

    Returns:
        Tuple[MongoClient, Collection]: Active MongoDB client and collection.

    Raises:
        ValueError: If required environment variables are missing.
    """
    load_dotenv()

    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB")
    collection_name = os.getenv("MONGODB_COLLECTION")

    if not mongodb_uri or not db_name or not collection_name:
        raise ValueError(
            "Missing MongoDB environment variables. "
            "Please set MONGODB_URI, MONGODB_DB, and MONGODB_COLLECTION in .env"
        )

    client = MongoClient(mongodb_uri)
    collection = client[db_name][collection_name]
    return client, collection
