import { NavLink } from 'react-router-dom';
import { Home, Activity, BarChart2, Info } from 'lucide-react';

const navItems = [
  { name: 'Home', path: '/', icon: Home },
  { name: 'Predict', path: '/predict', icon: Activity },
  { name: 'Insights', path: '/insights', icon: BarChart2 },
  { name: 'About', path: '/about', icon: Info },
];

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-[220px] flex-col border-r border-slate-200 bg-white px-5 py-8">
      {/* Brand */}
      <div className="mb-12 px-2">
        <span className="text-2xl leading-none">🚦</span>
        <h1 className="mt-2 text-[15px] font-bold leading-tight text-slate-900">
          Accident Risk
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
            Analyzer
          </span>
        </h1>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">
        {navItems.map(({ name, path, icon: Icon }) => (
          <NavLink
            key={name}
            to={path}
            end={path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-4 py-2.5 text-[13px] font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
              }`
            }
          >
            <Icon size={17} strokeWidth={1.8} />
            {name}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="mt-auto px-2 text-[11px] text-slate-400">
        Sprint 3 · v1.0
      </div>
    </aside>
  );
}
