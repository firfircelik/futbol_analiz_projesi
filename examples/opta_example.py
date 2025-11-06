"""
Example Usage of Opta-Style Professional Analytics
For Scouts, Managers, and Technical Directors
"""

import sys
sys.path.append('..')

from src.opta_analytics.performance_index import OptaPerformanceIndex, PerformanceMetrics, OptaBasketballIndex
from src.opta_analytics.expected_goals import ExpectedGoalsEngine, ShotContext
from src.opta_analytics.scouting_reports import ProfessionalScoutingReport


def example_football_player_analysis():
    """Example: Analyze a football player like a professional scout."""

    print("="*80)
    print("OPTA-STYLE FOOTBALL PLAYER ANALYSIS")
    print("="*80)
    print()

    # Create performance metrics for a midfielder
    metrics = PerformanceMetrics(
        goals=2,
        assists=1,
        shots=6,
        shots_on_target=3,
        key_passes=4,
        successful_dribbles=3,
        passes_attempted=65,
        passes_completed=58,
        progressive_passes=8,
        tackles=5,
        interceptions=4,
        clearances=2,
        blocks=1,
        touches=85,
        possession_won=7,
        possession_lost=4,
        fouls_committed=1,
        fouls_won=2,
        yellow_cards=0,
        red_cards=0,
        minutes_played=90,
        team_goals_for=3,
        team_goals_against=1,
    )

    # Calculate Opta Performance Index
    index_calculator = OptaPerformanceIndex()
    result = index_calculator.calculate_index(metrics, position='MID')

    print("OPTA PERFORMANCE INDEX")
    print("-"*80)
    print(f"Index Score: {result['opta_index']}/100")
    print(f"Rating: {result['rating']}")
    print(f"Performance Level: {result['performance_level']}")
    print(f"Percentile: {result['percentile']}th")
    print()

    print("PERFORMANCE BREAKDOWN:")
    for category, score in result['breakdown'].items():
        print(f"  {category.capitalize()}: {score}")
    print()

    print("INTERPRETATION:")
    if result['opta_index'] >= 70:
        print("  ✓ Elite performance - Exceptional match")
    elif result['opta_index'] >= 60:
        print("  ✓ Strong performance - Good match")
    elif result['opta_index'] >= 50:
        print("  ◉ Average performance - Solid contribution")
    else:
        print("  ✗ Below-par performance - Needs improvement")
    print()


def example_xg_analysis():
    """Example: Calculate Expected Goals for a shot."""

    print("="*80)
    print("EXPECTED GOALS (xG) ANALYSIS")
    print("="*80)
    print()

    engine = ExpectedGoalsEngine()

    # Example 1: Big chance - one-on-one
    print("SHOT 1: One-on-One Situation")
    print("-"*80)

    shot1 = ShotContext(
        distance_to_goal=10.0,
        angle_to_goal=8.0,
        shot_type='right_foot',
        body_part='foot',
        assist_type='through_ball',
        game_state='counter_attack',
        defender_pressure='low',
        goalkeeper_position='off_line',
        one_on_one=True,
        big_chance=True
    )

    result1 = engine.calculate_xg(shot1)
    print(f"xG Value: {result1['xg']} ({result1['xg_percentage']}%)")
    print(f"Shot Quality: {result1['shot_quality'].upper()}")
    print(f"Recommendation: {result1['recommendation']}")
    print()

    # Example 2: Long-range shot
    print("SHOT 2: Long-Range Effort")
    print("-"*80)

    shot2 = ShotContext(
        distance_to_goal=28.0,
        angle_to_goal=12.0,
        shot_type='right_foot',
        body_part='foot',
        assist_type='none',
        game_state='open_play',
        defender_pressure='medium',
        goalkeeper_position='set',
        one_on_one=False,
        big_chance=False
    )

    result2 = engine.calculate_xg(shot2)
    print(f"xG Value: {result2['xg']} ({result2['xg_percentage']}%)")
    print(f"Shot Quality: {result2['shot_quality'].upper()}")
    print(f"Recommendation: {result2['recommendation']}")
    print()

    # Match xG summary
    print("MATCH xG SUMMARY")
    print("-"*80)
    shots = [shot1, shot2]
    match_xg = engine.calculate_match_xg(shots)

    print(f"Total xG: {match_xg['total_xg']}")
    print(f"Shots: {match_xg['shots']}")
    print(f"Big Chances: {match_xg['big_chances']}")
    print(f"Average xG per Shot: {match_xg['average_xg_per_shot']}")
    print(f"Assessment: {match_xg['expected_goals_description']}")
    print()


