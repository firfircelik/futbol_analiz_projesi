# ScoutAI Backend

Professional FastAPI backend for sports analytics SaaS platform.

## Architecture

```
backend/
├── main.py              # FastAPI application entry point
├── config/              # Configuration and pricing tiers
├── src/                 # Core analytics modules
│   ├── data_collection/ # Multi-source data aggregation
│   ├── opta_analytics/  # Performance index & metrics
│   ├── team_fit/        # Team fit analysis engine
│   ├── moneyball/       # Player valuation system
│   └── db/              # Database schemas
├── static/              # Static assets
└── requirements.txt     # Python dependencies
```

## Features

- **Multi-tier Subscription System**: Free, Scout €29, Professional €99, Club €299
- **Usage Quotas & Enforcement**: Per-plan limits on reports, analyses, API calls
- **JWT Authentication**: Secure token-based auth
- **Stripe Integration**: Payment webhooks and subscription management
- **Advanced Analytics**: Opta Index, xG, Team Fit Analysis, Moneyball Valuation

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run development server
python main.py
```

Server runs on http://localhost:8000

## API Endpoints

### Public
- `GET /` - Health check
- `GET /api/v1/pricing` - Get all pricing plans
- `GET /api/v1/stats` - Public API statistics

### Authenticated
- `GET /api/v1/me` - Current user info and quotas
- `GET /api/v1/players/search` - Search players
- `GET /api/v1/players/{player_id}` - Player profile
- `POST /api/v1/team-fit/analyze` - Team fit analysis
- `POST /api/v1/moneyball/valuations` - Player valuation

### Webhooks
- `POST /api/webhooks/stripe` - Stripe subscription events

## Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn with auto-reload
- **Database**: PostgreSQL (production) / SQLite (development)
- **Cache**: Redis
- **Payments**: Stripe
- **Auth**: JWT with python-jose

## Environment Variables

```bash
DATABASE_URL=sqlite:///./scoutai.db
SECRET_KEY=your-secret-key
STRIPE_API_KEY=sk_test_...
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
```

See `.env.example` for complete configuration.

## Development

```bash
# Run with auto-reload
python main.py

# Run tests
pytest

# Format code
black .
```

## Production Deployment

Use Docker:

```bash
docker build -t scoutai-backend .
docker run -p 8000:8000 scoutai-backend
```

Or see `/DEPLOYMENT.md` for complete production setup.
