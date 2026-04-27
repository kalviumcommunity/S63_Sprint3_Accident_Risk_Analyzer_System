import { lazy, Suspense } from 'react'

import { motion } from 'framer-motion'
import {
  ArrowRight,
  BarChart3,
  Database,
  Layers3,
  ShieldCheck,
  Sparkles,
  Workflow,
} from 'lucide-react'

import PhaseTimelineCard from './components/PhaseTimelineCard'
import PredictionDemoCard from './components/PredictionDemoCard'
import ProjectStatCard from './components/ProjectStatCard'
import TopSectionNav from './components/TopSectionNav'
import {
  flowSteps,
  insightsChartData,
  phaseCards,
  projectStats,
  quickRunSteps,
} from './data/projectSummary'

const InsightsCharts = lazy(() => import('./components/InsightsCharts'))
const HowItWorksFlow = lazy(() => import('./components/HowItWorksFlow'))

function SectionLoadingPlaceholder({ label }) {
  return (
    <div className="animate-pulse rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">{label}</p>
      <div className="mt-4 h-5 w-1/3 rounded bg-slate-200" />
      <div className="mt-6 grid gap-3">
        <div className="h-16 rounded-2xl bg-slate-100" />
        <div className="h-16 rounded-2xl bg-slate-100" />
        <div className="h-16 rounded-2xl bg-slate-100" />
      </div>
    </div>
  )
}

const heroHighlights = [
  'Data connection from MongoDB Atlas',
  'EDA visual summaries with saved plots',
  'Preprocessing and encoded model-ready data',
  'RandomForest model with reusable prediction pipeline',
  'Streamlit frontend for simple severity prediction',
]

