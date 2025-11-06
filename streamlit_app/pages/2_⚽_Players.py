"""
Players Page - Search and Analyze Players
"""

import streamlit as st
import sys
sys.path.append('..')

from utils.api_client import api_client
from utils.charts import create_radar_chart, create_opta_breakdown_chart, create_gauge_chart
from utils.helpers import display_player_card, display_metric_row, create_progress_bar, get_position_icon

st.set_page_config(page_title="Players", page_icon="⚽", layout="wide")

st.title("⚽ Player Analysis")

# Sidebar filters
st.sidebar.header("🔍 Search Filters")

search_query = st.sidebar.text_input("Player Name", placeholder="Search by name...")

position_options = ['All', 'GK', 'DEF', 'MID', 'FWD', 'ST', 'CAM', 'CM', 'CDM', 'LW', 'RW', 'CB', 'LB', 'RB']
position = st.sidebar.selectbox("Position", position_options)

min_opta = st.sidebar.slider("Min Opta Index", 0, 100, 0, 5)

if st.sidebar.button("🔍 Search", use_container_width=True):
    st.session_state['search_triggered'] = True

# Main content
tab1, tab2, tab3 = st.tabs(["🔍 Search Players", "📊 Player Details", "⚖️ Compare Players"])

with tab1:
    st.header("Search Players")

    # Search players
    if st.session_state.get('search_triggered') or search_query:
        with st.spinner("Searching players..."):
            players = api_client.search_players(
                query=search_query if search_query else None,
                position=position if position != 'All' else None,
                min_opta_index=min_opta if min_opta > 0 else None,
                page_size=50
            )

        if players:
            st.success(f"✅ Found {len(players)} players")

            # Display as cards
            for i in range(0, len(players), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(players):
                        player = players[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                st.subheader(f"{get_position_icon(player.get('position', ''))} {player.get('name', 'Unknown')}")
                                st.caption(f"{player.get('position', 'N/A')} | Age: {player.get('age', 'N/A')}")

                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Opta Index", f"{player.get('opta_index', 0):.1f}")
                                with col2:
                                    st.metric("Goals", player.get('goals', 0))

                                if st.button(f"View Details", key=f"view_{player.get('player_id')}", use_container_width=True):
                                    st.session_state['selected_player_id'] = player.get('player_id')
                                    st.switch_page("pages/2_⚽_Players.py")
        else:
            st.info("No players found. Try different search criteria.")

with tab2:
    st.header("Player Details")

    if 'selected_player_id' in st.session_state:
        player_id = st.session_state['selected_player_id']

        with st.spinner("Loading player data..."):
            player = api_client.get_player(player_id)
            stats = api_client.get_player_stats(player_id)
            opta_data = api_client.get_opta_index(player_id)

        if player:
            # Player Card
            display_player_card(player)

            st.markdown("---")

            # Opta Index
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("Opta Performance Index")
                opta_index = player.get('opta_index', 0)
                st.plotly_chart(
                    create_gauge_chart(opta_index, "Opta Index"),
                    use_container_width=True
                )

                # Rating
                if opta_index >= 85:
                    st.success("🌟 WORLD CLASS")
                elif opta_index >= 75:
                    st.success("✅ EXCELLENT")
                elif opta_index >= 65:
                    st.info("👍 GOOD")
                elif opta_index >= 50:
                    st.warning("⚠️ AVERAGE")
                else:
                    st.error("❌ BELOW AVERAGE")

            with col2:
                if opta_data and 'breakdown' in opta_data:
                    st.plotly_chart(
                        create_opta_breakdown_chart(opta_data['breakdown']),
                        use_container_width=True
                    )

            st.markdown("---")

            # Attributes
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("⚡ Technical Attributes")
                create_progress_bar(player.get('pace', 0), label="Pace")
                create_progress_bar(player.get('shooting', 0), label="Shooting")
                create_progress_bar(player.get('passing', 0), label="Passing")
                create_progress_bar(player.get('dribbling', 0), label="Dribbling")

            with col2:
                st.subheader("💪 Physical & Defensive")
                create_progress_bar(player.get('physical', 0), label="Physical")
                create_progress_bar(player.get('defending', 0), label="Defending")
                create_progress_bar(player.get('decision_making', 70), label="Decision Making")
                create_progress_bar(player.get('composure', 70), label="Composure")

            # Radar Chart
            st.subheader("📊 Attributes Radar")
            st.plotly_chart(
                create_radar_chart(player),
                use_container_width=True
            )

            # Statistics
            if stats:
                st.subheader("📈 Season Statistics")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Matches", stats.get('matches_played', 0))
                with col2:
                    st.metric("Goals", stats.get('goals', 0))
                with col3:
                    st.metric("Assists", stats.get('assists', 0))
                with col4:
                    st.metric("Goals/90", f"{stats.get('goals_per_90', 0):.2f}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Shots/90", f"{stats.get('shots_per_90', 0):.2f}")
                with col2:
                    st.metric("Key Passes/90", f"{stats.get('key_passes_per_90', 0):.2f}")
                with col3:
                    trend = stats.get('trend', 'stable')
                    emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
                    st.metric("Form", f"{emoji} {trend.capitalize()}")
        else:
            st.error("Player not found")
    else:
        st.info("👆 Select a player from the search tab to view details")

with tab3:
    st.header("Compare Players")

    st.info("🔜 Player comparison feature coming soon! Use the API endpoint for now.")

    st.code("""
# Compare players via API
curl -X POST http://localhost:8000/api/v1/players/compare \\
  -H "Content-Type: application/json" \\
  -d '{"player_ids": ["player1", "player2", "player3"]}'
    """)
