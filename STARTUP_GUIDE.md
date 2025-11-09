# 🚀 Sports Analytics Platform - Complete Startup Guide

## Welcome! Let's Build This App FULLY!

This guide will help you get the **complete Sports Analytics Platform** up and running with:
- ✅ FastAPI Backend with all analytics
- ✅ PostgreSQL Database
- ✅ Redis Caching
- ✅ React Frontend (TypeScript + Tailwind)
- ✅ Docker Deployment
- ✅ 85+ Leagues Worldwide
- ✅ Opta-Style Analytics

---

## 📋 Prerequisites

### Required Software:
- **Python 3.10+**
- **Node.js 18+** and npm
- **Docker** and Docker Compose (recommended)
- **PostgreSQL 15+** (if not using Docker)
- **Git**

### System Requirements:
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Linux, macOS, or Windows (WSL2)

---

## 🎯 Quick Start (Docker - EASIEST!)

### Step 1: Clone Repository

```bash
git clone https://github.com/firfircelik/futbol_analiz_projesi.git
cd futbol_analiz_projesi
```

### Step 2: Start Everything with Docker

```bash
# Start all services (Database + Redis + Backend)
docker-compose up -d

# Check services are running
docker-compose ps
```

That's it! 🎉

**API will be available at:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Frontend: http://localhost:3000 (when ready)

### Step 3: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get all leagues
curl http://localhost:8000/api/v1/leagues | json_pp

# Swagger UI (in browser)
open http://localhost:8000/api/docs
```

---

## 🔧 Manual Setup (Without Docker)

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Setup Database

**Option A: PostgreSQL (Production)**

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

**Option B: SQLite (Quick Development)**

Just update `.env`:
```
DATABASE_URL=sqlite:///./sports_analytics.db
```

#### 3. Create Environment File

```bash
# Create .env in backend/ directory
cat > backend/.env <<EOF
DATABASE_URL=postgresql://sports_user:your_password@localhost:5432/sports_analytics
REDIS_URL=redis://localhost:6379
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
EOF
```

#### 4. Run Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend is now running at http://localhost:8000

---

### Frontend Setup (Coming in next phase)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend will run at http://localhost:3000

---

## 📊 Populate Database with Sample Data

### Option 1: Using Python Script

```python
# scripts/populate_db.py
import sys
sys.path.append('..')

from backend.app.database import SessionLocal
from backend.app.models.player import Player
from backend.app.models.team import Team, League

db = SessionLocal()

# Create sample league
league = League(
    league_id="EPL",
    name="English Premier League",
    sport="football",
    country="England",
    prestige="elite"
)
db.add(league)
db.commit()

# Create sample team
team = Team(
    team_id="mancity_1",
    name="Manchester City",
    league_id=league.id,
    playing_style="possession",
    formation="4-3-3"
)
db.add(team)
db.commit()

# Create sample player
player = Player(
    player_id="haaland_1",
    name="Erling Haaland",
    age=23,
    position="ST",
    nationality="Norway",
    team_id=team.id,
    league_id=league.id,
    goals=36,
    assists=8,
    matches_played=35,
    pace=89,
    shooting=94,
    passing=65,
    dribbling=80,
    defending=45,
    physical=88,
    opta_index=92.5,
    market_value_millions=180.0
)
db.add(player)
db.commit()

print("✅ Sample data added!")
db.close()
```

Run it:
```bash
python scripts/populate_db.py
```

### Option 2: Load from Real APIs

```python
# scripts/load_real_data.py
import sys
sys.path.append('..')

from src.data_collection.free_basketball_api import FreeBasketballAPI
from backend.app.database import SessionLocal
from backend.app.models.player import Player
from backend.app.models.team import Team, League

# Load NBA data
nba_api = FreeBasketballAPI()
players_df = nba_api.get_all_nba_players(max_pages=2)

db = SessionLocal()

# Create NBA league
nba_league = League(
    league_id="NBA",
    name="National Basketball Association",
    sport="basketball",
    country="USA",
    prestige="elite"
)
db.add(nba_league)
db.commit()

# Add players
for _, row in players_df.head(100).iterrows():
    player = Player(
        player_id=f"nba_{row['player_id']}",
        name=row['full_name'],
        position=row.get('position', 'G'),
        team_id=None,  # Would need to create teams first
        league_id=nba_league.id,
        opta_index=70.0  # Default, would calculate
    )
    db.add(player)

db.commit()
db.close()
print("✅ NBA data loaded!")
```

---

## 🧪 Testing the Application

### 1. Test Backend API

```bash
# Install httpie (optional, better than curl)
pip install httpie

