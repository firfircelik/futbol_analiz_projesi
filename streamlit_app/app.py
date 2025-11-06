"""
Sports Analytics Platform - Streamlit Frontend
Main Application Entry Point
"""

import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sports Analytics Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/firfircelik/futbol_analiz_projesi',
        'Report a bug': 'https://github.com/firfircelik/futbol_analiz_projesi/issues',
        'About': '# Sports Analytics Platform\nOpta-style professional analytics for Football & Basketball'
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }

    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_BASE_URL = "http://localhost:8000/api/v1"

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/football2.png", width=80)
    st.title("⚽ Sports Analytics")
    st.markdown("---")

    # Navigation Info
    st.info("👈 Use the pages in the sidebar to navigate")

    # API Status Check
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

    st.markdown("---")

    # Quick Stats
    st.subheader("📊 Quick Stats")
    try:
        leagues_response = requests.get(f"{API_BASE_URL}/leagues", timeout=2)
        if leagues_response.status_code == 200:
            leagues = leagues_response.json()
            st.metric("Leagues", len(leagues))
        else:
            st.metric("Leagues", "85+")
    except:
        st.metric("Leagues", "85+")

    st.metric("Data Coverage", "60-80%")
    st.metric("vs Opta Cost", "€0 vs €50k+")

    st.markdown("---")
    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main Content
st.markdown('<h1 class="main-header">⚽ Sports Analytics Platform 🏀</h1>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
    Professional Opta-Style Analytics for Football & Basketball | 85+ Leagues Worldwide
</div>
""", unsafe_allow_html=True)

# Hero Section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h2>📊</h2>
        <h3>Opta Index</h3>
        <p>Professional 0-100 player ratings</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h2>🎯</h2>
        <h3>Team Fit</h3>
        <p>7-dimensional compatibility analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h2>💰</h2>
        <h3>Moneyball</h3>
        <p>Find undervalued players</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features Section
st.header("🌟 Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>⚽ Football Analytics</h3>
        <ul>
            <li>55 leagues worldwide</li>
            <li>Expected Goals (xG)</li>
            <li>Pass networks & shot charts</li>
            <li>Position-specific metrics</li>
            <li>Progressive passes & pressures</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
        <h3>🎯 Team Fit Analyzer</h3>
        <ul>
            <li>Statistical Fit (25%)</li>
            <li>Tactical Fit (20%)</li>
            <li>Personality & Chemistry (30%)</li>
            <li>Budget & Age Fit (15%)</li>
            <li>Recommendations: BUY/MONITOR/PASS</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🏀 Basketball Analytics</h3>
        <ul>
            <li>35 leagues worldwide</li>
            <li>100% NBA coverage (450+ players)</li>
            <li>PER, TS%, eFG%</li>
            <li>Shot charts & efficiency</li>
            <li>Plus/minus & win shares</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-box">
        <h3>💰 Moneyball System</h3>
        <ul>
            <li>Find undervalued players</li>
            <li>Value ratio calculations</li>
            <li>Budget optimization</li>
            <li>ROI predictions</li>
            <li>Market inefficiencies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Data Coverage Section
st.header("📊 Data Coverage vs Opta")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Data Coverage",
        value="60-80%",
        delta="vs Opta 100%",
        help="We collect 60-80% of Opta's raw data from free sources"
    )

with col2:
    st.metric(
        label="NBA Coverage",
        value="95-100%",
        delta="Complete",
        delta_color="normal",
        help="Full NBA data via BallDontLie API"
    )

with col3:
    st.metric(
        label="Annual Cost",
        value="€0",
        delta="vs Opta €50k+",
        delta_color="normal",
        help="100% free APIs"
    )

with col4:
    st.metric(
        label="Leagues",
        value="85+",
        delta="vs Opta ~50",
        delta_color="normal",
        help="55 football + 35 basketball leagues"
    )

# Quick Start Guide
st.header("🚀 Quick Start")

tab1, tab2, tab3 = st.tabs(["🔍 Explore Players", "🎯 Team Fit Analysis", "💰 Find Value"])

with tab1:
    st.markdown("""
    ### Explore Players
    1. Navigate to **⚽ Players** page from sidebar
    2. Search by name, position, or league
    3. View comprehensive statistics
    4. Get Opta Performance Index
    5. Compare multiple players
    """)

    if st.button("Go to Players Page →", key="players_btn"):
        st.switch_page("pages/2_⚽_Players.py")

with tab2:
    st.markdown("""
    ### Team Fit Analysis
    1. Navigate to **🎯 Team Fit** page
    2. Select your team's profile
    3. Choose target position
    4. Get ranked recommendations
    5. View compatibility breakdown
    """)

    if st.button("Go to Team Fit →", key="teamfit_btn"):
        st.switch_page("pages/4_🎯_Team_Fit.py")

with tab3:
    st.markdown("""
    ### Find Undervalued Players
    1. Navigate to **💰 Moneyball** page
    2. Set your budget and criteria
    3. View undervalued players
    4. Analyze value ratios
    5. Optimize your squad spending
    """)

    if st.button("Go to Moneyball →", key="moneyball_btn"):
        st.switch_page("pages/6_💰_Moneyball.py")

# API Status
st.header("🔌 API Status")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Backend API")
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend is running at http://localhost:8000")
            st.info("📖 API Docs: http://localhost:8000/api/docs")
        else:
            st.error("❌ Backend returned error")
    except:
        st.error("❌ Backend is not running")
        st.warning("Start backend with: `docker-compose up -d`")

with col2:
    st.subheader("Available Endpoints")
    st.code("""
    ✅ /api/v1/leagues
    ✅ /api/v1/players
    ✅ /api/v1/teams
    ✅ /api/v1/analytics
    ✅ /api/v1/team-fit
    ✅ /api/v1/scouting
    ✅ /api/v1/moneyball
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔗 Links**")
    st.markdown("[GitHub](https://github.com/firfircelik/futbol_analiz_projesi)")
    st.markdown("[API Docs](http://localhost:8000/api/docs)")

with col2:
    st.markdown("**📚 Documentation**")
    st.markdown("[Startup Guide](../STARTUP_GUIDE.md)")
    st.markdown("[Architecture](../docs/FULL_STACK_ARCHITECTURE.md)")

with col3:
    st.markdown("**⚡ Quick Actions**")
    if st.button("🔄 Refresh Stats"):
        st.rerun()

st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    Built with ❤️ for sports analytics professionals | Powered by FastAPI + Streamlit
</div>
""", unsafe_allow_html=True)
