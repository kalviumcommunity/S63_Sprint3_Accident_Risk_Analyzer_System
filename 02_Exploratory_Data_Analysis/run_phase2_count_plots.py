"""Phase 2 runner (Chunk 1): count plots and insights."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.fetch_data import load_accident_dataframe
from src.eda.count_plots import create_count_plots_with_insights


def main() -> None:
    df = load_accident_dataframe()

    insights = create_count_plots_with_insights(
        df=df,
        output_dir=PROJECT_ROOT / "02_Exploratory_Data_Analysis" / "plots",
    )

    insights_path = PROJECT_ROOT / "02_Exploratory_Data_Analysis" / "count_plot_insights.txt"
    with open(insights_path, "w", encoding="utf-8") as file:
        file.write("Phase 2 (Chunk 1): Count Plot Insights\n")
        file.write("=" * 45 + "\n")
        file.write(f"Total records analyzed: {len(df)}\n\n")

        for key in ["weather", "time", "road_type", "severity"]:
            file.write(f"{key}: {insights[key]}\n")

    print("Phase 2 (Chunk 1) completed.")
    print("Generated plots in: 02_Exploratory_Data_Analysis/plots")
    print("Saved insights to: 02_Exploratory_Data_Analysis/count_plot_insights.txt")


if __name__ == "__main__":
    main()
