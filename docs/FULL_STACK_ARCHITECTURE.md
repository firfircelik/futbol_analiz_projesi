# Full-Stack Application Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + TypeScript)            │
│  ┌──────────────┬──────────────┬──────────────┬──────────┐ │
│  │  Dashboard   │   Players    │  Team Fit    │ Scouting │ │
│  │  Live Scores │   Analysis   │  Analyzer    │ Reports  │ │
│  └──────────────┴──────────────┴──────────────┴──────────┘ │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │  Moneyball   │  Comparisons │  Visualizations          │ │
│  │  Valuation   │  & Stats     │  Charts & Dashboards     │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API + WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI + Python)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API Layer                          │  │
│  │  /api/v1/leagues  /api/v1/players  /api/v1/teams    │  │
│  │  /api/v1/analytics  /api/v1/team-fit  /api/v1/scout │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Analytics Engine                         │  │
│  │  • Opta Analytics    • Team Fit Analyzer             │  │
│  │  • Moneyball System  • xG Engine                     │  │
│  │  • Performance Index • Scouting Reports              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Data Collection Layer                    │  │
│  │  • StatsBomb API    • BallDontLie API                │  │
│  │  • TheSportsDB API  • Data Aggregator                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                     │
│  • Players  • Teams  • Matches  • Analytics  • Cache        │
└─────────────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
futbol_analiz_projesi/
│
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # App configuration
│   │   ├── database.py              # Database connection
│   │   │
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── player.py
│   │   │   ├── team.py
│   │   │   ├── match.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── player.py
│   │   │   ├── team.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── api/                     # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── leagues.py
│   │   │   │   ├── players.py
│   │   │   │   ├── teams.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── team_fit.py
│   │   │   │   ├── scouting.py
│   │   │   │   └── moneyball.py
│   │   │
│   │   ├── services/                # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── data_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── team_fit_service.py
│   │   │   └── cache_service.py
│   │   │
│   │   └── utils/                   # Utilities
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                         # React Frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── App.tsx                  # Main app component
│   │   ├── index.tsx                # Entry point
│   │   ├── index.css                # Global styles
│   │   │
│   │   ├── components/              # Reusable components
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── charts/
│   │   │   │   ├── RadarChart.tsx
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── BarChart.tsx
│   │   │   │   └── ShotChart.tsx
│   │   │   ├── cards/
│   │   │   │   ├── PlayerCard.tsx
│   │   │   │   ├── TeamCard.tsx
│   │   │   │   └── MatchCard.tsx
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Input.tsx
│   │   │       ├── Select.tsx
│   │   │       └── Loading.tsx
│   │   │
│   │   ├── pages/                   # Page components
│   │   │   ├── Dashboard.tsx        # Home dashboard
│   │   │   ├── Players.tsx          # Player analysis
│   │   │   ├── Teams.tsx            # Team analysis
│   │   │   ├── TeamFit.tsx          # Team fit analyzer
│   │   │   ├── Scouting.tsx         # Scouting reports
│   │   │   ├── Moneyball.tsx        # Valuation system
│   │   │   └── Comparisons.tsx      # Player/team comparisons
│   │   │
│   │   ├── services/                # API services
│   │   │   ├── api.ts               # Axios instance
│   │   │   ├── playerService.ts
│   │   │   ├── teamService.ts
│   │   │   └── analyticsService.ts
│   │   │
│   │   ├── hooks/                   # Custom hooks
│   │   │   ├── usePlayer.ts
│   │   │   ├── useTeam.ts
│   │   │   └── useAnalytics.ts
│   │   │
│   │   ├── store/                   # State management
│   │   │   ├── index.ts
│   │   │   ├── playerSlice.ts
│   │   │   └── teamSlice.ts
│   │   │
│   │   ├── types/                   # TypeScript types
│   │   │   ├── player.ts
│   │   │   ├── team.ts
│   │   │   └── analytics.ts
│   │   │
│   │   └── utils/                   # Utilities
│   │       ├── formatters.ts
│   │       └── constants.ts
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml               # Docker orchestration
├── .env.example                     # Environment variables template
└── README.md
```

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Caching:** Redis
- **Task Queue:** Celery (for background tasks)
- **API Docs:** Swagger/OpenAPI (built-in)

### Frontend
- **Framework:** React 18
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 3
- **State Management:** Redux Toolkit
- **Routing:** React Router v6
- **Charts:** Recharts + D3.js
- **API Client:** Axios
- **Build Tool:** Vite

### DevOps
- **Containerization:** Docker + Docker Compose
- **Reverse Proxy:** Nginx
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana (optional)

## 📡 API Endpoints

### Authentication (Future)
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me
```

### Leagues
```
GET    /api/v1/leagues                    # List all leagues
GET    /api/v1/leagues/{league_id}        # Get league details
GET    /api/v1/leagues/{league_id}/teams  # Get teams in league
GET    /api/v1/leagues/{league_id}/standings
```

### Players
```
GET    /api/v1/players                    # Search players
GET    /api/v1/players/{player_id}        # Get player details
GET    /api/v1/players/{player_id}/stats  # Get player statistics
GET    /api/v1/players/{player_id}/analytics  # Get advanced analytics
GET    /api/v1/players/compare            # Compare multiple players
POST   /api/v1/players/search             # Advanced search
```

