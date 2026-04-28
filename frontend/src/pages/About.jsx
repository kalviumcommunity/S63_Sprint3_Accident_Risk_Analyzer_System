const techStack = [
  { label: 'Python', icon: '🐍' },
  { label: 'MongoDB', icon: '🍃' },
  { label: 'scikit-learn', icon: '🤖' },
  { label: 'React', icon: '⚛️' },
  { label: 'Tailwind CSS', icon: '🎨' },
  { label: 'Pandas', icon: '🐼' },
  { label: 'Recharts', icon: '📈' },
  { label: 'Vite', icon: '⚡' },
];

const pipeline = [
  { step: '01', title: 'Data Collection', desc: 'Fetch accident records from MongoDB Atlas into a structured DataFrame.' },
  { step: '02', title: 'Exploratory Analysis', desc: 'Visualize weather, time, road type, and severity trends with EDA charts.' },
  { step: '03', title: 'Preprocessing', desc: 'Handle missing values, encode categories, and generate model-ready features.' },
  { step: '04', title: 'Model Training', desc: 'Train a RandomForest classifier and evaluate predictive performance.' },
  { step: '05', title: 'Web Application', desc: 'Interactive prediction and insights dashboard for end users.' },
];

export default function About() {
  return (
    <div className="min-h-screen px-8 py-16 lg:px-12">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="mb-14 animate-fade-in-up">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-blue-600">
            ℹ️ Overview
          </p>
          <h1 className="mt-3 text-3xl font-bold text-slate-900 md:text-4xl">
            About This Project
          </h1>
        </div>

        <div className="space-y-14">
          {/* Problem Statement */}
          <section className="animate-fade-in-up">
            <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-slate-800">
              <span className="text-xl">⚠️</span> Problem Statement
            </h2>
            <p className="text-sm leading-7 text-slate-500">
              Road accidents are a leading cause of injuries and fatalities worldwide.
              Understanding the conditions that contribute to accident severity—such as
              time of day, weather, and road type—can help authorities take preventive
              measures and allocate resources more effectively.
            </p>
          </section>

          {/* Objective */}
          <section className="animate-fade-in-up-delay">
            <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-slate-800">
              <span className="text-xl">🎯</span> Objective
            </h2>
            <p className="text-sm leading-7 text-slate-500">
              Build an end-to-end data science and machine learning application that
              analyzes traffic accident data, identifies patterns through exploratory
              analysis, and predicts accident severity using a trained classification
              model—all accessible through a modern, interactive web interface.
            </p>
          </section>

          {/* Tech Stack */}
          <section className="animate-fade-in-up-delay-2">
            <h2 className="mb-6 flex items-center gap-2 text-lg font-semibold text-slate-800">
              <span className="text-xl">🛠️</span> Tech Stack
            </h2>
            <div className="flex flex-wrap gap-3">
              {techStack.map((tech) => (
                <span
                  key={tech.label}
                  className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-600 shadow-sm transition-colors hover:border-blue-300 hover:text-blue-600"
                >
                  <span>{tech.icon}</span>
                  {tech.label}
                </span>
              ))}
            </div>
          </section>

          {/* Pipeline */}
          <section className="animate-fade-in-up-delay-2">
            <h2 className="mb-6 flex items-center gap-2 text-lg font-semibold text-slate-800">
              <span className="text-xl">🔄</span> Project Pipeline
            </h2>
            <div className="space-y-4">
              {pipeline.map((item, idx) => (
                <div
                  key={item.step}
                  className="group flex items-start gap-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-colors hover:border-blue-200 hover:shadow-md"
                >
                  <span className="flex h-10 w-10 flex-none items-center justify-center rounded-xl bg-blue-50 text-xs font-bold text-blue-600">
                    {item.step}
                  </span>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-800">{item.title}</h3>
                    <p className="mt-1 text-sm leading-relaxed text-slate-500">{item.desc}</p>
                  </div>
                  {idx < pipeline.length - 1 && (
                    <span className="ml-auto hidden self-center text-slate-300 lg:block">→</span>
                  )}
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
