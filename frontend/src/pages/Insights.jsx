import InsightsCharts from '../components/InsightsCharts';
import { insightsChartData } from '../data/projectSummary';

export default function Insights() {
  return (
    <div className="min-h-screen px-8 py-16 lg:px-12">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-12 animate-fade-in-up">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-blue-600">
            📊 Data Analysis
          </p>
          <h1 className="mt-3 text-3xl font-bold text-slate-900 md:text-4xl">
            Insights &amp; Visualizations
          </h1>
          <p className="mt-3 max-w-lg text-sm leading-relaxed text-slate-500">
            Explore accident distributions across time, weather, and severity
            levels derived from the processed dataset.
          </p>
        </div>

        {/* Charts */}
        <div className="animate-fade-in-up-delay">
          <InsightsCharts
            timeData={insightsChartData.timeData}
            weatherData={insightsChartData.weatherData}
            severityData={insightsChartData.severityData}
          />
        </div>
      </div>
    </div>
  );
}
