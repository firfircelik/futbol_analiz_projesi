# ScoutAI Frontend

Modern, professional React + TypeScript frontend for the ScoutAI sports analytics platform.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

## 🎨 Features

### ✅ Modern Tech Stack
- **React 18** - Latest React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **React Query** - Server state management
- **Zustand** - Client state management
- **Lucide React** - Beautiful icons

### ✅ Pages & Features
- **Landing Page** - Marketing site with pricing
- **Authentication** - Login/Signup with JWT
- **Dashboard** - Overview with stats and quick actions
- **Player Search** - Advanced search with filters
- **Player Profile** - Detailed player analytics
- **Team Fit Analyzer** - Unique 7-dimensional compatibility
- **Settings** - Account and billing management
- **Pricing** - Public pricing page

### ✅ Professional Design
- Responsive (mobile, tablet, desktop)
- Dark navy + green color scheme
- Card-based UI
- Smooth transitions
- Loading states
- Error handling

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── layout/
│   │       └── DashboardLayout.tsx    # Main app layout with sidebar
│   ├── pages/
│   │   ├── LandingPage.tsx           # Marketing homepage
│   │   ├── LoginPage.tsx             # User login
│   │   ├── SignupPage.tsx            # User registration
│   │   ├── DashboardPage.tsx         # Main dashboard
│   │   ├── PlayerSearchPage.tsx      # Search interface
│   │   ├── PlayerProfilePage.tsx     # Player details
│   │   ├── TeamFitPage.tsx           # Team Fit analyzer
│   │   ├── SettingsPage.tsx          # User settings
│   │   └── PricingPage.tsx           # Public pricing
│   ├── store/
│   │   └── authStore.ts              # Authentication state
│   ├── lib/
│   │   └── api.ts                    # API client with interceptors
│   ├── App.tsx                       # Main app with routing
│   ├── main.tsx                      # Entry point
│   └── index.css                     # Global styles
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## 🔧 Development

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Lint Code
```bash
npm run lint
```

## 🔌 API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`.

### API Endpoints Used:
- `POST /auth/login` - User authentication
- `POST /auth/signup` - User registration
- `GET /api/v1/me` - Current user info
- `GET /api/v1/pricing` - Pricing plans
- `GET /api/v1/players/search` - Search players
- `GET /api/v1/players/:id` - Player profile
- `POST /api/v1/team-fit/analyze` - Team Fit analysis

### Authentication
JWT tokens stored in localStorage via Zustand persist middleware.

## 🎨 Styling

Uses Tailwind CSS with custom configuration:

**Colors:**
- Primary: Green (#10b981)
- Navy: Dark blue (#1e3a8a)

**Custom Classes:**
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.card` - Card container
- `.input` - Form input
- `.label` - Form label

## 📱 Responsive Breakpoints

- **sm:** 640px
- **md:** 768px
- **lg:** 1024px
- **xl:** 1280px

## 🔐 Authentication Flow

1. User enters email/password
2. Frontend calls `/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage
5. Token included in all API requests
6. Auto-redirect on 401 (token expired)

## 💾 State Management

### Global State (Zustand)
- User authentication
- User profile
- JWT token

### Server State (React Query)
- Player data
- Search results
- Team Fit analyses

## 🚢 Deployment

### Build for Production
```bash
npm run build
```

Output in `dist/` folder.

### Deploy to Netlify/Vercel
```bash
# Netlify
netlify deploy --prod

# Vercel
vercel --prod
```

### Environment Variables
Create `.env` file:
```
VITE_API_URL=https://api.scoutai.com
```

## 🧪 Testing

Mock data included for development:
- Mock users
- Mock players
- Mock Team Fit results

Replace with real API calls in production.

## 📈 Performance

- Code splitting with React lazy loading
- Optimized images
- Tailwind CSS purging
- Vite bundling
- Tree shaking

## 🎯 Next Steps

1. **Connect Real API** - Replace mock data
2. **Add Charts** - Use Recharts for visualizations
3. **PDF Generation** - Client-side PDF export
4. **Dark Mode** - Toggle theme
5. **Internationalization** - Multi-language support

## 💡 Tips

**Hot Reload:**
Changes auto-refresh during development.

**TypeScript:**
Strict mode enabled. Fix all type errors.

**Tailwind:**
Use utility classes. Avoid custom CSS.

**Components:**
Create reusable components in `components/`.

---

**Built with ❤️ for ScoutAI**
