import { useMemo, useState } from 'react';
import { ArrowRight, ShieldCheck, Shield, ShieldAlert } from 'lucide-react';
import { getPredictionOptions, predictAccidentSeverity } from '../services/predictionRules';

const initialState = { time: 'Night', weather: 'Rain', roadType: 'Highway' };

const severityTheme = {
  Low: {
    Icon: ShieldCheck,
    card: 'border-emerald-200 bg-emerald-50/60',
    text: 'text-emerald-600',
    badge: 'bg-emerald-100 text-emerald-700',
    score: 'text-emerald-600',
  },
  Medium: {
    Icon: Shield,
    card: 'border-amber-200 bg-amber-50/60',
    text: 'text-amber-600',
    badge: 'bg-amber-100 text-amber-700',
    score: 'text-amber-600',
  },
  High: {
    Icon: ShieldAlert,
    card: 'border-rose-200 bg-rose-50/60',
    text: 'text-rose-600',
    badge: 'bg-rose-100 text-rose-700',
    score: 'text-rose-600',
  },
};

function SelectField({ label, name, value, options, onChange }) {
  return (
    <label className="block space-y-2">
      <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
        {label}
      </span>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition-colors focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </label>
  );
}

export default function PredictionDemoCard() {
  const { timeOptions, weatherOptions, roadTypeOptions } = useMemo(
    () => getPredictionOptions(), [],
  );

  const [formState, setFormState] = useState(initialState);
  const [prediction, setPrediction] = useState(() => predictAccidentSeverity(initialState));

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormState((s) => ({ ...s, [name]: value }));
  };

  const handlePredict = (e) => {
    e.preventDefault();
    setPrediction(predictAccidentSeverity(formState));
  };

  const theme = severityTheme[prediction.severity] || severityTheme.Low;
  const SeverityIcon = theme.Icon;

  return (
    <div className="grid gap-8 lg:grid-cols-2">
      {/* ── Left: Form ───────────────────────────── */}
      <form
        onSubmit={handlePredict}
        className="space-y-6 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm"
      >
        <div>
          <h3 className="text-base font-semibold text-slate-800">
            Select Conditions
          </h3>
          <p className="mt-1 text-sm text-slate-400">
            Choose accident conditions to generate a severity prediction.
          </p>
        </div>

        <div className="grid gap-5 sm:grid-cols-3">
          <SelectField label="Time" name="time" value={formState.time} options={timeOptions} onChange={handleChange} />
          <SelectField label="Weather" name="weather" value={formState.weather} options={weatherOptions} onChange={handleChange} />
          <SelectField label="Road Type" name="roadType" value={formState.roadType} options={roadTypeOptions} onChange={handleChange} />
        </div>

        <button
          type="submit"
          className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-blue-500/30"
        >
          Predict Severity
          <ArrowRight size={15} />
        </button>
      </form>

      {/* ── Right: Result ────────────────────────── */}
      <div className={`flex flex-col justify-between rounded-2xl border p-7 shadow-sm transition-colors duration-500 ${theme.card}`}>
        <div>
          <div className="flex items-center gap-2.5">
            <SeverityIcon size={20} className={theme.text} />
            <h3 className="text-base font-semibold text-slate-800">Prediction Result</h3>
          </div>

          {/* Score */}
          <div className="mt-8">
            <p className="text-xs uppercase tracking-wider text-slate-400">Risk Score</p>
            <p className={`mt-1 text-5xl font-bold ${theme.score}`}>{prediction.score}</p>
          </div>

          {/* Badges */}
          <div className="mt-6 flex flex-wrap gap-2.5">
            <span className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold ${theme.badge}`}>
              {prediction.severity} Severity
            </span>
            <span className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold ${theme.badge}`}>
              {prediction.riskLevel}
            </span>
          </div>
        </div>

        {/* Conditions */}
        <div className="mt-8 grid grid-cols-3 gap-3">
          {[
            { label: 'Time', value: formState.time },
            { label: 'Weather', value: formState.weather },
            { label: 'Road', value: formState.roadType },
          ].map((item) => (
            <div key={item.label} className="rounded-xl bg-white/70 px-3.5 py-3 shadow-sm">
              <p className="text-[10px] uppercase tracking-wider text-slate-400">{item.label}</p>
              <p className="mt-1 text-sm font-medium text-slate-700">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Explanation */}
        <p className="mt-6 rounded-xl bg-white/60 px-4 py-3 text-xs leading-relaxed text-slate-500">
          {prediction.explanation}
        </p>
      </div>
    </div>
  );
}
