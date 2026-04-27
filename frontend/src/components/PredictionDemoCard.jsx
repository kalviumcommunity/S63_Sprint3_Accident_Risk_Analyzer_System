import { useMemo, useState } from 'react'
import { AlertTriangle, ArrowRight, BadgeInfo, BadgePercent } from 'lucide-react'

import { getPredictionOptions, predictAccidentSeverity } from '../services/predictionRules'

const initialState = {
  time: 'Night',
  weather: 'Rain',
  roadType: 'Highway',
}

export default function PredictionDemoCard() {
  const { timeOptions, weatherOptions, roadTypeOptions } = useMemo(
    () => getPredictionOptions(),
    [],
  )

  const [formState, setFormState] = useState(initialState)
  const [prediction, setPrediction] = useState(() =>
    predictAccidentSeverity(initialState),
  )

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormState((current) => ({
      ...current,
      [name]: value,
    }))
  }

  const handlePredict = (event) => {
    event.preventDefault()
    setPrediction(predictAccidentSeverity(formState))
  }

  return (
    <div className="grid gap-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:grid-cols-[0.95fr_1.05fr]">
      <form onSubmit={handlePredict} className="space-y-5">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-700">
            Live prediction demo
          </p>
          <h3 className="mt-2 text-2xl font-semibold text-slate-950">
            Pick conditions and generate a risk output.
          </h3>
          <p className="mt-3 text-sm leading-6 text-slate-600">
            This frontend demo mirrors the backend prediction flow with a local scoring rule so the
            interaction is visible even before the Streamlit layer is connected to a deployed API.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Time</span>
            <select
              name="time"
              value={formState.time}
              onChange={handleChange}
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-blue-500 focus:bg-white"
            >
              {timeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Weather</span>
            <select
              name="weather"
              value={formState.weather}
              onChange={handleChange}
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-blue-500 focus:bg-white"
            >
              {weatherOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="space-y-2 text-sm font-medium text-slate-700">
            <span>Road type</span>
            <select
              name="roadType"
              value={formState.roadType}
              onChange={handleChange}
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-blue-500 focus:bg-white"
            >
              {roadTypeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="rounded-2xl border border-blue-100 bg-blue-50 p-4 text-sm leading-7 text-blue-900">
          <div className="flex items-start gap-3">
            <BadgeInfo className="mt-0.5 h-5 w-5 flex-none text-blue-700" />
            <div>
              <p className="font-semibold">How the demo works</p>
              <p className="mt-1 text-blue-800/90">
                Higher time-of-day, weather, and road-risk scores increase the final severity. This
                keeps the UI simple while matching the categories used by the trained model.
              </p>
            </div>
          </div>
        </div>

        <button
          type="submit"
          className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-slate-800"
        >
          Predict severity
          <ArrowRight className="h-4 w-4" />
        </button>
      </form>

      <div className="rounded-3xl bg-slate-950 p-6 text-white shadow-xl shadow-slate-900/20">
        <div className="flex items-center gap-3 text-slate-100">
          <BadgePercent className="h-5 w-5 text-blue-300" />
          <h4 className="text-lg font-semibold">Prediction result</h4>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl bg-white/10 p-4">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-300">Selected time</p>
            <p className="mt-3 text-lg font-semibold">{formState.time}</p>
          </div>
          <div className="rounded-2xl bg-white/10 p-4">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-300">Selected weather</p>
            <p className="mt-3 text-lg font-semibold">{formState.weather}</p>
          </div>
          <div className="rounded-2xl bg-white/10 p-4">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-300">Selected road</p>
            <p className="mt-3 text-lg font-semibold">{formState.roadType}</p>
          </div>
        </div>

        <div className="mt-6 rounded-3xl border border-white/10 bg-white/5 p-6">
          <p className="text-sm text-slate-300">Computed risk score</p>
          <p className="mt-2 text-5xl font-semibold text-white">{prediction.score}</p>
          <div className="mt-5 flex flex-wrap gap-3">
            <span className="rounded-full bg-blue-500/20 px-4 py-2 text-sm font-semibold text-blue-100">
              {prediction.severity} severity
            </span>
            <span className="rounded-full bg-amber-500/20 px-4 py-2 text-sm font-semibold text-amber-100">
              {prediction.riskLevel}
            </span>
          </div>
        </div>

        <div className="mt-6 rounded-2xl bg-amber-500/10 p-4 text-sm leading-7 text-amber-100">
          <div className="flex items-start gap-3">
            <AlertTriangle className="mt-0.5 h-5 w-5 flex-none text-amber-300" />
            <p>{prediction.explanation}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
