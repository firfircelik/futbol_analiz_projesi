"""
Team Fit Analyzer Page
"""

import streamlit as st
import sys
sys.path.append('..')

from utils.api_client import api_client
from utils.charts import create_team_fit_chart
from utils.helpers import display_fit_rating, format_recommendation, create_progress_bar, get_position_icon

st.set_page_config(page_title="Team Fit Analyzer", page_icon="🎯", layout="wide")

st.title("🎯 Team Fit Analyzer")
st.markdown("**Find the perfect player for your team with 7-dimensional compatibility analysis**")

# Sidebar - Team Profile
st.sidebar.header("🏆 Your Team Profile")

team_name = st.sidebar.text_input("Team Name", "My Team")

playing_style = st.sidebar.selectbox(
    "Playing Style",
    ["POSSESSION_BASED", "COUNTER_ATTACK", "HIGH_PRESS", "BALANCED", "DEFENSIVE"]
)

formation = st.sidebar.text_input("Formation", "4-3-3")

budget = st.sidebar.number_input("Budget (€M)", min_value=1, max_value=500, value=50)

priority_position = st.sidebar.selectbox(
    "Priority Position",
    ['ST', 'CAM', 'CM', 'CDM', 'LW', 'RW', 'LB', 'RB', 'CB', 'GK']
)

requires_pace = st.sidebar.checkbox("Requires Pace", value=True)
requires_technique = st.sidebar.checkbox("Requires Technique", value=True)

# Main content
tab1, tab2 = st.tabs(["🔍 Find Players", "📊 Analyze Specific Player"])

with tab1:
    st.header("Find Best Fit Players")

    st.info(f"""
    **Team Profile:**
    - 🏆 Team: {team_name}
    - ⚙️ Style: {playing_style}
    - 📐 Formation: {formation}
    - 💰 Budget: €{budget}M
    - 🎯 Position: {priority_position}
    """)

    top_n = st.slider("Number of recommendations", 5, 50, 10)

    if st.button("🎯 Find Best Fit Players", use_container_width=True, type="primary"):
        with st.spinner("Analyzing players..."):
            # Build team profile
            team_profile = {
                "team_name": team_name,
                "playing_style": playing_style,
                "formation": formation,
                "budget_millions": float(budget),
                "priority_positions": [priority_position],
                "desired_traits": [],
                "requires_pace": requires_pace,
                "requires_technique": requires_technique
            }

            if requires_pace:
                team_profile["desired_traits"].append("pace")
            if requires_technique:
                team_profile["desired_traits"].append("technique")

            # Call API
            result = api_client.batch_team_fit(priority_position, team_profile, top_n)

        if result and 'top_matches' in result:
            matches = result['top_matches']
            st.success(f"✅ Found {len(matches)} compatible players")

            # Display results
            for idx, player in enumerate(matches, 1):
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])

                    with col1:
                        st.markdown(f"### #{idx}")
                        st.metric("Fit Score", f"{player.get('fit_score', 0):.1f}/100")

                    with col2:
                        st.subheader(f"{get_position_icon(player.get('position', ''))} {player.get('player_name', 'Unknown')}")
                        st.caption(f"{player.get('position', 'N/A')} | Age: {player.get('age', 'N/A')}")
                        st.caption(f"Opta Index: {player.get('opta_index', 0):.1f}")

                    with col3:
                        fit_rating = player.get('fit_rating', 'AVERAGE_FIT')
                        if fit_rating == 'EXCELLENT_FIT':
                            st.success(f"✅ {fit_rating}")
                        elif fit_rating == 'GOOD_FIT':
                            st.info(f"👍 {fit_rating}")
                        else:
                            st.warning(f"⚠️ {fit_rating}")

                    with col4:
                        recommendation = player.get('recommendation', 'MONITOR')
                        st.markdown(format_recommendation(recommendation), unsafe_allow_html=True)
        else:
            st.error("No players found. Please try different criteria.")

