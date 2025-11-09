import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Target, Check } from 'lucide-react'

export default function SignupPage() {
  const navigate = useNavigate()
  const signup = useAuthStore((state) => state.signup)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await signup(email, password)
      navigate('/dashboard')
    } catch (error) {
      console.error('Signup failed', error)
      alert('Signup failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-navy-800 to-primary-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-5xl grid md:grid-cols-2 gap-8">
        {/* Left: Sign up form */}
        <div>
          <div className="flex justify-center md:justify-start mb-6">
            <div className="flex items-center space-x-2">
              <Target className="h-10 w-10 text-primary-600" />
              <span className="text-3xl font-bold text-navy-900">ScoutAI</span>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-navy-900 mb-2">Create your account</h2>
          <p className="text-gray-600 mb-6">Start finding talent today</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Email</label>
              <input
                type="email"
                className="input"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="label">Password</label>
              <input
                type="password"
                className="input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />
              <p className="text-sm text-gray-500 mt-1">At least 8 characters</p>
            </div>

            <button
              type="submit"
              className="w-full btn-primary"
              disabled={loading}
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 font-medium hover:text-primary-700">
                Sign in
              </Link>
            </p>
          </div>

          <div className="mt-4 text-center">
            <Link to="/" className="text-sm text-gray-500 hover:text-gray-700">
              ← Back to home
            </Link>
          </div>
        </div>

        {/* Right: Features */}
        <div className="hidden md:flex flex-col justify-center bg-gradient-to-br from-navy-900 to-primary-900 text-white rounded-xl p-8">
          <h3 className="text-2xl font-bold mb-6">Start with our Free plan</h3>
          <ul className="space-y-4">
            {[
              '10 player reports per month',
              'Access to top 3 leagues',
              'Basic performance metrics',
              'Community support',
              'Upgrade anytime',
            ].map((feature) => (
              <li key={feature} className="flex items-start">
                <Check className="h-6 w-6 text-primary-400 mr-3 flex-shrink-0" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>

          <div className="mt-8 p-4 bg-white/10 rounded-lg backdrop-blur-sm">
            <p className="text-sm">
              💳 No credit card required<br />
              🔒 Cancel anytime<br />
              ⚡ Get started in seconds
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
