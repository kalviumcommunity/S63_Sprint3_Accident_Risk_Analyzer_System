const navItems = [
  { id: 'hero', label: 'Overview' },
  { id: 'pipeline', label: 'Pipeline' },
  { id: 'insights', label: 'Insights' },
  { id: 'prediction', label: 'Prediction' },
  { id: 'how-it-works', label: 'How It Works' },
]

export default function TopSectionNav() {
  return (
    <nav className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/80 backdrop-blur-lg">
      <div className="mx-auto flex max-w-7xl items-center gap-2 overflow-x-auto px-4 py-3 lg:px-8">
        {navItems.map((item) => (
          <a
            key={item.id}
            href={`#${item.id}`}
            className="whitespace-nowrap rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600 transition hover:border-blue-300 hover:text-blue-700"
          >
            {item.label}
          </a>
        ))}
      </div>
    </nav>
  )
}
