/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        slate: '#334155',
        mist: '#e2e8f0',
        accent: '#2563eb',
        accentSoft: '#dbeafe',
      },
    },
  },
  plugins: [],
}

