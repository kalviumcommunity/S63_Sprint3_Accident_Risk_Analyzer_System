const timeOptions = ['Morning', 'Afternoon', 'Evening', 'Night']
const weatherOptions = ['Clear', 'Rain', 'Fog']
const roadTypeOptions = ['Highway', 'City', 'Rural']

const severityByScore = [
  { min: 0, severity: 'Low', riskLevel: 'Low Risk' },
  { min: 3, severity: 'Medium', riskLevel: 'Moderate Risk' },
  { min: 6, severity: 'High', riskLevel: 'High Risk' },
]

const timeScoreMap = {
  Morning: 0,
  Afternoon: 1,
  Evening: 2,
  Night: 3,
}

const weatherScoreMap = {
  Clear: 0,
  Fog: 1,
  Rain: 2,
}

const roadTypeScoreMap = {
  Highway: 2,
  City: 1,
  Rural: 1,
}

function getSeverityFromScore(score) {
  return severityByScore
    .slice()
    .reverse()
    .find((entry) => score >= entry.min) ?? severityByScore[0]
}

export function getPredictionOptions() {
  return {
    timeOptions,
    weatherOptions,
    roadTypeOptions,
  }
}

export function predictAccidentSeverity({ time, weather, roadType }) {
  const score =
    (timeScoreMap[time] ?? 0) +
    (weatherScoreMap[weather] ?? 0) +
    (roadTypeScoreMap[roadType] ?? 0)

  const severityMatch = getSeverityFromScore(score)

  const reasonParts = [
    `Time: ${time} adds ${timeScoreMap[time] ?? 0} points`,
    `Weather: ${weather} adds ${weatherScoreMap[weather] ?? 0} points`,
    `Road type: ${roadType} adds ${roadTypeScoreMap[roadType] ?? 0} points`,
  ]

  return {
    score,
    severity: severityMatch.severity,
    riskLevel: severityMatch.riskLevel,
    explanation: reasonParts.join(' | '),
  }
}
