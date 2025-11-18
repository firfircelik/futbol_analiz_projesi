import { useAuthStore } from '../store/authStore'
import { User, CreditCard, Bell, Shield } from 'lucide-react'

export default function SettingsPage() {
  const user = useAuthStore((state) => state.user)

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-navy-900">Settings</h1>
        <p className="text-gray-600 mt-2">Manage your account and preferences</p>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="card space-y-2">
            {[
              { name: 'Account', icon: User, active: true },
              { name: 'Billing', icon: CreditCard },
              { name: 'Notifications', icon: Bell },
              { name: 'Security', icon: Shield },
            ].map((item) => (
              <button
                key={item.name}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                  item.active
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span className="font-medium">{item.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3 space-y-6">
          {/* Account Info */}
          <div className="card">
            <h2 className="text-xl font-bold text-navy-900 mb-6">Account Information</h2>

            <div className="space-y-4">
              <div>
                <label className="label">Email</label>
                <input type="email" className="input" value={user?.email} readOnly />
              </div>

              <div>
                <label className="label">Full Name</label>
                <input type="text" className="input" placeholder="Enter your name" />
              </div>

              <div>
                <label className="label">Organization</label>
                <input type="text" className="input" placeholder="Club or agency name" />
              </div>

              <button className="btn-primary">Save Changes</button>
            </div>
          </div>

          {/* Current Plan */}
          <div className="card">
            <h2 className="text-xl font-bold text-navy-900 mb-6">Current Plan</h2>

            <div className="bg-gradient-to-br from-primary-50 to-white p-6 rounded-lg border-2 border-primary-200 mb-4">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-2xl font-bold text-navy-900">{user?.plan.name}</h3>
                  <p className="text-gray-600 mt-1">
                    €{user?.plan.price_monthly}/month
                  </p>
                </div>
                <span className="bg-primary-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  Active
                </span>
              </div>

              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-sm text-gray-600">Reports/month</div>
                  <div className="text-xl font-bold text-navy-900">
                    {user?.quotas.player_reports.limit === 999999
                      ? 'Unlimited'
                      : user?.quotas.player_reports.limit}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Team Fit</div>
                  <div className="text-xl font-bold text-navy-900">
                    {user?.quotas.team_fit.limit === 999999
                      ? 'Unlimited'
                      : user?.quotas.team_fit.limit}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">API Calls/month</div>
                  <div className="text-xl font-bold text-navy-900">
                    {user?.quotas.api_requests.limit === 999999
                      ? 'Unlimited'
                      : user?.quotas.api_requests.limit.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-4">
              <button className="btn-primary">Upgrade Plan</button>
              <button className="btn-secondary">Cancel Subscription</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
