import { useNavigate } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-8">
      {/* Ambient glow orbs */}
      <div className="pointer-events-none absolute -top-40 right-1/4 h-[520px] w-[520px] rounded-full bg-blue-400/[0.08] blur-[120px] animate-glow-pulse" />
      <div className="pointer-events-none absolute -bottom-32 left-1/3 h-[400px] w-[400px] rounded-full bg-cyan-400/[0.06] blur-[100px] animate-glow-pulse" style={{ animationDelay: '2s' }} />

      {/* Hero content */}
      <div className="relative z-10 max-w-xl text-center">
        <div className="animate-fade-in-up text-6xl animate-float">🚦</div>

        <h1 className="animate-fade-in-up-delay mt-8 text-5xl font-extrabold leading-[1.1] tracking-tight text-slate-900 md:text-6xl">
          Accident Risk
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
            Analyzer
          </span>
        </h1>

        <p className="animate-fade-in-up-delay-2 mx-auto mt-6 max-w-md text-base leading-relaxed text-slate-500">
          Predict accident severity using machine learning. Analyze traffic
          patterns and make data-driven safety decisions.
        </p>

        <button
          onClick={() => navigate('/predict')}
          className="animate-fade-in-up-delay-2 mt-10 inline-flex items-center gap-2.5 rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-blue-500/30"
        >
          Start Prediction
          <ArrowRight size={17} />
        </button>
      </div>
    </div>
  );
}
