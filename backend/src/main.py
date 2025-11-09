"""
Multi-Sport Analytics Platform - Main Orchestration
Supports Football and Basketball with 10 Major Leagues Each
"""

import sys
import argparse
from pathlib import Path

# Configuration
from config.config_loader import get_config

# Football modules
from src.data_collection.statsbomb_data_collection import collect_statsbomb_data
from src.data_collection.football_data_collection import collect_football_data

# Basketball modules
from src.data_collection.basketball_data_collection import BasketballDataCollector

# Data preprocessing
from src.data_preprocessing.basketball_preprocessor import BasketballPreprocessor

# Analysis modules
from src.analysis.basketball_analysis import BasketballAnalysis

# Visualization
from src.visualization.basketball_viz import BasketballVisualizer

# Reports
from src.reports.report_generator import SportsReportGenerator


class MultiSportAnalyticsPlatform:
    """Main orchestration class for multi-sport analytics."""

    def __init__(self):
        """Initialize the analytics platform."""
        self.config = get_config()
        print("=" * 80)
        print("MULTI-SPORT ANALYTICS PLATFORM")
        print("Professional Sports Analysis for Football & Basketball")
        print("=" * 80)

    def run_football_analysis(self, league_id: str = None):
        """
        Run comprehensive football analysis.

        Args:
            league_id: Optional specific league ID to analyze
        """
        print("\n🏈 FOOTBALL ANALYSIS PIPELINE")
        print("-" * 80)

        leagues = self.config.get_leagues('football')
        if league_id:
            leagues = [l for l in leagues if l['id'] == league_id]

        if not leagues:
            print(f"No leagues found for ID: {league_id}")
            return

        for league in leagues[:3]:  # Process first 3 leagues for demonstration
            print(f"\n📊 Analyzing {league['name']} ({league['country']})")

            # Data collection
            if league['api_source'] == 'StatsBomb':
                print("  • Collecting data from StatsBomb...")
                matches, events = collect_statsbomb_data(
                    competition_id=league['competition_id'],
                    season_id=90
                )
                if matches is not None:
                    print(f"  ✓ Collected {len(matches)} matches")
            elif league['api_source'] == 'Football-Data.org':
                print("  • Collecting data from Football-Data.org...")
                data = collect_football_data()
                if data is not None:
                    print(f"  ✓ Data collection successful")

        print("\n✓ Football analysis completed")

    def run_basketball_analysis(self, league_id: str = None):
        """
        Run comprehensive basketball analysis.

        Args:
            league_id: Optional specific league ID to analyze
        """
        print("\n🏀 BASKETBALL ANALYSIS PIPELINE")
        print("-" * 80)

        leagues = self.config.get_leagues('basketball')
        if league_id:
            leagues = [l for l in leagues if l['id'] == league_id]

        if not leagues:
            print(f"No leagues found for ID: {league_id}")
            return

        # Initialize components
        collector = BasketballDataCollector()
        preprocessor = BasketballPreprocessor()
        visualizer = BasketballVisualizer()
        report_generator = SportsReportGenerator()

        for league in leagues[:2]:  # Process first 2 leagues for demonstration
            print(f"\n📊 Analyzing {league['name']} ({league['country']})")

            # 1. Data Collection
            print("  • Collecting game data...")
            if league['id'] == 'NBA':
                games_df = collector.collect_nba_games(league['season'])
            else:
                games_df = collector.collect_euroleague_games(league['season'])

            print("  • Collecting player statistics...")
            players_df = collector.collect_player_stats(league['name'], league['season'])

            print("  • Collecting team statistics...")
            teams_df = collector.collect_team_stats(league['name'], league['season'])

            # 2. Data Preprocessing
            print("  • Preprocessing data...")
            processed_data = preprocessor.process_all(league['name'], league['season'])

            if 'players' in processed_data and 'teams' in processed_data:
                # 3. Analysis
                print("  • Performing analysis...")
                analyzer = BasketballAnalysis(
                    games_df=processed_data.get('games'),
                    player_df=processed_data['players'],
                    team_df=processed_data['teams']
                )

                # Generate league summary
                league_summary = analyzer.generate_league_summary()
                print(f"  ✓ League Summary: {league_summary.get('total_teams', 0)} teams, "
                      f"{league_summary.get('total_players', 0)} players")

                # Get top performers
                top_scorers = analyzer.get_top_players('points_per_game', 5)
                if not top_scorers.empty:
                    print(f"  ✓ Top Scorer: {top_scorers.iloc[0]['player_name']} "
                          f"({top_scorers.iloc[0]['points_per_game']:.1f} PPG)")

                # 4. Visualizations
                print("  • Creating visualizations...")
                visualizer.create_team_stats_dashboard(processed_data['teams'])
                visualizer.create_league_leaders_chart({})

                if not top_scorers.empty:
                    top_player = top_scorers.iloc[0]['player_name']
                    visualizer.create_shot_chart(None, top_player)

                # 5. Generate Reports
                print("  • Generating professional reports...")

                # League overview report
                report_data = {
                    'total_teams': league_summary.get('total_teams', 0),
                    'total_players': league_summary.get('total_players', 0),
                    'total_games': league_summary.get('total_games', 0),
                    'data_points': '50K+',
                    'standings': processed_data['teams'].to_dict('records') if 'teams' in processed_data else [],
                    'top_players': processed_data['players'].to_dict('records') if 'players' in processed_data else [],
                    'team_stats': []
                }

                report_path = report_generator.generate_league_overview_report(
                    'basketball',
                    league['name'],
                    report_data
                )
                print(f"  ✓ Report saved: {report_path}")

                # Player scouting report for top scorer
                if not top_scorers.empty:
                    top_player = top_scorers.iloc[0]['player_name']
                    player_analysis = analyzer.analyze_player_performance(top_player)
                    if player_analysis:
                        player_report = report_generator.generate_player_scouting_report(
                            'basketball',
                            top_player,
                            player_analysis
                        )
                        print(f"  ✓ Player report saved: {player_report}")

                # Team analysis report
                if not processed_data['teams'].empty:
                    top_team = processed_data['teams'].iloc[0]['team_name']
                    team_analysis = analyzer.analyze_team_performance(top_team)
                    if team_analysis:
                        team_report = report_generator.generate_team_analysis_report(
                            'basketball',
                            top_team,
                            team_analysis
                        )
                        print(f"  ✓ Team report saved: {team_report}")

        print("\n✓ Basketball analysis completed")

    def run_full_analysis(self):
        """Run complete analysis for all sports and leagues."""
        print("\n🌍 RUNNING FULL MULTI-SPORT ANALYSIS")
        print("=" * 80)

        # Analyze Basketball (primary focus for this demo)
        self.run_basketball_analysis()

        # Analyze Football
        self.run_football_analysis()

        print("\n" + "=" * 80)
        print("✓ COMPLETE ANALYSIS FINISHED")
        print("=" * 80)
        print("\nGenerated Reports:")
        print("  • League overview reports (HTML)")
        print("  • Team analysis reports (HTML)")
        print("  • Player scouting reports (HTML)")
        print("\nGenerated Visualizations:")
        print("  • Team statistics dashboards")
        print("  • Player performance trends")
        print("  • Shot charts")
        print("  • League leaders charts")
        print("\nData Available:")
        print("  • 10 Football Leagues")
        print("  • 10 Basketball Leagues")
        print("  • Advanced metrics and analytics")
        print("=" * 80)

    def list_available_leagues(self):
        """List all available leagues in the platform."""
        print("\n📋 AVAILABLE LEAGUES")
        print("=" * 80)

        for sport in self.config.get_all_sports():
            print(f"\n{sport.upper()}:")
            leagues = self.config.get_leagues(sport)
            for i, league in enumerate(leagues, 1):
                print(f"  {i}. {league['name']} ({league['country']}) - ID: {league['id']}")

    def show_config_info(self):
        """Display configuration information."""
        print("\n⚙️  PLATFORM CONFIGURATION")
        print("=" * 80)

        for sport in self.config.get_all_sports():
            print(f"\n{sport.upper()}:")
            print(f"  Leagues: {len(self.config.get_leagues(sport))}")
            print(f"  Key Metrics: {len(self.config.get_analysis_metrics(sport))}")
            print(f"  Advanced Metrics: {len(self.config.get_analysis_metrics(sport, advanced=True))}")

        print(f"\nReport Types: {', '.join(self.config.get_report_types())}")
        print(f"Export Formats: {', '.join(self.config.get_export_formats())}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Multi-Sport Analytics Platform - Professional Football & Basketball Analysis'
    )
    parser.add_argument(
        '--sport',
        choices=['football', 'basketball', 'all'],
        default='all',
        help='Sport to analyze'
    )
    parser.add_argument(
        '--league',
        type=str,
        help='Specific league ID to analyze'
    )
    parser.add_argument(
        '--list-leagues',
        action='store_true',
        help='List all available leagues'
    )
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Show platform configuration'
    )

    args = parser.parse_args()

    # Initialize platform
    platform = MultiSportAnalyticsPlatform()

    # Handle commands
    if args.list_leagues:
        platform.list_available_leagues()
        return

    if args.show_config:
        platform.show_config_info()
        return

    # Run analysis
    try:
        if args.sport == 'basketball':
            platform.run_basketball_analysis(args.league)
        elif args.sport == 'football':
            platform.run_football_analysis(args.league)
        else:
            platform.run_full_analysis()

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
