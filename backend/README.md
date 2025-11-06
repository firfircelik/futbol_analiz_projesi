# Sports Analytics Platform - Backend API

## 🚀 FastAPI Backend for Opta-Style Sports Analytics

Professional sports analytics API serving football and basketball data with advanced features:
- ✅ Opta Performance Index
- ✅ Team Fit Analyzer (7-dimensional compatibility)
- ✅ Moneyball Valuation System
- ✅ Scouting Reports
- ✅ Expected Goals (xG) Engine
- ✅ 85+ Leagues Worldwide

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   │   ├── player.py
│   │   ├── team.py
│   │   ├── match.py
│   │   └── analytics.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── player.py
│   │   ├── team.py
│   │   ├── league.py
│   │   └── analytics.py
│   └── api/v1/              # API routes
│       ├── players.py
│       ├── teams.py
│       ├── leagues.py
│       ├── analytics.py
│       ├── team_fit.py
│       ├── scouting.py
│       └── moneyball.py
├── requirements.txt
└── README.md
```

---

## 🔧 Prerequisites

- Python 3.10 or higher
- PostgreSQL 15+ (or SQLite for development)
- Redis (optional, for caching)

---

## 📦 Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in `backend/` directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sports_analytics
# For SQLite (development):
# DATABASE_URL=sqlite:///./sports_analytics.db

# Redis (optional)
REDIS_URL=redis://localhost:6379

# CORS (Frontend URLs)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Debug
DEBUG=True
```

### 3. Setup Database

#### Option A: PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE sports_analytics;
CREATE USER sports_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sports_analytics TO sports_user;
\q
```

#### Option B: SQLite (Quick Development)

```bash
# No setup needed - database file will be created automatically
# Just update DATABASE_URL in .env to:
DATABASE_URL=sqlite:///./sports_analytics.db
```

---

## 🚀 Running the Backend

### Development Mode

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📡 API Endpoints

### Authentication (Coming Soon)
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
```

### Leagues
```
GET    /api/v1/leagues                    # List all leagues
GET    /api/v1/leagues/{league_id}        # Get league details
GET    /api/v1/leagues/{league_id}/standings  # Get standings
```

### Players
```
GET    /api/v1/players                    # List players
GET    /api/v1/players/{player_id}        # Get player details
GET    /api/v1/players/{player_id}/stats  # Get statistics
GET    /api/v1/players/{player_id}/analytics  # Get analytics
POST   /api/v1/players/search             # Search players
POST   /api/v1/players/compare            # Compare players
```

### Teams
```
GET    /api/v1/teams                      # List teams
GET    /api/v1/teams/{team_id}            # Get team details
GET    /api/v1/teams/{team_id}/players    # Get roster
GET    /api/v1/teams/{team_id}/stats      # Get statistics
```

### Analytics
```
GET    /api/v1/analytics/opta-index/{player_id}  # Opta Index
POST   /api/v1/analytics/xg                      # Expected Goals
```

### Team Fit Analyzer ⭐
```
POST   /api/v1/team-fit/analyze           # Analyze player-team fit
POST   /api/v1/team-fit/batch             # Batch analysis
```

### Scouting ⭐
```
GET    /api/v1/scouting/report/{player_id}  # Generate report
GET    /api/v1/scouting/targets              # Get targets
```

### Moneyball ⭐
```
GET    /api/v1/moneyball/undervalued         # Find undervalued players
GET    /api/v1/moneyball/value-analysis/{player_id}  # Value analysis
POST   /api/v1/moneyball/budget-optimizer    # Optimize budget
```

---

## 💡 Usage Examples