with tab2:
    st.header("Analyze Specific Player")

    player_id_input = st.text_input("Enter Player ID", placeholder="e.g., haaland_1")

    if st.button("Analyze Player Fit", use_container_width=True) and player_id_input:
        with st.spinner("Analyzing player..."):
            team_profile = {
                "team_name": team_name,
                "playing_style": playing_style,
                "formation": formation,
                "budget_millions": float(budget),
                "priority_positions": [priority_position],
                "desired_traits": [],
                "requires_pace": requires_pace,
                "requires_technique": requires_technique
            }

            fit_result = api_client.analyze_team_fit(player_id_input, team_profile)

        if fit_result and 'overall_fit_score' in fit_result:
            st.success("✅ Analysis Complete!")

            # Overall Fit
            col1, col2 = st.columns([1, 2])

            with col1:
                display_fit_rating(
                    fit_result.get('fit_rating', 'AVERAGE_FIT'),
                    fit_result.get('overall_fit_score', 0)
                )

                st.markdown(format_recommendation(fit_result.get('recommendation', 'MONITOR')), unsafe_allow_html=True)

                st.info(f"**Adaptation:** {fit_result.get('adaptation_timeline', 'MEDIUM')}")

            with col2:
                st.plotly_chart(
                    create_team_fit_chart(fit_result),
                    use_container_width=True
                )

            st.markdown("---")

            # Detailed Scores
            st.subheader("📊 Dimensional Breakdown")

            col1, col2 = st.columns(2)

            with col1:
                create_progress_bar(fit_result.get('statistical_fit', 0), label="Statistical Fit (25%)")
                create_progress_bar(fit_result.get('tactical_fit', 0), label="Tactical Fit (20%)")
                create_progress_bar(fit_result.get('personality_fit', 0), label="Personality Fit (15%)")
                create_progress_bar(fit_result.get('chemistry_fit', 0), label="Chemistry Fit (15%)")

            with col2:
                create_progress_bar(fit_result.get('cultural_fit', 0), label="Cultural Fit (10%)")
                create_progress_bar(fit_result.get('budget_fit', 0), label="Budget Fit (10%)")
                create_progress_bar(fit_result.get('age_fit', 0), label="Age Fit (5%)")

            # Key Points
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💪 Key Strengths")
                for strength in fit_result.get('key_strengths', []):
                    st.success(f"✅ {strength}")

            with col2:
                st.subheader("⚠️ Key Concerns")
                for concern in fit_result.get('key_concerns', []):
                    st.warning(f"⚠️ {concern}")
        else:
            st.error("Player not found or analysis failed")

# Info Section
with st.expander("ℹ️ How Team Fit Analysis Works"):
    st.markdown("""
    ### 7-Dimensional Compatibility Analysis

    **1. Statistical Fit (25%)**
    - Player's performance metrics match team's needs
    - Opta Index alignment with required level
    - Position-specific statistics

    **2. Tactical Fit (20%)**
    - Playing style compatibility
    - Formation suitability
    - Technical requirements match

    **3. Personality Fit (15%)**
    - Team chemistry potential
    - Leadership qualities
    - Professionalism level

    **4. Chemistry Fit (15%)**
    - Dressing room integration
    - Nationality/language compatibility
    - Cultural adaptation

    **5. Cultural Fit (10%)**
    - League experience
    - Language skills
    - Adaptation potential

    **6. Budget Fit (10%)**
    - Market value vs budget
    - Value for money
    - Wage structure

    **7. Age Fit (5%)**
    - Squad age balance
    - Development potential
    - Experience level

    ### Recommendations

    - **🟢 STRONG BUY**: Excellent fit, immediate signing recommended
    - **🟡 BUY**: Good fit, consider signing
    - **🟠 MONITOR**: Average fit, keep watching
    - **🔴 PASS**: Poor fit, not recommended
    """)
