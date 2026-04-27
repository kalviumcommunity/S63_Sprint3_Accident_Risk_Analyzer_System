import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const palette = ['#2563eb', '#0ea5e9', '#14b8a6', '#f59e0b']

function ChartCard({ title, subtitle, children }) {
  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      <p className="mt-1 text-sm text-slate-600">{subtitle}</p>
      <div className="mt-5 h-72">{children}</div>
    </article>
  )
}

export default function InsightsCharts({ timeData, weatherData, severityData }) {
  return (
    <div className="grid gap-5 xl:grid-cols-3">
      <ChartCard
        title="Accidents by Time"
        subtitle="Night currently has the highest incident count in this sample"
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={timeData} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="label" stroke="#64748b" />
            <YAxis allowDecimals={false} stroke="#64748b" />
            <Tooltip />
            <Bar dataKey="count" fill="#2563eb" radius={[10, 10, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title="Weather Contribution"
        subtitle="Rain and fog combinations indicate elevated risk situations"
      >
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip />
            <Legend />
            <Pie
              data={weatherData}
              dataKey="count"
              nameKey="label"
              cx="50%"
              cy="50%"
              outerRadius={94}
              innerRadius={54}
              paddingAngle={4}
            >
              {weatherData.map((entry, index) => (
                <Cell key={entry.label} fill={palette[index % palette.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard
        title="Severity Distribution"
        subtitle="Model and preprocessing pipeline are aligned with 3-level target classes"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={severityData} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="label" stroke="#64748b" />
            <YAxis allowDecimals={false} stroke="#64748b" />
            <Tooltip />
            <Line
              type="monotone"
              dataKey="count"
              stroke="#0ea5e9"
              strokeWidth={3}
              dot={{ r: 5, fill: '#0ea5e9' }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}
