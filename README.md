# 🏆 Multi-Sport Analytics Platform

> **Professional Sports Analysis for Football & Basketball** - Like SofaScore, but with advanced AI-powered analytics!

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Data](https://img.shields.io/badge/APIs-Free-brightgreen)](https://github.com/)

A comprehensive sports analytics platform that provides professional-grade analysis, live scores, detailed statistics, and predictive insights for **10 major football leagues** and **10 major basketball leagues**.

## 🌟 Key Features

### 📊 Real-Time Data Collection
- **Free API Integration** - No API keys required for most features!
- **Live Scores** - Real-time match updates
- **Complete League Coverage** - Fixtures, results, standings, and more
- **Player Statistics** - Comprehensive player performance data
- **Team Analytics** - Detailed team statistics and insights

### ⚽ Football (Soccer) Leagues
1. **English Premier League** (EPL)
2. **La Liga** (Spain)
3. **Serie A** (Italy)
4. **Bundesliga** (Germany)
5. **Ligue 1** (France)
6. **Eredivisie** (Netherlands)
7. **Primeira Liga** (Portugal)
8. **Brasileiro Série A** (Brazil)
9. **Liga Profesional** (Argentina)
10. **MLS** (USA)

### 🏀 Basketball Leagues
1. **NBA** (USA)
2. **EuroLeague**
3. **Liga ACB** (Spain)
4. **Turkish BSL**
5. **Lega Basket Serie A** (Italy)
6. **Basketball Bundesliga** (Germany)
7. **LNB Pro A** (France)
8. **Greek Basket League**
9. **CBA** (China)
10. **NBL** (Australia)

### 📈 Advanced Analytics

#### Football Analytics
- **Expected Goals (xG)** - Shot quality analysis
- **Expected Threat (xT)** - Spatial threat assessment
- **Possession Analysis** - Ball control metrics
- **Pass Networks** - Team passing patterns
- **Shot Charts** - Shot location and accuracy
- **PPDA** - Pressing intensity metrics
- **Progressive Passes** - Forward ball progression

#### Basketball Analytics
- **Player Efficiency Rating (PER)**
- **True Shooting Percentage**
- **Effective Field Goal Percentage**
- **Usage Rate** - Player involvement metrics
- **Offensive/Defensive Ratings**
- **Shot Charts** - NBA-style court visualizations
- **Plus/Minus Analysis**
- **Win Shares**

### 📝 Professional Reports
- **League Overview Reports** - Comprehensive league summaries
- **Team Analysis Reports** - Detailed team performance breakdowns
- **Player Scouting Reports** - Individual player assessments
- **Season Summary Reports** - End-of-season analytics
- **Export Formats**: HTML, JSON, Excel

### 📊 Visualizations
- **Heatmaps** - Spatial analysis
- **Radar Charts** - Multi-dimensional comparisons
- **Shot Charts** - Basketball court and football pitch visualizations
- **Trend Lines** - Performance over time
- **Comparison Charts** - Team and player comparisons
- **Interactive Dashboards** - Professional-grade visualizations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/firfircelik/futbol_analiz_projesi.git
cd futbol_analiz_projesi

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run full analysis (all sports and leagues)
python src/main.py

# Analyze specific sport
python src/main.py --sport basketball
python src/main.py --sport football

# Analyze specific league
python src/main.py --sport basketball --league NBA
python src/main.py --sport football --league EPL

# List all available leagues
python src/main.py --list-leagues

# Show platform configuration
python src/main.py --show-config
```

### Python API

```python
from src.data_collection.free_football_api import FreeFo

otballAPI
from src.data_collection.free_basketball_api import FreeBasketballAPI
from src.analysis.basketball_analysis import BasketballAnalysis
from src.reports.report_generator import SportsReportGenerator

# Football: Get live EPL scores
football_api = FreeFo

otballAPI()
live_scores = football_api.get_live_scores('EPL')
print(live_scores)

# Football: Get league standings
standings = football_api.get_league_standings('EPL', '2023-2024')
print(standings)

# Basketball: Collect NBA data
basketball_api = FreeBasketballAPI()
nba_data = basketball_api.collect_full_nba_data(season=2023)

# Generate reports
report_gen = SportsReportGenerator()
report_gen.generate_league_overview_report('basketball', 'NBA', data)
```

## 📁 Project Structure

```
futbol_analiz_projesi/
├── config/
│   ├── leagues_config.yaml      # League configurations
│   ├── api_config.py            # Free API endpoints
│   └── config_loader.py         # Configuration management
│
├── src/
│   ├── data_collection/
│   │   ├── free_football_api.py      # Free football data APIs
│   │   ├── free_basketball_api.py    # Free basketball data APIs
│   │   ├── statsbomb_data_collection.py
│   │   └── football_data_collection.py
│   │
│   ├── data_preprocessing/
│   │   ├── basketball_preprocessor.py
│   │   └── data_processor.py
│   │
│   ├── analysis/
│   │   ├── basketball_analysis.py    # Basketball analytics
│   │   ├── team_analysis.py
│   │   ├── match_prediction.py
│   │   └── player_trend_analysis.py
│   │
│   ├── visualization/
│   │   ├── basketball_viz.py         # Basketball visualizations
│   │   ├── plot_generator.py
│   │   ├── radar_charts.py
│   │   └── heatmaps.py
│   │
│   ├── reports/
│   │   └── report_generator.py       # Professional report generation
│   │
│   ├── ml_models/
│   │   └── prediction_model.py
│   │
│   └── main.py                       # Main orchestration
│
├── data/
│   ├── raw/                          # Raw collected data
│   ├── processed/                    # Processed data
│   └── visualizations/               # Generated charts
│
├── reports/                          # Generated reports
├── tests/                            # Unit tests
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Free APIs Used (No Keys Required!)

1. **TheSportsDB** - Football & Basketball data
   - Completely free
   - No registration needed
   - Live scores, fixtures, standings, players

2. **BallDontLie** - NBA data
   - Completely free
   - No API key required
   - Teams, players, games, statistics

3. **StatsBomb** - Advanced football analytics
   - Free tier available
   - Event-level data
   - xG and advanced metrics

### Optional: Adding API Keys

For enhanced data access, you can add API keys in `.env`:

```bash
# Optional: API-Football (100 requests/day free tier)
API_FOOTBALL_KEY=your_key_here

# Optional: SportsData.io
SPORTSDATA_API_KEY=your_key_here
```

## 📊 Data Sources & APIs

| Sport      | Source          | Type  | Coverage                    |
|------------|-----------------|-------|-----------------------------|
| Football   | TheSportsDB     | Free  | All major leagues           |
| Football   | StatsBomb       | Free  | Event-level data            |
| Football   | API-Football    | Paid  | Enhanced data (optional)    |
| Basketball | BallDontLie     | Free  | NBA complete data           |
| Basketball | TheSportsDB     | Free  | Global basketball leagues   |
| Basketball | NBA Official    | Free  | Official NBA data feed      |

## 🎯 Use Cases

### For Analysts
- Comprehensive league and team analysis
- Player performance tracking
- Tactical pattern identification
- Data-driven scouting reports

### For Fans
- Live scores and match updates
- Team and player statistics
- Historical data analysis
- Performance predictions

### For Researchers
- Large-scale sports data collection
- Machine learning model development
- Statistical analysis and research
- Predictive modeling

### For Developers
- Clean, well-documented codebase
- Modular architecture
- Easy API integration
- Extensible framework

## 📈 Example Outputs

### League Overview Report
```
NBA 2023-24 Season
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Teams: 30
Total Players: 450+
Games Analyzed: 1,230

Top Teams:
1. Boston Celtics    (64-18, 78.0%)
2. Denver Nuggets    (57-25, 69.5%)
3. Milwaukee Bucks   (49-33, 59.8%)

League Leaders:
🏀 Points: Luka Dončić (33.9 PPG)
🎯 Assists: Tyrese Haliburton (10.9 APG)
🛡️ Rebounds: Domantas Sabonis (13.7 RPG)
```

### Player Scouting Report
```
LeBron James - Scouting Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Team: Los Angeles Lakers
Position: Forward
Season: 2023-24

Scoring: 25.7 PPG (Elite)
Playmaking: 8.3 APG (Elite)
Rebounding: 7.3 RPG (Above Average)
Efficiency: 58.5 TS% (Elite)

Strengths:
✓ Elite court vision and passing
✓ Consistent scoring from all areas
✓ High basketball IQ
✓ Leadership and experience

Advanced Metrics:
• PER: 26.8
• Win Shares: 8.5
• Usage Rate: 29.3%
• Plus/Minus: +5.8
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TheSportsDB** for free sports data API
- **BallDontLie** for free NBA data
- **StatsBomb** for advanced football analytics
- **NBA** for official data feeds

## 📧 Contact

- **GitHub**: [@firfircelik](https://github.com/firfircelik)
- **Project**: [futbol_analiz_projesi](https://github.com/firfircelik/futbol_analiz_projesi)

## 🔮 Roadmap

- [ ] Real-time WebSocket data streaming
- [ ] Mobile app integration
- [ ] Advanced machine learning predictions
- [ ] Player comparison tool
- [ ] Fantasy sports integration
- [ ] Video highlights integration
- [ ] Social media sentiment analysis
- [ ] Betting odds integration

---

**Made with ❤️ for sports analytics enthusiasts**

*Last Updated: January 2025*
