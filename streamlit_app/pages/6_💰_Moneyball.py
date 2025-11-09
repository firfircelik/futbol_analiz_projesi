"""
Moneyball System - Find Undervalued Players
"""

import streamlit as st
import sys
sys.path.append('..')

from utils.api_client import api_client
from utils.charts import create_value_scatter, create_gauge_chart
from utils.helpers import format_currency, get_rating_color, get_position_icon

st.set_page_config(page_title="Moneyball", page_icon="💰", layout="wide")

st.title("💰 Moneyball System")
st.markdown("**Find undervalued players and optimize your transfer budget**")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Find Undervalued", "📊 Value Analysis", "💼 Budget Optimizer"])

with tab1:
    st.header("Find Undervalued Players")

    st.info("""
    The Moneyball system identifies players who perform above their market value.
    We calculate a **Value Ratio** = Performance / Price to find the best deals.
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        position_filter = st.selectbox(
            "Position",
            ["All", "GK", "DEF", "MID", "FWD", "ST", "CAM", "CM", "LW", "RW"]
        )

    with col2:
        limit = st.number_input("Number of results", min_value=5, max_value=100, value=20)

    with col3:
        st.metric("", "")  # Spacer

    if st.button("🔍 Find Undervalued Players", use_container_width=True, type="primary"):
        with st.spinner("Analyzing market..."):
            result = api_client.get_undervalued_players(
                position=position_filter if position_filter != "All" else None,
                limit=limit
            )

        if result and 'players' in result:
            players = result['players']
            st.success(f"✅ Found {len(players)} undervalued players")

            # Value scatter plot
            if len(players) > 0:
                st.plotly_chart(
                    create_value_scatter(players),
                    use_container_width=True
                )

            # Display players
            for idx, player in enumerate(players, 1):
                with st.container(border=True):
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])

                    with col1:
                        st.markdown(f"### #{idx}")

                    with col2:
                        st.subheader(f"{get_position_icon(player.get('position', ''))} {player.get('name', 'Unknown')}")
                        st.caption(f"{player.get('position', 'N/A')} | Age: {player.get('age', 'N/A')}")
                        st.caption(f"Team: {player.get('team', 'N/A')}")

                    with col3:
                        st.metric("Opta Index", f"{player.get('opta_index', 0):.1f}")
                        status = player.get('valuation_status', 'undervalued')
                        if status == 'undervalued':
                            st.success("🟢 UNDERVALUED")
                        else:
                            st.info(status.upper())

                    with col4:
                        value = player.get('market_value_millions', 0)
                        st.metric("Market Value", format_currency(value))
                        ratio = player.get('value_ratio', 0)
                        st.metric("Value Ratio", f"{ratio:.2f}")

                    with col5:
                        roi = player.get('roi_potential', 'medium')
                        if roi == 'high':
                            st.success("🎯 HIGH ROI")
                        elif roi == 'medium':
                            st.info("📊 MEDIUM ROI")
                        else:
                            st.warning("⚠️ LOW ROI")

        else:
            st.error("No undervalued players found")

with tab2:
    st.header("Player Value Analysis")

    player_id = st.text_input("Enter Player ID", placeholder="e.g., player_123")

    if st.button("Analyze Value", use_container_width=True) and player_id:
        with st.spinner("Analyzing..."):
            analysis = api_client.get_value_analysis(player_id)

        if analysis and 'player_name' in analysis:
            st.success("✅ Analysis Complete!")

            # Header
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Player", analysis.get('player_name', 'Unknown'))
                st.metric("Position", analysis.get('position', 'N/A'))

            with col2:
                actual_value = analysis.get('actual_market_value', 0)
                estimated_value = analysis.get('estimated_market_value', 0)
                st.metric("Market Value", format_currency(actual_value))
                st.metric("Est. Fair Value", format_currency(estimated_value))

            with col3:
                ratio = analysis.get('value_ratio', 0)
                st.plotly_chart(
                    create_gauge_chart(ratio * 10, "Value Ratio", max_value=20),
                    use_container_width=True
                )

            st.markdown("---")

            # Valuation Status
            col1, col2 = st.columns(2)

            with col1:
                status = analysis.get('valuation_status', 'fair_value')
                if status == 'undervalued':
                    st.success("🟢 **UNDERVALUED** - Great buying opportunity!")
                elif status == 'fair_value':
                    st.info("🟡 **FAIR VALUE** - Priced correctly")
                else:
                    st.error("🔴 **OVERVALUED** - May be too expensive")

                st.metric("ROI Potential", analysis.get('roi_potential', 'medium').upper())

            with col2:
                st.subheader("Recommendation")
                recommendation = analysis.get('recommendation', 'Monitor')
                st.markdown(f"""
                <div style="background: {get_rating_color(ratio * 10)}; color: white;
                            padding: 1rem; border-radius: 10px; text-align: center;">
                    <h3>{recommendation}</h3>
                </div>
                """, unsafe_allow_html=True)

                target = analysis.get('target_price', 0)
                st.metric("Target Price", format_currency(target))

            # Scores
            st.markdown("---")
            st.subheader("📊 Performance Metrics")

            col1, col2, col3 = st.columns(3)

            with col1:
                perf = analysis.get('performance_score', 0)
                st.plotly_chart(
                    create_gauge_chart(perf, "Performance"),
                    use_container_width=True
                )

            with col2:
                cons = analysis.get('consistency_score', 0)
                st.plotly_chart(
                    create_gauge_chart(cons, "Consistency"),
                    use_container_width=True
                )

            with col3:
                pot = analysis.get('potential_score', 0)
                st.plotly_chart(
                    create_gauge_chart(pot, "Potential"),
                    use_container_width=True
                )

            # Reasoning
            st.subheader("💡 Analysis")
            st.info(analysis.get('reasoning', 'No analysis available'))

        else:
            st.error("Player not found or analysis failed")

with tab3:
    st.header("Budget Optimizer")

    st.info("Build the best possible squad within your budget")

    budget = st.number_input("Total Budget (€M)", min_value=10, max_value=1000, value=100)

    st.subheader("Positions Needed")
    positions = []

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.checkbox("Striker (ST)"):
            positions.append("ST")
        if st.checkbox("Winger (LW/RW)"):
            positions.extend(["LW", "RW"])
        if st.checkbox("CAM"):
            positions.append("CAM")

    with col2:
        if st.checkbox("Midfielder (CM)"):
            positions.append("CM")
        if st.checkbox("CDM"):
            positions.append("CDM")
        if st.checkbox("Full Back (LB/RB)"):
            positions.extend(["LB", "RB"])

    with col3:
        if st.checkbox("Center Back (CB)"):
            positions.append("CB")
        if st.checkbox("Goalkeeper (GK)"):
            positions.append("GK")

    if st.button("🎯 Optimize Squad", use_container_width=True, type="primary") and positions:
        st.info("🔜 Budget optimizer feature coming soon!")

        st.markdown("""
        The budget optimizer will:
        - Find the best value players for each position
        - Maximize overall squad quality within budget
        - Balance spending across positions
        - Prioritize high ROI players
        """)

        st.code(f"""
# API Call Example
curl -X POST http://localhost:8000/api/v1/moneyball/budget-optimizer \\
  -H "Content-Type: application/json" \\
  -d '{{"budget": {budget}, "positions_needed": {positions}}}'
        """)

# Info Section
with st.expander("ℹ️ How Moneyball Works"):
    st.markdown("""
    ### Value Ratio Calculation

    **Value Ratio = Performance / Market Price**

    Where:
    - **Performance** = Opta Performance Index (0-100)
    - **Market Price** = Transfer market value in millions

    ### Interpretation

    - **Ratio > 6.0**: 🟢 **Undervalued** - Excellent buying opportunity
    - **Ratio 4.0-6.0**: 🟡 **Fair Value** - Priced correctly
    - **Ratio < 4.0**: 🔴 **Overvalued** - May be too expensive

    ### ROI Potential

    - **High ROI**: Value ratio > 8.0, young age, high potential
    - **Medium ROI**: Value ratio 5.0-8.0, good performance
    - **Low ROI**: Value ratio < 5.0, declining or overpriced

    ### Example

    **Player A:**
    - Opta Index: 80
    - Market Value: €10M
    - Value Ratio: 80 / 10 = **8.0** → 🟢 **Undervalued**

    **Player B:**
    - Opta Index: 75
    - Market Value: €50M
    - Value Ratio: 75 / 50 = **1.5** → 🔴 **Overvalued**
    """)