function App() {
  return (
    <main className="min-h-screen text-slate-900">
      <TopSectionNav />

      <section id="hero" className="relative overflow-hidden border-b border-slate-200/70">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(37,99,235,0.18),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(14,165,233,0.12),transparent_22%)]" />
        <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-8 lg:px-8">
          <header className="flex flex-col gap-4 rounded-3xl border border-white/60 bg-white/70 px-5 py-4 shadow-sm backdrop-blur md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.4em] text-blue-700">
                Traffic Accident Analysis & Risk Prediction System
              </p>
              <h1 className="mt-2 text-2xl font-semibold tracking-tight text-slate-950 md:text-3xl">
                One dashboard to understand the full pipeline at a glance.
              </h1>
            </div>
            <div className="flex flex-wrap gap-2 text-sm font-medium text-slate-700">
              <span className="rounded-full bg-blue-50 px-3 py-1 text-blue-700">MongoDB</span>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-700">EDA</span>
              <span className="rounded-full bg-violet-50 px-3 py-1 text-violet-700">ML</span>
              <span className="rounded-full bg-amber-50 px-3 py-1 text-amber-700">Streamlit</span>
            </div>
          </header>

          <div className="grid flex-1 items-center gap-10 py-10 lg:grid-cols-[1.3fr_0.9fr] lg:py-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              <div className="space-y-5">
                <span className="inline-flex w-fit items-center gap-2 rounded-full border border-blue-200 bg-white/80 px-4 py-2 text-sm font-medium text-blue-800 shadow-sm">
                  <Sparkles className="h-4 w-4" />
                  Clean, guided, phase-by-phase project view
                </span>

                <div className="space-y-4">
                  <h2 className="max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 md:text-6xl">
                    See every completed phase, output, and next action in one place.
                  </h2>
                  <p className="max-w-2xl text-base leading-8 text-slate-600 md:text-lg">
                    This frontend organizes the entire accident-risk workflow so users can quickly
                    understand data input, analysis, model training, and final prediction behavior.
                  </p>
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {projectStats.map((stat) => (
                  <ProjectStatCard key={stat.label} {...stat} />
                ))}
              </div>

              <div className="flex flex-col gap-3 sm:flex-row">
                <a
                  href="#pipeline"
                  className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-950/20 transition hover:-translate-y-0.5 hover:bg-slate-800"
                >
                  Explore the pipeline
                  <ArrowRight className="h-4 w-4" />
                </a>
                <a
                  href="#insights"
                  className="inline-flex items-center justify-center gap-2 rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-800 transition hover:-translate-y-0.5 hover:border-slate-400 hover:bg-slate-50"
                >
                  View interactive charts
                </a>
              </div>

              <div className="grid gap-4 rounded-3xl border border-slate-200 bg-white/80 p-6 shadow-sm backdrop-blur md:grid-cols-2">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">
                    What this dashboard shows
                  </p>
                  <ul className="mt-4 space-y-3 text-sm leading-7 text-slate-600">
                    {heroHighlights.map((item) => (
                      <li key={item} className="flex items-start gap-3">
                        <ShieldCheck className="mt-1 h-4 w-4 flex-none text-emerald-600" />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-2xl bg-slate-950 p-5 text-white">
                  <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-300">
                    Current sample prediction
                  </p>
                  <div className="mt-4 space-y-3 text-sm text-slate-200">
                    <p>
                      <span className="text-slate-400">Time:</span> Night
                    </p>
                    <p>
                      <span className="text-slate-400">Weather:</span> Rain
                    </p>
                    <p>
                      <span className="text-slate-400">Road Type:</span> Highway
                    </p>
                  </div>
                  <div className="mt-5 rounded-2xl bg-white/10 p-4">
                    <p className="text-sm text-slate-300">Predicted severity</p>
                    <p className="text-2xl font-semibold text-white">High</p>
                    <p className="text-sm text-slate-300">Risk level: High Risk</p>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.aside
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="grid gap-4"
            >
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-200/60">
                <div className="flex items-center gap-3 text-slate-950">
                  <Database className="h-5 w-5 text-blue-700" />
                  <h3 className="text-lg font-semibold">Project flow</h3>
                </div>
                <div className="mt-5 space-y-4">
                  {quickRunSteps.map((step, index) => (
                    <div key={step} className="flex gap-4 rounded-2xl bg-slate-50 p-4">
                      <div className="flex h-8 w-8 flex-none items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
                        {index + 1}
                      </div>
                      <p className="text-sm leading-6 text-slate-700">{step}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-3xl border border-blue-100 bg-gradient-to-br from-blue-600 to-slate-900 p-6 text-white shadow-xl shadow-blue-900/20">
                <div className="flex items-center gap-3">
                  <Workflow className="h-5 w-5 text-blue-100" />
                  <h3 className="text-lg font-semibold">Why this dashboard helps</h3>
                </div>
                <p className="mt-4 text-sm leading-7 text-blue-50/90">
                  The project was built in separate phases, so the frontend should communicate the sequence,
                  outputs, and final prediction behavior without forcing the user to jump through files.
                </p>
                <div className="mt-5 grid gap-3 text-sm text-blue-50">
                  <div className="rounded-2xl bg-white/10 p-4">Simple explanation of each phase</div>
                  <div className="rounded-2xl bg-white/10 p-4">Quick access to results and metrics</div>
                  <div className="rounded-2xl bg-white/10 p-4">Prediction-ready interaction section</div>
                </div>
              </div>
            </motion.aside>
          </div>
        </div>
      </section>

      <section id="pipeline" className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="mb-8 flex items-end justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-blue-700">
              Phase overview
            </p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
              The full project flow, clearly shown.
            </h2>
          </div>
          <div className="hidden items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 shadow-sm md:flex">
            <Layers3 className="h-4 w-4 text-blue-700" />
            Built step-by-step, then surfaced together
          </div>
        </div>

        <div className="grid gap-5 lg:grid-cols-2 xl:grid-cols-3">
          {phaseCards.map((phase) => (
            <PhaseTimelineCard key={phase.id} {...phase} />
          ))}
        </div>
      </section>

      <section id="insights" className="border-t border-slate-200 bg-white/70">
        <div className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
          <div className="mb-8">
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-blue-700">
              Insight charts
            </p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
              Visual summaries from your current dataset.
            </h2>
            <p className="mt-3 max-w-3xl text-base leading-8 text-slate-600">
              These charts mirror the project EDA outputs and make the trend findings visible directly
              inside the frontend dashboard.
            </p>
          </div>

          <Suspense fallback={<SectionLoadingPlaceholder label="Loading charts" />}>
            <InsightsCharts
              timeData={insightsChartData.timeData}
              weatherData={insightsChartData.weatherData}
              severityData={insightsChartData.severityData}
            />
          </Suspense>
        </div>
      </section>

      <section id="prediction" className="border-t border-slate-200 bg-white/70">
        <div className="mx-auto grid max-w-7xl gap-8 px-6 py-16 lg:grid-cols-[0.9fr_1.1fr] lg:px-8">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-blue-700">
              Prediction snapshot
            </p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
              Try conditions and see immediate risk output.
            </h2>
            <p className="mt-4 max-w-xl text-base leading-8 text-slate-600">
              Choose time, weather, and road type to generate severity and risk-level output in real-time.
              This section is intentionally simple for demo and explanation clarity.
            </p>
          </div>

          <PredictionDemoCard />
        </div>
      </section>

      <section id="how-it-works" className="border-t border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
          <div className="mb-8">
            <p className="text-sm font-semibold uppercase tracking-[0.35em] text-blue-700">
              How it works
            </p>
            <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">
              End-to-end flow from raw data to user prediction.
            </h2>
          </div>

          <Suspense fallback={<SectionLoadingPlaceholder label="Loading flow" />}>
            <HowItWorksFlow steps={flowSteps} />
          </Suspense>
        </div>
      </section>

      <footer className="border-t border-slate-200 bg-slate-950 text-slate-300">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-8 text-sm md:flex-row md:items-center md:justify-between lg:px-8">
          <p>Traffic Accident Analysis & Risk Prediction System</p>
          <p className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4" />
            Frontend Part 3: charts, guided navigation, and flow visualization
          </p>
        </div>
      </footer>
    </main>
  )
}

export default App
