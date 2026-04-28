import {
  Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart,
  Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';

const palette = ['#2563eb', '#0891b2', '#7c3aed', '#f59e0b'];

const tooltipStyle = {
  backgroundColor: '#ffffff',
  border: '1px solid #e2e8f0',
  borderRadius: '10px',
  fontSize: '12px',
  color: '#334155',
  boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
};

function ChartCard({ title, insight, children }) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
      <div className="mt-4 h-64">{children}</div>
      <p className="mt-4 text-xs leading-relaxed text-slate-400">
        💡 {insight}
      </p>
    </article>
  );
}

export default function InsightsCharts({ timeData, weatherData, severityData }) {
  return (
    <div className="grid gap-6 xl:grid-cols-3">
      {/* Bar chart — Accidents by Time */}
      <ChartCard
        title="📊 Accidents by Time of Day"
        insight="Night has the highest incident count, indicating elevated risk during low-visibility hours."
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={timeData} margin={{ top: 8, right: 8, left: -12, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="label" stroke="#cbd5e1" tick={{ fill: '#64748b', fontSize: 11 }} />
            <YAxis allowDecimals={false} stroke="#cbd5e1" tick={{ fill: '#64748b', fontSize: 11 }} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(0,0,0,0.03)' }} />
            <Bar dataKey="count" radius={[8, 8, 0, 0]}>
              {timeData.map((_, i) => (
                <Cell key={i} fill={palette[i % palette.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Pie chart — Weather Contribution */}
      <ChartCard
        title="🌦️ Weather Contribution"
        insight="Rain and fog combinations contribute to over 60% of incidents, suggesting weather is a key factor."
      >
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip contentStyle={tooltipStyle} />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: '11px', color: '#64748b' }}
            />
            <Pie
              data={weatherData}
              dataKey="count"
              nameKey="label"
              cx="50%"
              cy="45%"
              outerRadius={80}
              innerRadius={48}
              paddingAngle={4}
              strokeWidth={0}
            >
              {weatherData.map((entry, i) => (
                <Cell key={entry.label} fill={palette[i % palette.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Line chart — Severity Distribution */}
      <ChartCard
        title="📈 Severity Distribution"
        insight="Low and High severity classes dominate, with Medium being the least common in this dataset."
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={severityData} margin={{ top: 8, right: 8, left: -12, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="label" stroke="#cbd5e1" tick={{ fill: '#64748b', fontSize: 11 }} />
            <YAxis allowDecimals={false} stroke="#cbd5e1" tick={{ fill: '#64748b', fontSize: 11 }} />
            <Tooltip contentStyle={tooltipStyle} />
            <Line
              type="monotone"
              dataKey="count"
              stroke="#2563eb"
              strokeWidth={2.5}
              dot={{ r: 5, fill: '#2563eb', strokeWidth: 0 }}
              activeDot={{ r: 7, fill: '#2563eb' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  );
}
