import { useState } from 'react'
import { Search, Filter, TrendingUp, DollarSign } from 'lucide-react'
import { Link } from 'react-router-dom'

const MOCK_PLAYERS = [
  { id: '1', name: 'Lionel Messi', team: 'Inter Miami', position: 'FWD', age: 36, opta_index: 82.5, market_value: 25, nationality: 'Argentina' },
  { id: '2', name: 'Erling Haaland', team: 'Manchester City', position: 'FWD', age: 23, opta_index: 88.3, market_value: 180, nationality: 'Norway' },
  { id: '3', name: 'Kylian Mbappé', team: 'Real Madrid', position: 'FWD', age: 25, opta_index: 86.7, market_value: 180, nationality: 'France' },
  { id: '4', name: 'Mohamed Salah', team: 'Liverpool FC', position: 'RW', age: 31, opta_index: 85.2, market_value: 65, nationality: 'Egypt' },
  { id: '5', name: 'Kevin De Bruyne', team: 'Manchester City', position: 'MID', age: 32, opta_index: 84.9, market_value: 80, nationality: 'Belgium' },
  { id: '6', name: 'Vinicius Junior', team: 'Real Madrid', position: 'LW', age: 23, opta_index: 83.4, market_value: 150, nationality: 'Brazil' },
]

export default function PlayerSearchPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedLeague, setSelectedLeague] = useState('all')
  const [selectedPosition, setSelectedPosition] = useState('all')
  const [players] = useState(MOCK_PLAYERS)

  const filteredPlayers = players.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         player.team.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesPosition = selectedPosition === 'all' || player.position === selectedPosition
    return matchesSearch && matchesPosition
  })

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-navy-900">Search Players</h1>
        <p className="text-gray-600 mt-2">Find talent across 50+ leagues worldwide</p>
      </div>

      {/* Search & Filters */}
      <div className="card mb-6">
        <div className="grid md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by player name or team..."
                className="input pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          <select
            className="input"
            value={selectedPosition}
            onChange={(e) => setSelectedPosition(e.target.value)}
          >
            <option value="all">All Positions</option>
            <option value="GK">Goalkeeper</option>
            <option value="DEF">Defender</option>
            <option value="MID">Midfielder</option>
            <option value="FWD">Forward</option>
            <option value="LW">Left Wing</option>
            <option value="RW">Right Wing</option>
          </select>
        </div>

        <div className="flex items-center space-x-4 mt-4">
          <select className="input w-auto">
            <option value="all">All Leagues</option>
            <option value="epl">Premier League</option>
            <option value="laliga">La Liga</option>
            <option value="bundesliga">Bundesliga</option>
            <option value="seriea">Serie A</option>
            <option value="ligue1">Ligue 1</option>
          </select>

          <button className="btn-secondary flex items-center">
            <Filter className="h-4 w-4 mr-2" />
            More Filters
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="card">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-navy-900">
            {filteredPlayers.length} Players Found
          </h2>
          <select className="input w-auto">
            <option>Sort by: Opta Index</option>
            <option>Sort by: Market Value</option>
            <option>Sort by: Age</option>
          </select>
        </div>

        <div className="space-y-4">
          {filteredPlayers.map((player) => (
            <Link
              key={player.id}
              to={`/dashboard/players/${player.id}`}
              className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  <div className="h-14 w-14 bg-navy-900 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">
                      {player.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-navy-900 text-lg">{player.name}</h3>
                    <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
                      <span>{player.team}</span>
                      <span>•</span>
                      <span>{player.position}</span>
                      <span>•</span>
                      <span>{player.age} years</span>
                      <span>•</span>
                      <span>{player.nationality}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-8">
                  <div className="text-center">
                    <div className="flex items-center text-primary-600">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      <span className="text-2xl font-bold">{player.opta_index}</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Opta Index</p>
                  </div>

                  <div className="text-center">
                    <div className="flex items-center text-gray-900">
                      <DollarSign className="h-4 w-4" />
                      <span className="text-xl font-bold">{player.market_value}M</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">Market Value</p>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
