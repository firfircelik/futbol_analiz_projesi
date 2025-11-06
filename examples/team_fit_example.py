"""
Team Fit Analysis Example
Shows how scouts and managers can find perfect players for their team
"""

import sys
sys.path.append('..')

from src.team_fit.team_fit_analyzer import (
    TeamFitAnalyzer, TeamProfile, PlayerProfile,
    PlayingStyle, Personality, find_best_players_for_team
)


def example_team_fit_analysis():
    """Example: Find if a player fits your team."""

    print("="*80)
    print("TEAM FIT ANALYSIS - Find the Perfect Player for Your Team!")
    print("="*80)
    print()

    # Define your team profile
    my_team = TeamProfile(
        team_name="FC Example United",
        league="Premier League",
        playing_style=PlayingStyle.HIGH_PRESS,
        formation="4-3-3",
        average_age=26.5,
        budget_millions=40.0,
        priority_positions=['ST', 'CAM', 'LW'],
        desired_traits=['pace', 'dribbling', 'work_rate'],
        average_player_value=25.0,
        team_personality='ambitious',
        language='english',
        requires_pace=True,
        requires_technique=True,
        requires_experience=False,
    )

    print(f"YOUR TEAM: {my_team.team_name}")
    print(f"  Playing Style: {my_team.playing_style.value}")
    print(f"  Formation: {my_team.formation}")
    print(f"  Budget: €{my_team.budget_millions}M")
    print(f"  Priority Positions: {', '.join(my_team.priority_positions)}")
    print()

    # Target player profile
    target_player = PlayerProfile(
        player_name="Marco Silva",
        age=24,
        position="ST",
        nationality="Brazilian",
        current_team="FC Porto",
        market_value_millions=35.0,
        opta_index=72.5,
        goals=18,
        assists=6,
        matches_played=30,
        pace=88,
        strength=75,
        stamina=82,
        dribbling=85,
        passing=76,
        shooting=84,
        defending=40,
        work_rate=85,
        decision_making=78,
        composure=80,
        leadership=65,
        personality_type=Personality.AMBITIOUS,
        temperament='calm',
        professionalism=88,
        preferred_foot='right',
        languages=['portuguese', 'english', 'spanish'],
        injury_proneness='low',
        contract_expiry_years=1.5,
    )

    print(f"TARGET PLAYER: {target_player.player_name}")
    print(f"  Age: {target_player.age} | Position: {target_player.position}")
    print(f"  Market Value: €{target_player.market_value_millions}M")
    print(f"  Opta Index: {target_player.opta_index}")
    print(f"  This Season: {target_player.goals} goals, {target_player.assists} assists")
    print()
    print("-"*80)
    print()

    # Analyze fit
    analyzer = TeamFitAnalyzer()
    fit_result = analyzer.analyze_fit(target_player, my_team)

    # Display results
    print("FIT ANALYSIS RESULTS")
    print("="*80)
    print()
    print(f"🎯 OVERALL FIT SCORE: {fit_result['overall_fit_score']}/100")
    print(f"📊 FIT RATING: {fit_result['fit_rating']}")
    print()
    print(f"💡 RECOMMENDATION:")
    print(f"   {fit_result['recommendation']}")
    print()
    print(f"⏱️  ADAPTATION TIMELINE: {fit_result['adaptation_timeline']}")
    print(f"🎖️  SIGNING PRIORITY: {fit_result['signing_priority']}")
    print()

    # Detailed breakdown
    print("DETAILED FIT BREAKDOWN:")
    print("-"*80)

    breakdown = fit_result['breakdown']
    for category, data in breakdown.items():
        category_name = category.replace('_', ' ').title()
        score = data['score']
        bar = '█' * int(score/5) + '░' * (20 - int(score/5))
        print(f"{category_name:.<25} [{bar}] {score}/100")

    print()

    # Key strengths
    print("✅ KEY STRENGTHS:")
    for i, strength in enumerate(fit_result['key_strengths'], 1):
        print(f"   {i}. {strength}")
    print()

    # Potential concerns
    if fit_result['potential_concerns']:
        print("⚠️  POTENTIAL CONCERNS:")
        for i, concern in enumerate(fit_result['potential_concerns'], 1):
            print(f"   {i}. {concern}")
        print()

    # Tactical fit details
    print("TACTICAL FIT ANALYSIS:")
    print("-"*80)
    tactical = breakdown['tactical_fit']
    print(f"  Playing Style Match: {'✓ YES' if tactical.get('playing_style_match') else '✗ NO'}")
    print(f"  Analysis: {tactical['analysis']}")
    print()

    # Personality fit details
    print("PERSONALITY FIT ANALYSIS:")
    print("-"*80)
    personality = breakdown['personality_fit']
    print(f"  Personality Match: {'✓ YES' if personality.get('personality_match') else '✗ NO'}")
    print(f"  Type: {target_player.personality_type.value.title()}")
    print(f"  Temperament: {target_player.temperament.title()}")
    print(f"  Professionalism: {target_player.professionalism}/100")
    print()

    # Budget fit details
    print("BUDGET FIT ANALYSIS:")
    print("-"*80)
    budget = breakdown['budget_fit']
    print(f"  Market Value: €{target_player.market_value_millions}M")
    print(f"  Team Budget: €{my_team.budget_millions}M")
    print(f"  Affordable: {'✓ YES' if budget.get('affordable') else '✗ OVER BUDGET'}")
    print(f"  Value Ratio: {budget.get('value_ratio', 0):.2f}")
    print()