# Test endpoints
http GET http://localhost:8000/
http GET http://localhost:8000/api/v1/leagues
http GET http://localhost:8000/api/v1/players
```

### 2. Test Opta Analytics

```bash
# Get Opta Index for a player
http GET "http://localhost:8000/api/v1/analytics/opta-index/haaland_1"
```

### 3. Test Team Fit Analyzer

```bash
http POST "http://localhost:8000/api/v1/team-fit/analyze" \
  player_id="haaland_1" \
  team_profile:='{"team_name":"Liverpool","playing_style":"HIGH_PRESS","formation":"4-3-3","budget_millions":100,"priority_positions":["ST"],"desired_traits":["pace","finishing"],"requires_pace":true,"requires_technique":false}'
```

### 4. Test Moneyball System

```bash
# Find undervalued players
http GET "http://localhost:8000/api/v1/moneyball/undervalued?limit=10"
```

---

## 📱 Frontend Features (When Ready)

The React frontend will include:

### Pages:
1. **Dashboard** - Live scores, league overviews
2. **Players** - Search, analyze, compare players
3. **Teams** - Team analysis, rosters, statistics
4. **Team Fit Analyzer** - Find perfect players for your team
5. **Scouting** - Generate professional scouting reports
6. **Moneyball** - Find undervalued players, budget optimization
7. **Analytics** - Deep dive into xG, Opta Index, advanced metrics

### Components:
- Player cards
- Radar charts for attributes
- Shot charts (football pitch / basketball court)
- Live score widgets
- Comparison tables
- Data visualizations

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Check database connection
psql -h localhost -U sports_user -d sports_analytics

# Check logs
docker-compose logs backend
```

### Database connection errors

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Restart PostgreSQL
sudo service postgresql restart

# Check database exists
sudo -u postgres psql -l | grep sports_analytics
```

### Docker issues

```bash
# Stop all containers
docker-compose down

# Remove volumes and restart fresh
docker-compose down -v
docker-compose up -d

# View logs
docker-compose logs -f
```

### Import errors in Python

```bash
# Make sure you're in the right directory
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Or add to .bashrc / .zshrc:
echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/futbol_analiz_projesi"' >> ~/.bashrc
```

---

## 🚀 Development Workflow

### Daily Development

```bash
# Start services
docker-compose up -d

# Follow backend logs
docker-compose logs -f backend

# Make changes to code (auto-reload enabled)

# Run tests
docker-compose exec backend pytest

# Stop services
docker-compose down
```

### Adding New Features

1. **Add API Endpoint:**
   - Create route in `backend/app/api/v1/`
   - Add schema in `backend/app/schemas/`
   - Test with Swagger UI

2. **Add Frontend Page:**
   - Create component in `frontend/src/pages/`
   - Add route in `frontend/src/App.tsx`
   - Create API service in `frontend/src/services/`

3. **Add Database Model:**
   - Add model in `backend/app/models/`
   - Create migration: `alembic revision --autogenerate`
   - Apply: `alembic upgrade head`

---

## 📊 Monitoring & Logs

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs db

# Follow logs
docker-compose logs -f backend
```

### Database Administration

```bash
# Connect to database
docker-compose exec db psql -U sports_user -d sports_analytics

# Or with pgAdmin (add to docker-compose.yml):
# http://localhost:5050
```

---

## 🎯 Next Steps

### Phase 1: Backend ✅ (DONE!)
- [x] FastAPI application
- [x] Database models
- [x] API endpoints
- [x] Analytics integration
- [x] Docker setup

### Phase 2: Frontend 🔄 (IN PROGRESS)
- [ ] React application setup
- [ ] Main pages (Dashboard, Players, Teams)
- [ ] Team Fit Analyzer UI
- [ ] Data visualizations
- [ ] API integration

### Phase 3: Enhancement
- [ ] Authentication (JWT)
- [ ] Real-time updates (WebSocket)
- [ ] Advanced analytics
- [ ] Mobile responsive design
- [ ] Performance optimization

### Phase 4: Deployment
- [ ] Production Docker setup
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Domain and SSL
- [ ] Cloud deployment (AWS/GCP/Azure)

---

## 📚 Documentation

- [Full Stack Architecture](docs/FULL_STACK_ARCHITECTURE.md)
- [Data Coverage Comparison](docs/DATA_COVERAGE_COMPARISON.md)
- [Backend README](backend/README.md)
- [API Documentation](http://localhost:8000/api/docs) (when running)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📝 License

MIT License - feel free to use for your projects!

---

## 🎉 You're Ready!

Your Sports Analytics Platform is now running!

**Access Points:**
- 🌐 API: http://localhost:8000
- 📖 Docs: http://localhost:8000/api/docs
- 🎨 Frontend: http://localhost:3000 (when ready)

**Try it out:**
```bash
# Get all leagues
curl http://localhost:8000/api/v1/leagues | json_pp

# Explore API in browser
open http://localhost:8000/api/docs
```

---

**Questions? Issues?**
- Check [backend/README.md](backend/README.md)
- Visit http://localhost:8000/api/docs
- Open an issue on GitHub

**Happy Analyzing! ⚽🏀📊**
