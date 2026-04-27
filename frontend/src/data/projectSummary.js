export const projectStats = [
  {
    label: 'MongoDB records',
    value: '8',
    note: 'Traffic accident sample loaded successfully',
  },
  {
    label: 'EDA visuals',
    value: '7',
    note: 'Count, trend, scatter, and box plots generated',
  },
  {
    label: 'Processed features',
    value: '10',
    note: 'Encoded feature columns ready for ML',
  },
  {
    label: 'Model accuracy',
    value: '50%',
    note: 'RandomForest baseline on small dataset',
  },
]

export const phaseCards = [
  {
    id: '01',
    title: 'Data Connection',
    status: 'Complete',
    summary: 'MongoDB Atlas connection, record fetch, and DataFrame extraction.',
    highlights: ['traffic_db.accidents', '8 records fetched', '_id removed'],
  },
  {
    id: '02',
    title: 'Exploratory Analysis',
    status: 'Complete',
    summary: 'Count, trend, scatter, and box plots with short insights.',
    highlights: ['Weather, time, road type', 'Severity distribution', 'Trend checks'],
  },
  {
    id: '03',
    title: 'Preprocessing',
    status: 'Complete',
    summary: 'Missing values handled, categories encoded, ML-ready data saved.',
    highlights: ['Mode imputation', 'get_dummies encoding', 'Clean + encoded CSV'],
  },
  {
    id: '04',
    title: 'Machine Learning',
    status: 'Complete',
    summary: 'RandomForest trained, evaluated, and saved as a reusable artifact.',
    highlights: ['Train/test split', 'Accuracy 0.50', 'Joblib model file'],
  },
  {
    id: '05',
    title: 'Insights & Conclusion',
    status: 'Complete',
    summary: 'Key patterns, assumptions, limitations, and final conclusions documented.',
    highlights: ['Night risk signal', 'Small-sample limits', 'Project summary'],
  },
  {
    id: '06',
    title: 'Web Application',
    status: 'Complete',
    summary: 'Streamlit prediction UI with severity and risk-level output.',
    highlights: ['Dropdown inputs', 'Live inference', 'High / Medium / Low risk'],
  },
]

export const quickRunSteps = [
  '1. Phase 1 connects to MongoDB and fetches data',
  '2. Phase 2 creates visual insights and saves plots',
  '3. Phase 3 prepares the encoded dataset',
  '4. Phase 4 trains the model and saves the artifact',
  '5. Phase 6 lets the user predict severity from the UI',
]

export const insightsChartData = {
  timeData: [
    { label: 'Morning', count: 2 },
    { label: 'Afternoon', count: 1 },
    { label: 'Evening', count: 2 },
    { label: 'Night', count: 3 },
  ],
  weatherData: [
    { label: 'Clear', count: 3 },
    { label: 'Rain', count: 3 },
    { label: 'Fog', count: 2 },
  ],
  severityData: [
    { label: 'Low', count: 3 },
    { label: 'Medium', count: 2 },
    { label: 'High', count: 3 },
  ],
}

export const flowSteps = [
  {
    title: 'Collect Data',
    description: 'Fetch accident records from MongoDB Atlas into a structured DataFrame.',
  },
  {
    title: 'Explore Patterns',
    description: 'Visualize weather, time, road type, and severity trends with EDA charts.',
  },
  {
    title: 'Preprocess Data',
    description: 'Handle missing values, encode categories, and generate model-ready features.',
  },
  {
    title: 'Train Model',
    description: 'Fit a RandomForest classifier and evaluate its predictive performance.',
  },
  {
    title: 'Predict Risk',
    description: 'Use the frontend form to generate severity and risk-level outcomes.',
  },
]
