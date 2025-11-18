import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  user_id: string
  email: string
  plan: {
    tier: string
    name: string
    price_monthly: number
  }
  quotas: {
    player_reports: { used: number; limit: number; remaining: number }
    team_fit: { used: number; limit: number; remaining: number }
    api_requests: { used: number; limit: number; remaining: number }
  }
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  setToken: (token: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        // TODO: Implement real API call
        // const response = await api.post('/auth/login', { email, password })

        // Mock login
        const mockToken = 'mock-jwt-token'
        const mockUser: User = {
          user_id: 'user_123',
          email,
          plan: {
            tier: 'professional',
            name: 'Professional',
            price_monthly: 99,
          },
          quotas: {
            player_reports: { used: 45, limit: 500, remaining: 455 },
            team_fit: { used: 12, limit: 999999, remaining: 999987 },
            api_requests: { used: 3456, limit: 10000, remaining: 6544 },
          },
        }

        set({ token: mockToken, user: mockUser, isAuthenticated: true })
      },

      signup: async (email: string, password: string) => {
        // TODO: Implement real API call
        const mockToken = 'mock-jwt-token'
        const mockUser: User = {
          user_id: 'user_new',
          email,
          plan: {
            tier: 'free',
            name: 'Free',
            price_monthly: 0,
          },
          quotas: {
            player_reports: { used: 0, limit: 10, remaining: 10 },
            team_fit: { used: 0, limit: 0, remaining: 0 },
            api_requests: { used: 0, limit: 0, remaining: 0 },
          },
        }

        set({ token: mockToken, user: mockUser, isAuthenticated: true })
      },

      logout: () => {
        set({ token: null, user: null, isAuthenticated: false })
      },

      setUser: (user: User) => {
        set({ user })
      },

      setToken: (token: string) => {
        set({ token, isAuthenticated: true })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
