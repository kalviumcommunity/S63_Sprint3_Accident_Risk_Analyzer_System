"""Advanced EDA plots for Phase 2 (Chunk 2).

Creates line, scatter, and box plots with beginner-friendly insight text.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")

TIME_ORDER = ["Morning", "Afternoon", "Evening", "Night"]
SEVERITY_MAP = {"Low": 1, "Medium": 2, "High": 3}
TIME_MAP = {label: idx + 1 for idx, label in enumerate(TIME_ORDER)}


def _validate_columns(df: pd.DataFrame) -> None:
    required = ["time", "severity"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for advanced EDA: {missing}")


def create_line_plot(df: pd.DataFrame, output_dir: str | Path) -> str:
    """Create line plot for accident trend across time categories."""
    time_counts = df["time"].value_counts().reindex(TIME_ORDER, fill_value=0)

    plt.figure(figsize=(8, 5))
    ax = sns.lineplot(x=time_counts.index, y=time_counts.values, marker="o", linewidth=2)
    ax.set_title("Accident Trend by Time of Day", fontsize=14)
    ax.set_xlabel("Time")
    ax.set_ylabel("Accident Count")
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "line_trend_time.png", dpi=150)
    plt.close()

    peak_time = time_counts.idxmax()
    peak_count = int(time_counts.max())
    return f"Accident trend peaks at '{peak_time}' with {peak_count} accidents."


def create_scatter_plot(df: pd.DataFrame, output_dir: str | Path) -> str:
    """Create scatter plot for relationship between time and severity."""
    working_df = df.copy()
    working_df["time_code"] = working_df["time"].map(TIME_MAP)
    working_df["severity_code"] = working_df["severity"].map(SEVERITY_MAP)
    working_df = working_df.dropna(subset=["time_code", "severity_code"])

    plt.figure(figsize=(8, 5))
    ax = sns.scatterplot(
        data=working_df,
        x="time_code",
        y="severity_code",
        hue="severity",
        style="time",
        s=120,
        palette="Set1",
    )
    ax.set_title("Relationship Between Time and Severity", fontsize=14)
    ax.set_xlabel("Time Code (1=Morning, 2=Afternoon, 3=Evening, 4=Night)")
    ax.set_ylabel("Severity Code (1=Low, 2=Medium, 3=High)")
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "scatter_time_severity.png", dpi=150)
    plt.close()

    mean_by_time = (
        working_df.groupby("time", as_index=False)["severity_code"]
        .mean()
        .sort_values("severity_code", ascending=False)
    )
    top_time = mean_by_time.iloc[0]["time"]
    top_score = float(mean_by_time.iloc[0]["severity_code"])
    return f"Average severity is highest during '{top_time}' (mean severity score {top_score:.2f})."


def create_box_plot(df: pd.DataFrame, output_dir: str | Path) -> str:
    """Create box plot to inspect severity score outliers by road type."""
    working_df = df.copy()
    working_df["severity_code"] = working_df["severity"].map(SEVERITY_MAP)

    if "road_type" not in working_df.columns:
        working_df["road_type"] = "Unknown"

    plt.figure(figsize=(8, 5))
    ax = sns.boxplot(
        data=working_df,
        x="road_type",
        y="severity_code",
        hue="road_type",
        legend=False,
        palette="pastel",
    )
    ax.set_title("Severity Score Distribution by Road Type", fontsize=14)
    ax.set_xlabel("Road Type")
    ax.set_ylabel("Severity Code (1=Low, 2=Medium, 3=High)")
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "boxplot_severity_road_type.png", dpi=150)
    plt.close()

    q1 = working_df["severity_code"].quantile(0.25)
    q3 = working_df["severity_code"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = working_df[(working_df["severity_code"] < lower) | (working_df["severity_code"] > upper)]
    return (
        f"Outlier check using IQR found {len(outliers)} potential outlier(s) "
        f"in severity scores."
    )


def create_advanced_plots_with_insights(df: pd.DataFrame, output_dir: str | Path) -> Dict[str, str]:
    """Create all Phase 2 chunk 2 plots and return per-plot insights."""
    if df.empty:
        raise ValueError("DataFrame is empty. Cannot run advanced EDA plots.")

    _validate_columns(df)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    insights = {
        "line_plot": create_line_plot(df, output_path),
        "scatter_plot": create_scatter_plot(df, output_path),
        "box_plot": create_box_plot(df, output_path),
    }
    return insights