def example_multiple_players_comparison():
    """Example: Compare multiple players and find the best fit."""

    print("\n" + "="*80)
    print("MULTIPLE PLAYERS COMPARISON - Find Your Best Transfer Target")
    print("="*80)
    print()

    # Your team
    my_team = TeamProfile(
        team_name="Chelsea FC",
        league="Premier League",
        playing_style=PlayingStyle.POSSESSION_BASED,
        formation="4-2-3-1",
        average_age=25.8,
        budget_millions=60.0,
        priority_positions=['CM', 'CAM'],
        desired_traits=['passing', 'vision', 'creativity'],
        average_player_value=35.0,
        team_personality='professional',
        language='english',
        requires_technique=True,
    )

    # Candidate players
    candidates = [
        PlayerProfile(
            player_name="João Félix",
            age=24,
            position="CAM",
            nationality="Portuguese",
            current_team="Atletico Madrid",
            market_value_millions=45.0,
            opta_index=74.0,
            goals=12, assists=8, matches_played=28,
            pace=82, strength=68, stamina=78,
            dribbling=88, passing=85, shooting=80, defending=45,
            work_rate=75, decision_making=82, composure=79, leadership=60,
            personality_type=Personality.AMBITIOUS,
            temperament='calm',
            professionalism=85,
            languages=['portuguese', 'spanish', 'english'],
        ),
        PlayerProfile(
            player_name="Mason Mount",
            age=25,
            position="CAM",
            nationality="English",
            current_team="Manchester United",
            market_value_millions=40.0,
            opta_index=71.5,
            goals=10, assists=9, matches_played=32,
            pace=78, strength=72, stamina=85,
            dribbling=80, passing=83, shooting=76, defending=60,
            work_rate=88, decision_making=80, composure=77, leadership=75,
            personality_type=Personality.TEAM_PLAYER,
            temperament='calm',
            professionalism=92,
            languages=['english'],
        ),
        PlayerProfile(
            player_name="Khvicha Kvaratskhelia",
            age=23,
            position="LW",
            nationality="Georgian",
            current_team="Napoli",
            market_value_millions=50.0,
            opta_index=76.5,
            goals=15, assists=12, matches_played=30,
            pace=90, strength=70, stamina=82,
            dribbling=90, passing=80, shooting=82, defending=40,
            work_rate=82, decision_making=79, composure=81, leadership=55,
            personality_type=Personality.MAVERICK,
            temperament='aggressive',
            professionalism=80,
            languages=['georgian', 'italian'],
        ),
    ]

    # Find best fits
    best_fits = find_best_players_for_team(candidates, my_team, top_n=3)

    print(f"TEAM: {my_team.team_name}")
    print(f"Looking for: {', '.join(my_team.priority_positions)}")
    print(f"Budget: €{my_team.budget_millions}M")
    print()
    print("="*80)
    print("RANKED TRANSFER TARGETS:")
    print("="*80)
    print()

    print(best_fits.to_string(index=False))
    print()

    # Detailed analysis of top choice
    analyzer = TeamFitAnalyzer()
    top_choice = candidates[0]  # João Félix
    detailed = analyzer.analyze_fit(top_choice, my_team)

    print("="*80)
    print(f"DETAILED ANALYSIS: #{1} - {top_choice.player_name}")
    print("="*80)
    print()
    print(f"Overall Fit: {detailed['overall_fit_score']}/100 - {detailed['fit_rating']}")
    print()
    print("Strengths:")
    for strength in detailed['key_strengths'][:3]:
        print(f"  ✓ {strength}")
    print()
    print(f"💡 {detailed['recommendation']}")


def main():
    """Run all examples."""

    print("\n" + "█"*80)
    print(" "*25 + "TEAM FIT ANALYZER")
    print(" "*20 + "Find Perfect Players for Your Team")
    print("█"*80)
    print()

    # Example 1: Single player analysis
    example_team_fit_analysis()

    input("\n\nPress Enter to see multiple players comparison...")

    # Example 2: Multiple players
    example_multiple_players_comparison()

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print()
    print("This system helps you:")
    print("  ✓ Find statistically compatible players")
    print("  ✓ Assess tactical fit with your playing style")
    print("  ✓ Evaluate personality and team chemistry")
    print("  ✓ Check budget compatibility")
    print("  ✓ Predict adaptation timeline")
    print("  ✓ Make data-driven transfer decisions")
    print()


if __name__ == "__main__":
    main()