### Teams
```
GET    /api/v1/teams                      # List teams
GET    /api/v1/teams/{team_id}            # Get team details
GET    /api/v1/teams/{team_id}/players    # Get team roster
GET    /api/v1/teams/{team_id}/stats      # Get team statistics
GET    /api/v1/teams/{team_id}/analytics  # Get team analytics
```

### Analytics
```
GET    /api/v1/analytics/opta-index/{player_id}  # Opta performance index
GET    /api/v1/analytics/xg/{match_id}           # Expected goals
POST   /api/v1/analytics/performance             # Performance analysis
```

### Team Fit Analyzer
```
POST   /api/v1/team-fit/analyze           # Analyze player-team fit
POST   /api/v1/team-fit/batch             # Batch analyze multiple players
GET    /api/v1/team-fit/recommendations/{team_id}  # Get recommendations
```

### Scouting
```
GET    /api/v1/scouting/report/{player_id}  # Generate scouting report
POST   /api/v1/scouting/generate             # Generate custom report
GET    /api/v1/scouting/targets              # Get scouting targets
```

### Moneyball
```
GET    /api/v1/moneyball/undervalued         # Find undervalued players
GET    /api/v1/moneyball/value-analysis/{player_id}
POST   /api/v1/moneyball/budget-optimizer    # Optimize squad within budget
```

### Live Scores
```
GET    /api/v1/live/scores                   # Get live scores
WS     /ws/live                              # WebSocket for live updates
```

## 🗄️ Database Schema

### Players Table
```sql
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INTEGER,
    nationality VARCHAR(100),
    position VARCHAR(50),
    team_id INTEGER REFERENCES teams(id),
    league_id INTEGER REFERENCES leagues(id),

    -- Physical
    height_cm FLOAT,
    weight_kg FLOAT,
    preferred_foot VARCHAR(10),

    -- Market
    market_value_millions FLOAT,
    contract_expiry DATE,

    -- Technical attributes (0-100)
    pace INTEGER,
    shooting INTEGER,
    passing INTEGER,
    dribbling INTEGER,
    defending INTEGER,
    physical INTEGER,

    -- Analytics
    opta_index FLOAT,

    -- Metadata
    data_completeness FLOAT,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Teams Table
```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    league_id INTEGER REFERENCES leagues(id),
    stadium VARCHAR(255),
    founded_year INTEGER,

    -- Tactical
    playing_style VARCHAR(50),
    formation VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Matches Table
```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(100) UNIQUE NOT NULL,
    league_id INTEGER REFERENCES leagues(id),
    home_team_id INTEGER REFERENCES teams(id),
    away_team_id INTEGER REFERENCES teams(id),

    match_date TIMESTAMP,
    home_score INTEGER,
    away_score INTEGER,

    status VARCHAR(20),  -- 'scheduled', 'live', 'finished'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Analytics Cache Table
```sql
CREATE TABLE analytics_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_type VARCHAR(50),  -- 'opta_index', 'team_fit', 'xg', etc.
    entity_id VARCHAR(100),
    data JSONB NOT NULL,

    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Data Flow

### Player Analysis Flow
```
1. User requests player analysis
   ↓
2. Frontend → GET /api/v1/players/{id}/analytics
   ↓
3. Backend checks cache
   ↓
4. If not cached:
   - Fetch from data collection APIs
   - Run analytics engine
   - Calculate Opta Index
   - Store in cache
   ↓
5. Return comprehensive data
   ↓
6. Frontend renders visualizations
```

### Team Fit Analysis Flow
```
1. User inputs team profile + target position
   ↓
2. Frontend → POST /api/v1/team-fit/analyze
   ↓
3. Backend:
   - Loads team profile
   - Queries players in position
   - Runs 7-dimensional fit analysis
   - Ranks by compatibility score
   ↓
4. Return top matches with scores
   ↓
5. Frontend displays ranked list + details
```

## 🚀 Deployment Architecture

### Development
```
docker-compose up
```

### Production
```
┌─────────────┐
│   Nginx     │  Port 80/443
│   (Proxy)   │
└──────┬──────┘
       │
       ├──────► Frontend (React) - Port 3000
       │
       └──────► Backend (FastAPI) - Port 8000
                    │
                    ├──► PostgreSQL - Port 5432
                    └──► Redis - Port 6379
```

## 🔐 Security Considerations

- JWT authentication (future)
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (React auto-escaping)

## 📊 Performance Optimizations

- Database indexing on frequently queried fields
- Redis caching for expensive computations
- Lazy loading for heavy components
- API response pagination
- Image optimization
- Code splitting in frontend

## 🧪 Testing Strategy

- Backend: pytest + pytest-asyncio
- Frontend: Jest + React Testing Library
- E2E: Playwright
- API: Swagger UI testing

## 📈 Monitoring

- API response times
- Error rates
- Cache hit rates
- Database query performance
- User analytics (page views, popular features)

---

**Next Steps:**
1. ✅ Setup backend FastAPI structure
2. ✅ Create database models
3. ✅ Build API endpoints
4. ✅ Setup React frontend
5. ✅ Create core UI components
6. ✅ Integrate analytics modules
7. ✅ Configure Docker deployment
