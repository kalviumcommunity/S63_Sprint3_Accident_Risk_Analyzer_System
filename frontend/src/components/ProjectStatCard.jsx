export default function ProjectStatCard({ label, value, note }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white/85 p-5 shadow-sm backdrop-blur">
      <p className="text-sm font-medium uppercase tracking-[0.24em] text-slate-500">
        {label}
      </p>
      <div className="mt-3 text-3xl font-semibold text-slate-900">{value}</div>
      <p className="mt-2 text-sm leading-6 text-slate-600">{note}</p>
    </div>
  )
}
