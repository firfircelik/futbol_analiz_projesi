"""
Helper Functions and Utilities
"""

import streamlit as st
from typing import Dict, Any


def format_currency(value: float, currency: str = "€") -> str:
    """Format currency value"""
    if value >= 1000:
        return f"{currency}{value/1000:.1f}B"
    elif value >= 1:
        return f"{currency}{value:.1f}M"
    else:
        return f"{currency}{value*1000:.0f}K"


def get_rating_color(rating: float) -> str:
    """Get color based on rating"""
    if rating >= 85:
        return "#22c55e"  # Green
    elif rating >= 70:
        return "#eab308"  # Yellow
    elif rating >= 50:
        return "#f97316"  # Orange
    else:
        return "#ef4444"  # Red


def get_rating_emoji(rating: float) -> str:
    """Get emoji based on rating"""
    if rating >= 85:
        return "🌟"
    elif rating >= 70:
        return "✅"
    elif rating >= 50:
        return "⚠️"
    else:
        return "❌"


def display_player_card(player: Dict):
    """Display player card with key info"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image("https://img.icons8.com/fluency/96/000000/user-male-circle.png", width=80)

    with col2:
        st.subheader(player.get('name', 'Unknown Player'))
        st.caption(f"{player.get('position', 'N/A')} | Age: {player.get('age', 'N/A')}")
        st.caption(f"Team: {player.get('team', 'N/A')}")

    with col3:
        opta = player.get('opta_index', 0)
        color = get_rating_color(opta)
        emoji = get_rating_emoji(opta)
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            <h2>{emoji} {opta:.1f}</h2>
            <p style="margin: 0;">Opta Index</p>
        </div>
        """, unsafe_allow_html=True)


def display_metric_row(metrics: Dict):
    """Display row of metrics"""
    cols = st.columns(len(metrics))

    for idx, (label, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(label, value)


def get_position_icon(position: str) -> str:
    """Get icon for position"""
    position_icons = {
        'GK': '🧤',
        'DEF': '🛡️',
        'CB': '🛡️',
        'LB': '⬅️',
        'RB': '➡️',
        'MID': '⚙️',
        'CM': '⚙️',
        'CAM': '🎯',
        'CDM': '🛡️',
        'FWD': '⚔️',
        'ST': '⚔️',
        'LW': '⬅️⚔️',
        'RW': '➡️⚔️',
        # Basketball
        'G': '🏀',
        'F': '🏀',
        'C': '🏀',
        'PG': '🎯',
        'SG': '🎯',
        'SF': '⚔️',
        'PF': '⚔️',
    }
    return position_icons.get(position, '⚽')


def format_recommendation(recommendation: str) -> str:
    """Format recommendation with color"""
    colors = {
        'STRONG_BUY': ('#22c55e', '🟢'),
        'BUY': ('#eab308', '🟡'),
        'MONITOR': ('#f97316', '🟠'),
        'PASS': ('#ef4444', '🔴')
    }

    color, emoji = colors.get(recommendation, ('#666', '⚪'))

    return f"""
    <div style="background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 5px;
                display: inline-block; font-weight: bold;">
        {emoji} {recommendation}
    </div>
    """


def display_fit_rating(fit_rating: str, fit_score: float):
    """Display fit rating badge"""
    colors = {
        'EXCELLENT_FIT': '#22c55e',
        'GOOD_FIT': '#eab308',
        'AVERAGE_FIT': '#f97316',
        'POOR_FIT': '#ef4444'
    }

    color = colors.get(fit_rating, '#666')

    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 1rem; border-radius: 10px;
                text-align: center; margin: 1rem 0;">
        <h2>{fit_score:.1f}/100</h2>
        <h4>{fit_rating.replace('_', ' ')}</h4>
    </div>
    """, unsafe_allow_html=True)


def create_progress_bar(value: float, max_value: float = 100, label: str = ""):
    """Create custom progress bar"""
    percentage = (value / max_value) * 100
    color = get_rating_color(value)

    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
            <span>{label}</span>
            <span><strong>{value:.1f}</strong></span>
        </div>
        <div style="background: #e5e7eb; border-radius: 10px; height: 20px; overflow: hidden;">
            <div style="background: {color}; width: {percentage}%; height: 100%;
                        border-radius: 10px; transition: width 0.3s ease;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_swot_analysis(swot: Dict):
    """Display SWOT analysis"""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: rgba(34, 197, 94, 0.1); padding: 1rem; border-radius: 10px;
                    border-left: 4px solid #22c55e; margin-bottom: 1rem;">
            <h4>💪 Strengths</h4>
        """, unsafe_allow_html=True)
        for strength in swot.get('strengths', []):
            st.markdown(f"- {strength}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(234, 179, 8, 0.1); padding: 1rem; border-radius: 10px;
                    border-left: 4px solid #eab308;">
            <h4>🎯 Opportunities</h4>
        """, unsafe_allow_html=True)
        for opp in swot.get('opportunities', []):
            st.markdown(f"- {opp}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 10px;
                    border-left: 4px solid #ef4444; margin-bottom: 1rem;">
            <h4>⚠️ Weaknesses</h4>
        """, unsafe_allow_html=True)
        for weakness in swot.get('weaknesses', []):
            st.markdown(f"- {weakness}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(249, 115, 22, 0.1); padding: 1rem; border-radius: 10px;
                    border-left: 4px solid #f97316;">
            <h4>⛔ Threats</h4>
        """, unsafe_allow_html=True)
        for threat in swot.get('threats', []):
            st.markdown(f"- {threat}")
        st.markdown("</div>", unsafe_allow_html=True)


def show_api_error():
    """Show API connection error"""
    st.error("""
    ❌ **Cannot connect to backend API**

    Please make sure the backend is running:
    ```bash
    docker-compose up -d
    ```

    Or start manually:
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```

    Backend should be running at: http://localhost:8000
    """)


def show_no_data():
    """Show no data message"""
    st.info("""
    📊 **No data available**

    The database might be empty. Please populate it with sample data:
    ```python
    python scripts/populate_db.py
    ```

    Or load real data:
    ```python
    python scripts/load_real_data.py
    ```
    """)
