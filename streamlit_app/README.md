# 🎨 Streamlit Frontend - Sports Analytics Platform

Professional Streamlit-based frontend for the Sports Analytics Platform with Opta-style analytics.

## 🌟 Features

### ✅ Completed Pages:
1. **🏠 Home Dashboard** - Overview and quick start
2. **⚽ Players** - Search, analyze, and view player details
3. **🎯 Team Fit Analyzer** - 7-dimensional compatibility analysis
4. **💰 Moneyball System** - Find undervalued players

### 🎨 UI Components:
- Modern gradient design
- Interactive charts (Plotly)
- Responsive layout
- Real-time API integration
- Progress bars and gauges
- Radar charts for player attributes
- Value scatter plots

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Backend API running at http://localhost:8000

### Installation

```bash
cd streamlit_app
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

## 📁 Project Structure

```
streamlit_app/
├── app.py                      # Main application
├── pages/                      # Multi-page app
│   ├── 2_⚽_Players.py         # Player search and analysis
│   ├── 4_🎯_Team_Fit.py       # Team fit analyzer
│   └── 6_💰_Moneyball.py      # Moneyball system
├── utils/                      # Utilities
│   ├── api_client.py          # Backend API client
│   ├── charts.py              # Plotly charts
│   └── helpers.py             # Helper functions
├── requirements.txt
└── README.md
```

## 🎯 Pages

### 1. Home Dashboard
- Platform overview
- Quick stats
- API status check
- Quick navigation

### 2. Players Page
**Features:**
- 🔍 Advanced search (name, position, Opta Index)
- 📊 Detailed player profiles
- ⚡ Technical attributes visualization
- 📈 Season statistics
- 🎯 Opta Performance Index
- 📊 Radar charts

**Search Filters:**
- Player name
- Position (GK, DEF, MID, FWD, etc.)
- Min Opta Index (0-100)

**Player Details:**
- Opta Performance Index with gauge chart
- Technical attributes (Pace, Shooting, Passing, Dribbling)
- Physical & defensive attributes
- Radar chart visualization
- Season statistics (Goals, Assists, per-90 metrics)
- Performance trend

### 3. Team Fit Analyzer
**7-Dimensional Analysis:**
1. Statistical Fit (25%) - Performance metrics
2. Tactical Fit (20%) - Playing style match
3. Personality Fit (15%) - Team chemistry
4. Chemistry Fit (15%) - Integration potential
5. Cultural Fit (10%) - Language/adaptation
6. Budget Fit (10%) - Value for money
7. Age Fit (5%) - Squad balance

**Features:**
- 🏆 Define your team profile
- ⚙️ Choose playing style (Possession, Counter-attack, High Press)
- 🎯 Set priority position
- 💰 Define budget
- 🔍 Get ranked recommendations
- 📊 View compatibility breakdown

**Output:**
- Overall fit score (0-100)
- Fit rating (EXCELLENT/GOOD/AVERAGE/POOR)
- Recommendation (STRONG_BUY/BUY/MONITOR/PASS)
- Adaptation timeline
- Key strengths and concerns

### 4. Moneyball System
**Find Undervalued Players:**
- Calculate Value Ratio (Performance / Price)
- Identify market inefficiencies
- Find high ROI players

**Features:**
- 🔍 Search undervalued players
- 📊 Value scatter plot visualization
- 💰 Player value analysis
- 🎯 ROI potential assessment
- 💼 Budget optimizer (coming soon)

**Value Analysis:**
- Actual vs Estimated market value
- Valuation status (Undervalued/Fair/Overvalued)
- Performance, Consistency, Potential scores
- Target price recommendations

## 🎨 Design Features

### Color Scheme
- Primary: Purple/Blue gradient (#667eea → #764ba2)
- Success: Green (#22c55e)
- Warning: Yellow (#eab308)
- Error: Red (#ef4444)

### UI Elements
- Gradient header
- Metric cards with gradients
- Feature boxes with colored borders
- Progress bars with color coding
- Gauge charts
- Interactive Plotly charts

## 🔌 API Integration

The app connects to the FastAPI backend at `http://localhost:8000/api/v1`

### Endpoints Used:
```
GET  /leagues                  # List leagues
POST /players/search           # Search players
GET  /players/{id}             # Get player
GET  /players/{id}/stats       # Get stats
GET  /analytics/opta-index/{id}  # Opta Index
POST /team-fit/analyze         # Analyze fit
POST /team-fit/batch           # Batch analysis
GET  /moneyball/undervalued    # Find undervalued
GET  /moneyball/value-analysis/{id}  # Value analysis
```

## 📊 Visualizations

### Charts (Plotly):
1. **Radar Chart** - Player attributes comparison
2. **Bar Chart** - Opta Index breakdown
3. **Horizontal Bar** - Team fit dimensions
4. **Gauge Chart** - Single metric display
5. **Scatter Plot** - Value analysis
6. **Progress Bars** - Attribute ratings

### Custom Components:
- Player cards
- Metric rows
- Fit rating badges
- Recommendation badges
- SWOT analysis display

## 🎯 Usage Examples

### Search Players
1. Navigate to **Players** page
2. Enter search criteria (name, position, min Opta)
3. Click **Search**
4. View results in card format
5. Click **View Details** for full profile

### Team Fit Analysis
1. Navigate to **Team Fit** page
2. Fill team profile in sidebar:
   - Team name
   - Playing style
   - Formation
   - Budget
   - Priority position
3. Click **Find Best Fit Players**
4. View ranked recommendations

### Find Undervalued Players
1. Navigate to **Moneyball** page
2. Select position filter
3. Click **Find Undervalued Players**
4. View value scatter plot
5. Check value ratios and ROI potential

## 🐛 Troubleshooting

### Backend Not Connected
```
❌ API Offline
```

**Solution:**
```bash
# Start backend
docker-compose up -d

# Or manually
cd backend
uvicorn app.main:app --reload
```

### Port Already in Use
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

### Module Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Or specific package
pip install streamlit plotly requests pandas
```

## 🔧 Configuration

### Streamlit Config (Optional)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
```

## 📈 Performance

### Caching
API calls are cached using `@st.cache_data`:
- TTL: 300 seconds (5 minutes) for most calls
- TTL: 600 seconds (10 minutes) for scouting reports

### Optimization Tips
1. Use caching for expensive operations
2. Limit API calls in loops
3. Pagination for large datasets
4. Lazy load heavy visualizations

## 🚀 Deployment

### Local
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Select app.py as entry point
4. Add secrets in dashboard

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🆕 Adding New Pages

Create file in `pages/` folder:

```python
# pages/7_📊_New_Page.py
import streamlit as st

st.title("New Page")
st.write("Content here")
```

Streamlit will automatically detect and add to sidebar!

## 🎨 Custom Styling

Add custom CSS in any page:

```python
st.markdown("""
<style>
    .custom-class {
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)
```

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Backend API Docs](http://localhost:8000/api/docs)

## 🤝 Contributing

1. Add new page in `pages/` folder
2. Add utility function in `utils/`
3. Update README
4. Test with backend running

## 📝 License

MIT License

---

**Built with ❤️ using Streamlit**

For full application documentation, see [STARTUP_GUIDE.md](../STARTUP_GUIDE.md)