### 1. Get Player Opta Index

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/opta-index/messi_1" | json_pp
```

Response:
```json
{
  "player_id": "messi_1",
  "player_name": "Lionel Messi",
  "position": "RW",
  "opta_index": 92.5,
  "rating": "world_class",
  "breakdown": {
    "goals": 18.5,
    "assists": 12.0,
    "passing": 15.2
  },
  "strengths": ["Exceptional finishing", "World-class playmaking"],
  "weaknesses": []
}
```

### 2. Analyze Team Fit

```bash
curl -X POST "http://localhost:8000/api/v1/team-fit/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": "haaland_1",
    "team_profile": {
      "team_name": "Manchester City",
      "playing_style": "POSSESSION_BASED",
      "formation": "4-3-3",
      "budget_millions": 100,
      "priority_positions": ["ST"],
      "desired_traits": ["pace", "finishing"],
      "requires_pace": true,
      "requires_technique": true
    }
  }' | json_pp
```

Response:
```json
{
  "player_id": "haaland_1",
  "player_name": "Erling Haaland",
  "team_name": "Manchester City",
  "overall_fit_score": 88.5,
  "fit_rating": "EXCELLENT_FIT",
  "recommendation": "STRONG_BUY",
  "statistical_fit": 92.0,
  "tactical_fit": 85.0,
  "key_strengths": ["Elite finishing", "Perfect pace for counter-attacks"],
  "adaptation_timeline": "IMMEDIATE"
}
```

### 3. Find Undervalued Players

```bash
curl -X GET "http://localhost:8000/api/v1/moneyball/undervalued?position=ST&limit=10" | json_pp
```

### 4. Generate Scouting Report

```bash
curl -X GET "http://localhost:8000/api/v1/scouting/report/player_123" | json_pp
```

---

## 🗄️ Database Models

### Player Model

Key fields:
- Basic: name, age, nationality, position, team, league
- Physical: height, weight, preferred_foot
- Performance: goals, assists, matches_played, minutes
- Advanced: passes_completed, shots, xG, dribbles, tackles
- Attributes: pace, shooting, passing, dribbling, defending (0-100)
- Analytics: opta_index, form_rating
- Market: market_value_millions, contract_expiry

### Team Model

Key fields:
- Basic: name, league, stadium, city
- Tactical: playing_style, formation, manager
- Performance: wins, draws, losses, goals_for, goals_against, points

### League Model

Key fields:
- Basic: name, sport (football/basketball), country, prestige
- External: thesportsdb_id, competition_id

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Test specific module
pytest app/api/v1/test_players.py
```

---

## 📊 Database Migrations

Using Alembic for database migrations:

```bash
# Initialize (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 🔐 Security

Current implementation:
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ⏳ JWT authentication (coming soon)
- ⏳ Rate limiting (coming soon)

---

## 🚀 Performance Optimization

1. **Database Indexing**:
   - Player name, position, opta_index
   - Team name, league_id
   - Match date, league_id

2. **Caching** (if Redis is enabled):
   - Analytics results cached for 5-30 minutes
   - Player data cached for 1 hour
   - League standings cached for 6 hours

3. **Pagination**:
   - Default: 20 items per page
   - Max: 100 items per page

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check connection
psql -h localhost -U sports_user -d sports_analytics
```

### Import Errors

Make sure you're running from the `backend/` directory:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

---

## 📈 Monitoring

View real-time logs:
```bash
# Development
tail -f uvicorn.log

# Production
tail -f /var/log/sports-analytics/api.log
```

---

## 🔗 Integration with Frontend

The backend is designed to work seamlessly with the React frontend.

Frontend should make requests to:
```
http://localhost:8000/api/v1/...
```

Example frontend service:
```typescript
// playerService.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const getPlayer = async (playerId: string) => {
  const response = await axios.get(`${API_BASE_URL}/players/${playerId}`);
  return response.data;
};
```

---

## 📚 Additional Documentation

- [Full Stack Architecture](../docs/FULL_STACK_ARCHITECTURE.md)
- [Data Coverage Comparison](../docs/DATA_COVERAGE_COMPARISON.md)
- [API Documentation](http://localhost:8000/api/docs) (when running)

---

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Add tests
4. Submit PR

---

## 📝 License

MIT License

---

## 🆘 Support

- **GitHub Issues**: [Report issues](https://github.com/firfircelik/futbol_analiz_projesi/issues)
- **Documentation**: Check `/api/docs` when running

---

**Built with ❤️ for sports analytics professionals**
