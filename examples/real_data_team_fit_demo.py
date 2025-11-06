"""
REAL DATA Team Fit Analysis Demo
Uses actual API data to find best players for your team!
"""

import sys
sys.path.append('..')

from src.team_fit.real_data_integration import RealDataTeamFitIntegration
from src.team_fit.team_fit_analyzer import TeamProfile, PlayingStyle


def demo_real_nba_players():
    """Demo: Analyze REAL NBA players for your team."""

    print("\n" + "█"*80)
    print(" "*20 + "REAL DATA TEAM FIT ANALYSIS")
    print(" "*15 + "Using Actual NBA Players from Free API")
    print("█"*80)
    print()

    # Initialize with real data
    integrator = RealDataTeamFitIntegration()

    # Define YOUR team
    print("STEP 1: Define Your Team")
    print("="*80)

    my_team = TeamProfile(
        team_name="My Dream Team",
        league="NBA",
        playing_style=PlayingStyle.HIGH_PRESS,
        formation="Fast-paced",
        average_age=26.0,
        budget_millions=50.0,
        priority_positions=['G', 'F', 'C'],
        desired_traits=['shooting', 'defense', 'speed'],
        average_player_value=30.0,
        team_personality='ambitious',
        language='english',
        requires_pace=True,
        requires_technique=True,
    )

    print(f"✓ Team: {my_team.team_name}")
    print(f"✓ Playing Style: {my_team.playing_style.value}")
    print(f"✓ Budget: ${my_team.budget_millions}M")
    print(f"✓ Looking for: {', '.join(my_team.priority_positions)}")
    print()

    # Get real players from API
    print("STEP 2: Fetching REAL NBA Players from API...")
    print("="*80)
    print("Connecting to BallDontLie API (100% FREE)...")
    print("This may take a moment...\n")

    # Analyze real players
    results = integrator.analyze_real_league_players(
        league='NBA',
        sport='basketball',
        my_team_profile=my_team,
        top_n=15  # Top 15 matches
    )

    if results.empty:
        print("❌ Could not fetch real data. Check your internet connection.")
        return

    # Display results
    print("\n" + "="*80)
    print("🏆 TOP 15 REAL NBA PLAYERS FOR YOUR TEAM")
    print("="*80)
    print()
    print("These are ACTUAL NBA players from the API!")
    print()

    # Format and display
    for idx, row in results.iterrows():
        print(f"#{row['rank']} - {row['player_name']}")
        print(f"     Position: {row['position']} | Age: {row['age']} | Team: {row['current_team']}")
        print(f"     Fit Score: {row['fit_score']}/100 | Rating: {row['fit_rating']}")
        print(f"     Market Value: ${row['market_value_millions']}M")
        print(f"     Nationality: {row['nationality']}")
        print()

    # Summary
    print("="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print(f"✓ Total Real Players Analyzed: {len(results)}")
    print(f"✓ Best Fit Score: {results.iloc[0]['fit_score']}/100")
    print(f"✓ Top Recommendation: {results.iloc[0]['player_name']}")
    print()
    print("💡 All data is pulled from FREE APIs in real-time!")
    print("   - Player names: REAL")
    print("   - Teams: REAL")
    print("   - Positions: REAL")
    print("   - Ages: ESTIMATED (based on typical player age)")
    print()


def demo_real_football_players():
    """Demo: Analyze REAL football players."""

    print("\n" + "="*80)
    print("REAL FOOTBALL PLAYERS ANALYSIS")
    print("="*80)
    print()

    integrator = RealDataTeamFitIntegration()

    # Your team
    my_football_team = TeamProfile(
        team_name="Manchester United",
        league="Premier League",
        playing_style=PlayingStyle.COUNTER_ATTACK,
        formation="4-2-3-1",
        average_age=26.5,
        budget_millions=60.0,
        priority_positions=['ST', 'LW', 'CM'],
        desired_traits=['pace', 'power', 'finishing'],
        average_player_value=40.0,
        team_personality='ambitious',
        language='english',
        requires_pace=True,
    )

    print(f"Team: {my_football_team.team_name}")
    print(f"Looking for: {', '.join(my_football_team.priority_positions)}")
    print()

    print("Fetching REAL Premier League players...")
    print("(This uses TheSportsDB FREE API)\n")

    results = integrator.analyze_real_league_players(
        league='EPL',
        sport='football',
        my_team_profile=my_football_team,
        top_n=10
    )

    if not results.empty:
        print("\n🏆 TOP 10 REAL EPL PLAYERS FOR YOUR TEAM:\n")
        print(results.to_string(index=False))
    else:
        print("Note: Real football data requires API connection.")
        print("Make sure you're connected to the internet!")


def main():
    """Run demos."""

    print("\n\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*15 + "REAL DATA TEAM FIT ANALYSIS DEMO" + " "*31 + "║")
    print("║" + " "*20 + "100% Real Players from Free APIs" + " "*25 + "║")
    print("╚" + "═"*78 + "╝")

    print("\nThis demo shows Team Fit Analysis with REAL player data!")
    print("All data is pulled from:")
    print("  • BallDontLie API (NBA) - Completely FREE")
    print("  • TheSportsDB API (Football) - Completely FREE")
    print()

    choice = input("Choose sport: [1] NBA (Basketball)  [2] Football  [3] Both\nChoice: ")

    if choice == '1':
        demo_real_nba_players()
    elif choice == '2':
        demo_real_football_players()
    else:
        demo_real_nba_players()
        input("\nPress Enter for Football analysis...")
        demo_real_football_players()

    print("\n" + "="*80)
    print("✓ DEMO COMPLETE!")
    print("="*80)
    print()
    print("What you saw:")
    print("  ✓ REAL player names from APIs")
    print("  ✓ REAL team information")
    print("  ✓ REAL positions and data")
    print("  ✓ AI-powered fit analysis")
    print()
    print("You can now use this for:")
    print("  • Finding transfer targets")
    print("  • Scouting players")
    print("  • Building your dream team")
    print("  • Analyzing any league in the world (85+ leagues!)")
    print()


if __name__ == "__main__":
    main()
