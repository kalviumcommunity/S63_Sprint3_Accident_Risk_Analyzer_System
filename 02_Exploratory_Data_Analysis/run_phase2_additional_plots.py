"""Phase 2 runner (Chunk 2): line, scatter, and box plots with insights."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.fetch_data import load_accident_dataframe
from src.eda.advanced_plots import create_advanced_plots_with_insights


def main() -> None:
    df = load_accident_dataframe()

    insights = create_advanced_plots_with_insights(
        df=df,
        output_dir=PROJECT_ROOT / "02_Exploratory_Data_Analysis" / "plots",
    )

    insights_path = PROJECT_ROOT / "02_Exploratory_Data_Analysis" / "additional_plot_insights.txt"
    with open(insights_path, "w", encoding="utf-8") as file:
        file.write("Phase 2 (Chunk 2): Additional Plot Insights\n")
        file.write("=" * 50 + "\n")
        file.write(f"Total records analyzed: {len(df)}\n\n")
        file.write(f"line_plot: {insights['line_plot']}\n")
        file.write(f"scatter_plot: {insights['scatter_plot']}\n")
        file.write(f"box_plot: {insights['box_plot']}\n")

    print("Phase 2 (Chunk 2) completed.")
    print("Generated plots in: 02_Exploratory_Data_Analysis/plots")
    print("Saved insights to: 02_Exploratory_Data_Analysis/additional_plot_insights.txt")


if __name__ == "__main__":
    main()
