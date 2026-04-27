import { ArrowRight, CheckCircle2 } from 'lucide-react'

export default function HowItWorksFlow({ steps }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="grid gap-4 lg:grid-cols-5">
        {steps.map((step, index) => (
          <div key={step.title} className="relative rounded-2xl bg-slate-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-blue-700">
              Step {index + 1}
            </p>
            <h3 className="mt-2 text-base font-semibold text-slate-900">{step.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-600">{step.description}</p>

            <div className="mt-3 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Complete
            </div>

            {index < steps.length - 1 && (
              <ArrowRight className="absolute -right-3 top-1/2 hidden h-5 w-5 -translate-y-1/2 rounded-full border border-slate-200 bg-white p-1 text-slate-500 lg:block" />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
