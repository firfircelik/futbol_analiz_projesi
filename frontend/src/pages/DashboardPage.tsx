import { useAuthStore } from '../store/authStore'
import { TrendingUp, Users, Target, BarChart3 } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user)

  const stats = [
    { name: 'Reports This Month', value: user?.quotas.player_reports.used || 0, icon: BarChart3, change: '+12%' },
    { name: 'Team Fit Analyses', value: user?.quotas.team_fit.used || 0, icon: Target, change: '+8%' },
    { name: 'Players Tracked', value: '24', icon: Users, change: '+3' },
    { name: 'Success Rate', value: '87%', icon: TrendingUp, change: '+2%' },
  ]

  const recentPlayers = [
    { name: 'Mohamed Salah', team: 'Liverpool FC', opta_index: 85.2, status: 'EXCELLENT' },
    { name: 'Erling Haaland', team: 'Manchester City', opta_index: 88.3, status: 'EXCEPTIONAL' },
    { name: 'Kylian Mbappé', team: 'Real Madrid', opta_index: 86.7, status: 'EXCELLENT' },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-navy-900">Welcome back, {user?.email?.split('@')[0]}!</h1>
        <p className="text-gray-600 mt-2">Here's what's happening with your scouting</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.name}</p>
                <p className="text-3xl font-bold text-navy-900 mt-2">{stat.value}</p>
                <p className="text-sm text-green-600 mt-1">{stat.change} from last month</p>
              </div>
              <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <stat.icon className="h-6 w-6 text-primary-600" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid lg:grid-cols-3 gap-6 mb-8">
        <Link to="/dashboard/search" className="card hover:shadow-lg transition-shadow cursor-pointer group">
          <div className="flex items-center space-x-4">
            <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-colors">
              <Users className="h-6 w-6 text-primary-600 group-hover:text-white transition-colors" />
            </div>
            <div>
              <h3 className="font-semibold text-navy-900">Search Players</h3>
              <p className="text-sm text-gray-600">Find talent across 50+ leagues</p>
            </div>
          </div>
        </Link>

        <Link to="/dashboard/team-fit" className="card hover:shadow-lg transition-shadow cursor-pointer group">
          <div className="flex items-center space-x-4">
            <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-colors">
              <Target className="h-6 w-6 text-primary-600 group-hover:text-white transition-colors" />
            </div>
            <div>
              <h3 className="font-semibold text-navy-900">Team Fit Analysis</h3>
              <p className="text-sm text-gray-600">Find perfect matches for your squad</p>
            </div>
          </div>
        </Link>

        <a href="/api/docs" target="_blank" rel="noopener noreferrer" className="card hover:shadow-lg transition-shadow cursor-pointer group">
          <div className="flex items-center space-x-4">
            <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-600 transition-colors">
              <BarChart3 className="h-6 w-6 text-primary-600 group-hover:text-white transition-colors" />
            </div>
            <div>
              <h3 className="font-semibold text-navy-900">API Access</h3>
              <p className="text-sm text-gray-600">Integrate our data into your tools</p>
            </div>
          </div>
        </a>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-bold text-navy-900 mb-4">Recently Viewed Players</h2>
        <div className="space-y-4">
          {recentPlayers.map((player) => (
            <div key={player.name} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
              <div className="flex items-center space-x-4">
                <div className="h-12 w-12 bg-navy-900 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">{player.name.split(' ').map(n => n[0]).join('')}</span>
                </div>
                <div>
                  <p className="font-semibold text-navy-900">{player.name}</p>
                  <p className="text-sm text-gray-600">{player.team}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-primary-600">{player.opta_index}</p>
                <p className="text-sm text-gray-600">{player.status}</p>
              </div>
            </div>
          ))}
        </div>
        <Link to="/dashboard/search" className="mt-4 text-primary-600 font-medium hover:text-primary-700 inline-block">
          View all players →
        </Link>
      </div>
    </div>
  )
}
