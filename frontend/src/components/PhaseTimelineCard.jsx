export default function PhaseTimelineCard({ id, title, status, summary, highlights }) {
  return (
    <article className="group rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-700">
            Phase {id}
          </p>
          <h3 className="mt-2 text-xl font-semibold text-slate-900">{title}</h3>
        </div>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
          {status}
        </span>
      </div>

      <p className="mt-4 text-sm leading-6 text-slate-600">{summary}</p>

      <ul className="mt-5 space-y-2 text-sm text-slate-700">
        {highlights.map((highlight) => (
          <li key={highlight} className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-blue-600" />
            <span>{highlight}</span>
          </li>
        ))}
      </ul>
    </article>
  )
}
