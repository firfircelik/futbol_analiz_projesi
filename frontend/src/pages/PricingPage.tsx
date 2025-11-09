import { Link } from 'react-router-dom'
import { Check, Target } from 'lucide-react'

export default function PricingPage() {
  const plans = [
    {
      name: 'Free',
      price: 0,
      description: 'Try out ScoutAI',
      features: ['10 player reports/month', '3 leagues access', 'Basic metrics', 'Community support'],
      cta: 'Get Started',
      popular: false,
    },
    {
      name: 'Scout',
      price: 29,
      description: 'For enthusiasts',
      features: ['100 player reports/month', '10 leagues access', 'Team Fit Analysis', 'PDF exports', 'API access (1K req/mo)'],
      cta: 'Start Trial',
      popular: false,
    },
    {
      name: 'Professional',
      price: 99,
      description: 'For serious analysts',
      features: ['500 player reports/month', '50+ leagues access', 'Unlimited Team Fit', 'Moneyball Valuation', 'Advanced metrics (xG, xA)', 'Excel exports', 'API access (10K req/mo)', 'Priority support'],
      cta: 'Start Trial',
      popular: true,
    },
    {
      name: 'Club',
      price: 299,
      description: 'For professional teams',
      features: ['Unlimited reports', 'All leagues', '5 user seats', 'White-label reports', 'Live match analysis', 'Custom integrations', 'API access (100K req/mo)', 'Dedicated support'],
      cta: 'Contact Sales',
      popular: false,
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Target className="h-8 w-8 text-primary-600" />
            <span className="text-2xl font-bold text-navy-900">ScoutAI</span>
          </Link>
          <Link to="/login" className="btn-primary">Sign In</Link>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-navy-900 mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-gray-600">Choose the plan that's right for you</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`card relative ${plan.popular ? 'border-2 border-primary-500 shadow-xl' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    MOST POPULAR
                  </span>
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-navy-900 mb-2">{plan.name}</h3>
                <p className="text-gray-600 mb-4">{plan.description}</p>
                <div className="text-4xl font-bold text-navy-900">
                  €{plan.price}
                  <span className="text-lg text-gray-600 font-normal">/mo</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start">
                    <Check className="h-5 w-5 text-primary-600 mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <Link
                to="/signup"
                className={`block text-center py-3 rounded-lg font-semibold transition-colors ${
                  plan.popular
                    ? 'bg-primary-600 text-white hover:bg-primary-700'
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
