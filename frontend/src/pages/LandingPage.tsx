import { Link } from 'react-router-dom'
import { TrendingUp, Target, DollarSign, Zap, BarChart3, Users } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Target className="h-8 w-8 text-primary-600" />
            <span className="text-2xl font-bold text-navy-900">ScoutAI</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-700 hover:text-primary-600">Features</a>
            <a href="#pricing" className="text-gray-700 hover:text-primary-600">Pricing</a>
            <Link to="/login" className="text-gray-700 hover:text-primary-600">Login</Link>
          </nav>
          <Link to="/signup" className="btn-primary">
            Start Free Trial
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="bg-gradient-to-br from-navy-900 via-navy-800 to-primary-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6">
            Professional Sports Analytics<br />for Everyone
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-200 max-w-3xl mx-auto">
            Get the insights used by top clubs, at a fraction of the cost. No PhD required.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup" className="bg-primary-500 hover:bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors">
              Start Free Trial
            </Link>
            <a href="#features" className="bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors backdrop-blur-sm">
              Learn More
            </a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
            {[
              { label: 'Leagues Covered', value: '50+' },
              { label: 'Opta-Level Coverage', value: '85%' },
              { label: 'Starting Price', value: '€29' },
              { label: 'Happy Users', value: '3,000+' },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="text-4xl font-bold text-primary-400">{stat.value}</div>
                <div className="text-gray-300 mt-2">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-navy-900 mb-4">
              Everything You Need to Find Talent
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Professional-grade analytics that help you make better decisions
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Target className="h-8 w-8" />,
                title: 'Team Fit Analysis',
                description: '7-dimensional compatibility scoring tells you exactly how well a player will fit your team',
                badge: 'UNIQUE',
              },
              {
                icon: <DollarSign className="h-8 w-8" />,
                title: 'Moneyball Valuation',
                description: 'Find undervalued talent before your competitors with our market inefficiency detection',
                badge: 'UNIQUE',
              },
              {
                icon: <BarChart3 className="h-8 w-8" />,
                title: 'Opta Performance Index',
                description: 'Professional player ratings (0-100) used by top clubs. Position-specific scoring.',
              },
              {
                icon: <TrendingUp className="h-8 w-8" />,
                title: 'Expected Goals (xG)',
                description: 'Advanced shot quality analysis. Know which chances should have been scored.',
              },
              {
                icon: <Zap className="h-8 w-8" />,
                title: '50+ Leagues',
                description: 'From Premier League to lower tiers. Complete coverage of major competitions.',
              },
              {
                icon: <Users className="h-8 w-8" />,
                title: 'API Access',
                description: 'Integrate our data into your tools. Build custom dashboards and analytics.',
              },
            ].map((feature) => (
              <div key={feature.title} className="card hover:shadow-lg transition-shadow">
                {feature.badge && (
                  <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-semibold px-3 py-1 rounded-full mb-3">
                    {feature.badge}
                  </span>
                )}
                <div className="text-primary-600 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-navy-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-navy-900 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to Find Your Next Star Player?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Join 3,000+ scouts, agents, and clubs using ScoutAI
          </p>
          <Link to="/signup" className="btn-primary bg-primary-500 hover:bg-primary-600 text-lg px-8 py-4">
            Get Started Free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p>&copy; 2025 ScoutAI. All rights reserved.</p>
            </div>
            <div className="flex space-x-6">
              <a href="#" className="hover:text-white">Privacy</a>
              <a href="#" className="hover:text-white">Terms</a>
              <a href="#" className="hover:text-white">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
