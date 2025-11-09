import { useState } from 'react'
import { Target, TrendingUp, AlertCircle, CheckCircle, Clock } from 'lucide-react'

export default function TeamFitPage() {
  const [selectedPlayer, setSelectedPlayer] = useState('')
  const [teamStyle, setTeamStyle] = useState('high_press')
  const [showResults, setShowResults] = useState(false)

  const handleAnalyze = () => {
    setShowResults(true)
  }

  const fitResult = {
    overall_score: 87.5,
    rating: 'EXCELLENT_FIT',
    recommendation: 'STRONG BUY',
    breakdown: {
      statistical_fit: 90,
      tactical_fit: 88,
      personality_fit: 85,
      chemistry_fit: 87,
      cultural_fit: 92,
      budget_fit: 75,
      age_fit: 95,
    },
    strengths: [
      'Plays in priority position (ST)',
      'High performance level (Opta: 88.3)',
      'Perfect age bracket (23 years)',
      'Excellent cultural fit',
      'Strong work rate for high-press system',
    ],
    concerns: [
      'Market value slightly above budget (€180M)',
      'Limited Premier League experience',
    ],
    adaptation_timeline: 'IMMEDIATE (0-1 months)',
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-navy-900 flex items-center">
          <Target className="h-8 w-8 mr-3 text-primary-600" />
          Team Fit Analysis
        </h1>
        <p className="text-gray-600 mt-2">
          Find players that perfectly match your team's tactics, culture, and budget
        </p>
      </div>

      {/* Analysis Form */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h2 className="text-xl font-bold text-navy-900 mb-4">Player Selection</h2>

          <div className="space-y-4">
            <div>
              <label className="label">Select Player</label>
              <select
                className="input"
                value={selectedPlayer}
                onChange={(e) => setSelectedPlayer(e.target.value)}
              >
                <option value="">Choose a player...</option>
                <option value="haaland">Erling Haaland - Manchester City</option>
                <option value="mbappe">Kylian Mbappé - Real Madrid</option>
                <option value="salah">Mohamed Salah - Liverpool FC</option>
              </select>
            </div>

            <div>
              <label className="label">Player Position</label>
              <input type="text" className="input" placeholder="e.g., ST, CAM, LW" />
            </div>

            <div>
              <label className="label">Current Market Value (€M)</label>
              <input type="number" className="input" placeholder="e.g., 180" />
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-navy-900 mb-4">Your Team Profile</h2>

          <div className="space-y-4">
            <div>
              <label className="label">Team Name</label>
              <input type="text" className="input" placeholder="e.g., Manchester United" />
            </div>

            <div>
              <label className="label">Playing Style</label>
              <select
                className="input"
                value={teamStyle}
                onChange={(e) => setTeamStyle(e.target.value)}
              >
                <option value="high_press">High Press</option>
                <option value="possession">Possession Based</option>
                <option value="counter_attack">Counter Attack</option>
                <option value="defensive">Defensive</option>
                <option value="wing_play">Wing Play</option>
              </select>
            </div>

            <div>
              <label className="label">Formation</label>
              <select className="input">
                <option>4-3-3</option>
                <option>4-2-3-1</option>
                <option>3-5-2</option>
                <option>4-4-2</option>
              </select>
            </div>

            <div>
              <label className="label">Transfer Budget (€M)</label>
              <input type="number" className="input" placeholder="e.g., 150" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center mb-8">
        <button
          onClick={handleAnalyze}
          className="btn-primary px-8 py-3 text-lg flex items-center"
        >
          <Target className="h-5 w-5 mr-2" />
          Analyze Team Fit
        </button>
      </div>

      {/* Results */}
      {showResults && (
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="card bg-gradient-to-br from-primary-50 to-white border-2 border-primary-200">
            <div className="text-center">
              <div className="inline-flex items-center justify-center h-24 w-24 bg-primary-100 rounded-full mb-4">
                <span className="text-4xl font-bold text-primary-700">{fitResult.overall_score}</span>
              </div>
              <h2 className="text-2xl font-bold text-navy-900 mb-2">
                {fitResult.rating.replace('_', ' ')}
              </h2>
              <p className="text-lg text-gray-700 mb-4">{fitResult.recommendation}</p>
              <div className="flex items-center justify-center space-x-6 text-sm">
                <div className="flex items-center text-green-600">
                  <Clock className="h-4 w-4 mr-1" />
                  {fitResult.adaptation_timeline}
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Breakdown */}
          <div className="card">
            <h3 className="text-xl font-bold text-navy-900 mb-6">Fit Breakdown</h3>
            <div className="space-y-4">
              {Object.entries(fitResult.breakdown).map(([key, value]) => (
                <div key={key}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700 capitalize">
                      {key.replace('_', ' ')}
                    </span>
                    <span className="text-sm font-bold text-navy-900">{value}/100</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full ${
                        value >= 80
                          ? 'bg-green-500'
                          : value >= 60
                          ? 'bg-primary-500'
                          : 'bg-yellow-500'
                      }`}
                      style={{ width: `${value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Strengths & Concerns */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-bold text-navy-900 mb-4 flex items-center">
                <CheckCircle className="h-5 w-5 mr-2 text-green-600" />
                Key Strengths
              </h3>
              <ul className="space-y-3">
                {fitResult.strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start">
                    <TrendingUp className="h-5 w-5 text-green-600 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card">
              <h3 className="text-lg font-bold text-navy-900 mb-4 flex items-center">
                <AlertCircle className="h-5 w-5 mr-2 text-yellow-600" />
                Potential Concerns
              </h3>
              <ul className="space-y-3">
                {fitResult.concerns.map((concern, idx) => (
                  <li key={idx} className="flex items-start">
                    <AlertCircle className="h-5 w-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{concern}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center space-x-4">
            <button className="btn-primary">
              Generate Full Report (PDF)
            </button>
            <button className="btn-secondary">
              Compare with Other Players
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
