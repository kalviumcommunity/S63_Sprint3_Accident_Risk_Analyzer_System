import PredictionDemoCard from '../components/PredictionDemoCard';

export default function Predict() {
  return (
    <div className="min-h-screen px-8 py-16 lg:px-12">
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <div className="mb-12 animate-fade-in-up">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-blue-600">
            ⚡ Risk Assessment
          </p>
          <h1 className="mt-3 text-3xl font-bold text-slate-900 md:text-4xl">
            Predict Accident Severity
          </h1>
          <p className="mt-3 max-w-lg text-sm leading-relaxed text-slate-500">
            Select the time of day, weather condition, and road type to generate
            an accident severity prediction.
          </p>
        </div>

        {/* Prediction card */}
        <div className="animate-fade-in-up-delay">
          <PredictionDemoCard />
        </div>
      </div>
    </div>
  );
}
