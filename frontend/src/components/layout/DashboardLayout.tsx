import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import {
  Home,
  Search,
  Target,
  Settings,
  LogOut,
  Menu,
  X,
  CreditCard,
  BarChart3,
} from 'lucide-react'
import { useState } from 'react'

export default function DashboardLayout() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Search Players', href: '/dashboard/search', icon: Search },
    { name: 'Team Fit', href: '/dashboard/team-fit', icon: Target },
    { name: 'Settings', href: '/dashboard/settings', icon: Settings },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const QuotaBar = ({ label, used, limit }: { label: string; used: number; limit: number }) => {
    const percentage = limit === 999999 ? 100 : (used / limit) * 100
    const isUnlimited = limit === 999999

    return (
      <div className="mb-3">
        <div className="flex justify-between text-xs text-gray-600 mb-1">
          <span>{label}</span>
          <span>{isUnlimited ? 'Unlimited' : `${used}/${limit}`}</span>
        </div>
        {!isUnlimited && (
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${percentage > 80 ? 'bg-red-500' : 'bg-primary-500'}`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-gray-900 bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-50 w-64 h-full bg-white border-r border-gray-200 transform transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-4 border-b flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Target className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-navy-900">ScoutAI</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* User info & Plan */}
          <div className="p-4 border-b">
            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                <span className="text-primary-700 font-semibold">
                  {user?.email?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.email}
                </p>
                <p className="text-xs text-gray-500">{user?.plan.name} Plan</p>
              </div>
            </div>

            {/* Quotas */}
            {user?.quotas && (
              <div className="space-y-2">
                <QuotaBar
                  label="Player Reports"
                  used={user.quotas.player_reports.used}
                  limit={user.quotas.player_reports.limit}
                />
                <QuotaBar
                  label="Team Fit"
                  used={user.quotas.team_fit.used}
                  limit={user.quotas.team_fit.limit}
                />
              </div>
            )}

            <Link
              to="/pricing"
              className="mt-3 flex items-center justify-center text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              <CreditCard className="h-4 w-4 mr-1" />
              Upgrade Plan
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <item.icon className="h-5 w-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* Logout */}
          <div className="p-4 border-t">
            <button
              onClick={handleLogout}
              className="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 w-full transition-colors"
            >
              <LogOut className="h-5 w-5" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
          <div className="px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden"
            >
              <Menu className="h-6 w-6" />
            </button>

            <div className="flex-1"></div>

            <div className="flex items-center space-x-4">
              <a
                href="/api/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 hover:text-gray-900 flex items-center"
              >
                <BarChart3 className="h-4 w-4 mr-1" />
                API Docs
              </a>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
