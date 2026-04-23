"""Count plot generation for Phase 2 EDA.

This module creates required count plots and produces short insights for each plot.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")


PLOT_CONFIG = {
    "weather": {
        "title": "Accidents by Weather",
        "filename": "count_weather.png",
        "x_label": "Weather",
    },
    "time": {
        "title": "Accidents by Time of Day",
        "filename": "count_time.png",
        "x_label": "Time",
    },
    "road_type": {
        "title": "Accidents by Road Type",
        "filename": "count_road_type.png",
        "x_label": "Road Type",
    },
    "severity": {
        "title": "Severity Distribution",
        "filename": "count_severity.png",
        "x_label": "Severity",
    },
}


def _build_insight(df: pd.DataFrame, column: str) -> str:
    """Generate a simple insight sentence for one categorical column."""
    counts = df[column].value_counts(dropna=False)
    top_category = counts.index[0]
    top_count = int(counts.iloc[0])
    total = int(counts.sum())
    percentage = (top_count / total) * 100 if total else 0.0
    return (
        f"Most accidents are in '{top_category}' for '{column}' "
        f"({top_count}/{total}, {percentage:.1f}%)."
    )


def create_count_plots_with_insights(df: pd.DataFrame, output_dir: str | Path) -> Dict[str, str]:
    """Create required count plots and return insights.

    Args:
        df: Source accident DataFrame.
        output_dir: Folder to save plot images.

    Returns:
        Dict[str, str]: Mapping of plot column to generated insight.
    """
    if df.empty:
        raise ValueError("DataFrame is empty. Cannot run EDA count plots.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    insights: Dict[str, str] = {}

    for column, config in PLOT_CONFIG.items():
        if column not in df.columns:
            raise ValueError(f"Missing required column for EDA: {column}")

        plt.figure(figsize=(8, 5))
        ax = sns.countplot(data=df, x=column, hue=column, legend=False, palette="Set2")
        ax.set_title(config["title"], fontsize=14)
        ax.set_xlabel(config["x_label"])
        ax.set_ylabel("Accident Count")
        plt.tight_layout()
        plt.savefig(output_path / config["filename"], dpi=150)
        plt.close()

        insights[column] = _build_insight(df, column)

    return insights
