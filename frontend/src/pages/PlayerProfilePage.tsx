import { useParams } from 'react-router-dom'
import { TrendingUp, DollarSign, Award, BarChart3, Target } from 'lucide-react'

export default function PlayerProfilePage() {
  const { playerId } = useParams()

  // Mock data
  const player = {
    name: 'Erling Haaland',
    team: 'Manchester City',
    position: 'FWD',
    age: 23,
    nationality: 'Norway',
    opta_index: 88.3,
    rating: 'EXCEPTIONAL',
    market_value: 180,
    stats: {
      goals: 36,
      assists: 12,
      minutes: 3240,
      shots_on_target: 98,
      pass_accuracy: 78.2,
    },
    advanced: {
      xg: 32.4,
      xa: 9.2,
      progressive_passes: 156,
    },
  }

  return (
    <div>
      {/* Header */}
      <div className="card mb-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-6">
            <div className="h-24 w-24 bg-navy-900 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-3xl">
                {player.name.split(' ').map(n => n[0]).join('')}
              </span>
            </div>
            <div>
              <h1 className="text-3xl font-bold text-navy-900">{player.name}</h1>
              <div className="flex items-center space-x-4 mt-2 text-gray-600">
                <span className="font-medium">{player.team}</span>
                <span>•</span>
                <span>{player.position}</span>
                <span>•</span>
                <span>{player.age} years</span>
                <span>•</span>
                <span>{player.nationality}</span>
              </div>
            </div>
          </div>

          <div className="text-right">
            <div className="text-4xl font-bold text-primary-600">{player.opta_index}</div>
            <div className="text-sm text-gray-600 mt-1">{player.rating}</div>
          </div>
        </div>
      </div>

      {/* Key Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {[
          { label: 'Goals', value: player.stats.goals, icon: Award },
          { label: 'Assists', value: player.stats.assists, icon: Target },
          { label: 'Minutes', value: player.stats.minutes, icon: BarChart3 },
          { label: 'Market Value', value: `€${player.market_value}M`, icon: DollarSign },
          { label: 'Pass Accuracy', value: `${player.stats.pass_accuracy}%`, icon: TrendingUp },
        ].map((stat) => (
          <div key={stat.label} className="card text-center">
            <stat.icon className="h-6 w-6 text-primary-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-navy-900">{stat.value}</div>
            <div className="text-sm text-gray-600 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Advanced Metrics */}
      <div className="card mb-6">
        <h2 className="text-xl font-bold text-navy-900 mb-4">Advanced Metrics</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <div className="text-sm text-gray-600 mb-1">Expected Goals (xG)</div>
            <div className="text-3xl font-bold text-primary-600">{player.advanced.xg}</div>
            <div className="text-sm text-green-600 mt-1">+{(player.stats.goals - player.advanced.xg).toFixed(1)} vs expected</div>
          </div>
          <div>
            <div className="text-sm text-gray-600 mb-1">Expected Assists (xA)</div>
            <div className="text-3xl font-bold text-primary-600">{player.advanced.xa}</div>
            <div className="text-sm text-green-600 mt-1">+{(player.stats.assists - player.advanced.xa).toFixed(1)} vs expected</div>
          </div>
          <div>
            <div className="text-sm text-gray-600 mb-1">Progressive Passes</div>
            <div className="text-3xl font-bold text-primary-600">{player.advanced.progressive_passes}</div>
            <div className="text-sm text-gray-600 mt-1">Per 90 minutes</div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex space-x-4">
        <button className="btn-primary flex items-center">
          <Target className="h-5 w-5 mr-2" />
          Analyze Team Fit
        </button>
        <button className="btn-secondary">Download Full Report (PDF)</button>
      </div>
    </div>
  )
}