def example_basketball_player_analysis():
    """Example: Analyze an NBA player."""

    print("="*80)
    print("OPTA-STYLE BASKETBALL PLAYER ANALYSIS")
    print("="*80)
    print()

    # Example NBA player stats
    player_stats = {
        'player_name': 'Example Player',
        'points_per_game': 24.5,
        'rebounds_per_game': 8.2,
        'assists_per_game': 6.1,
        'steals_per_game': 1.4,
        'blocks_per_game': 0.8,
        'turnovers_per_game': 2.9,
        'field_goal_pct': 0.485,
        'three_point_pct': 0.375,
        'free_throw_pct': 0.850,
        'minutes_per_game': 34.5,
    }

    # Calculate basketball index
    basketball_index = OptaBasketballIndex()
    result = basketball_index.calculate_index(player_stats)

    print("NBA PERFORMANCE INDEX")
    print("-"*80)
    print(f"Index Score: {result['opta_index']}/100")
    print(f"Rating: {result['rating']}")
    print(f"Performance Level: {result['performance_level']}")
    print()

    print("PERFORMANCE BREAKDOWN:")
    for category, score in result['breakdown'].items():
        print(f"  {category.capitalize()}: {score}")
    print()

    print("STATISTICAL PROFILE:")
    print(f"  Points: {player_stats['points_per_game']} PPG")
    print(f"  Rebounds: {player_stats['rebounds_per_game']} RPG")
    print(f"  Assists: {player_stats['assists_per_game']} APG")
    print(f"  FG%: {player_stats['field_goal_pct']:.1%}")
    print(f"  3P%: {player_stats['three_point_pct']:.1%}")
    print()


def example_scouting_report():
    """Example: Generate a professional scouting report."""

    print("="*80)
    print("PROFESSIONAL SCOUTING REPORT GENERATION")
    print("="*80)
    print()

    # Example player data
    player_data = {
        'player_name': 'João Silva',
        'age': 23,
        'date_of_birth': '2001-05-15',
        'nationality': 'Brazilian',
        'team': 'FC Example',
        'position': 'MID',
        'preferred_foot': 'Right',
        'height': '178 cm',
        'weight': '72 kg',
        'contract_expiry': '2026-06-30',
        'contract_years_remaining': 2.5,
        'market_value_millions': 18.0,
        'sport': 'football',
        'matches_played': 28,
        'minutes_played': 2340,
        'goals': 6,
        'assists': 8,
        'goals_per_90': 0.23,
        'assists_per_90': 0.31,
        'xg': 5.8,
        'xa': 7.2,
        'pass_accuracy': 0.87,
        'opta_index': 68,
    }

    # Generate scouting report
    scout = ProfessionalScoutingReport()
    report = scout.generate_player_report(player_data)

    print("SCOUT REPORT GENERATED")
    print("-"*80)
    print(f"Player: {report['player_profile']['name']}")
    print(f"Age: {report['player_profile']['age']}")
    print(f"Position: {report['player_profile']['position']}")
    print(f"Market Value: €{report['player_profile']['market_value']}M")
    print()

    print("PERFORMANCE ANALYSIS:")
    perf = report['performance_analysis']
    print(f"  Appearances: {perf['appearances']}")
    print(f"  Goals: {perf['goals']}")
    print(f"  Assists: {perf['assists']}")
    print(f"  Performance Rating: {perf['performance_rating']}")
    print()

    print("MARKET INTELLIGENCE:")
    market = report['market_intelligence']
    print(f"  Transfer Fee Estimate: €{market['estimated_transfer_fee_millions']}M")
    print(f"  Wage Estimate: €{market['wage_estimate_millions_annual']}M/year")
    print(f"  Transfer Likelihood: {market['transfer_likelihood']}")
    print(f"  Investment Rating: {market['investment_rating']}")
    print()

    print("FINAL VERDICT:")
    verdict = report['scouting_verdict']
    print(f"  Recommendation: {verdict['recommendation']}")
    print(f"  Confidence: {verdict['confidence_level']}")
    print(f"  Rationale: {verdict['rationale']}")
    print(f"  Target Price: €{verdict['target_price_millions']}M")
    print(f"  Maximum Price: €{verdict['maximum_price_millions']}M")
    print()

    print("NEXT STEPS:")
    for step in verdict['next_steps']:
        print(f"  • {step}")
    print()


def main():
    """Run all examples."""

    print("\n")
    print("█"*80)
    print(" "*20 + "OPTA-STYLE PROFESSIONAL ANALYTICS")
    print(" "*25 + "For Professional Teams")
    print("█"*80)
    print("\n")

    # Run examples
    example_football_player_analysis()
    input("Press Enter to continue to xG analysis...")
    print("\n")

    example_xg_analysis()
    input("Press Enter to continue to basketball analysis...")
    print("\n")

    example_basketball_player_analysis()
    input("Press Enter to continue to scouting report...")
    print("\n")

    example_scouting_report()

    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print()
    print("These analytics are now available for:")
    print("  ✓ Professional scouts")
    print("  ✓ Team managers")
    print("  ✓ Technical directors")
    print("  ✓ Data analysts")
    print()
    print("Use these tools to make data-driven decisions in:")
    print("  • Player recruitment")
    print("  • Transfer negotiations")
    print("  • Performance evaluation")
    print("  • Tactical planning")
    print("  • Market intelligence")
    print()


if __name__ == "__main__":
    main()
