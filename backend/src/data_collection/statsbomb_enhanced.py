"""
StatsBomb Free Data Integration - Enhanced Data Collection
StatsBomb provides FREE detailed event data for multiple competitions.
This gives us Opta-level detail for player analysis.
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import json


class StatsBombEnhancedAPI:
    """
    StatsBomb provides FREE access to:
    - Event-level data (passes, shots, tackles with coordinates)
    - Multiple competitions (World Cup, Champions League, etc.)
    - Advanced metrics (xG, progressive actions, pressure events)

    NO API KEY REQUIRED - Completely free!
    """

    BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

    def __init__(self):
        """Initialize StatsBomb API client."""
        self.competitions_cache = None
        self.matches_cache = {}

    def get_competitions(self) -> pd.DataFrame:
        """
        Get all available free competitions.

        Returns:
            DataFrame with competition details
        """
        if self.competitions_cache is not None:
            return self.competitions_cache

        try:
            url = f"{self.BASE_URL}/competitions.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            competitions = pd.DataFrame(response.json())
            self.competitions_cache = competitions

            print(f"✓ Found {len(competitions)} free competitions:")
            for _, comp in competitions.iterrows():
                print(f"  • {comp['competition_name']} - {comp['season_name']}")

            return competitions

        except Exception as e:
            print(f"Error fetching competitions: {e}")
            return pd.DataFrame()

    def get_matches(self, competition_id: int, season_id: int) -> pd.DataFrame:
        """
        Get all matches for a competition/season.

        Args:
            competition_id: Competition ID
            season_id: Season ID

        Returns:
            DataFrame with match details
        """
        cache_key = f"{competition_id}_{season_id}"
        if cache_key in self.matches_cache:
            return self.matches_cache[cache_key]

        try:
            url = f"{self.BASE_URL}/matches/{competition_id}/{season_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            matches = pd.DataFrame(response.json())
            self.matches_cache[cache_key] = matches

            return matches

        except Exception as e:
            print(f"Error fetching matches: {e}")
            return pd.DataFrame()

    def get_match_events(self, match_id: int) -> pd.DataFrame:
        """
        Get ALL events for a match (passes, shots, tackles, etc.).
        This is where we get Opta-level detail!

        Args:
            match_id: Match ID

        Returns:
            DataFrame with every event in the match
        """
        try:
            url = f"{self.BASE_URL}/events/{match_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            events = pd.json_normalize(response.json())

            return events

        except Exception as e:
            print(f"Error fetching match events: {e}")
            return pd.DataFrame()

    def get_lineups(self, match_id: int) -> Dict:
        """
        Get lineups for a match.

        Args:
            match_id: Match ID

        Returns:
            Dictionary with team lineups
        """
        try:
            url = f"{self.BASE_URL}/lineups/{match_id}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error fetching lineups: {e}")
            return {}

    def analyze_player_comprehensive(self, player_name: str,
                                    competition_id: int = None,
                                    season_id: int = None) -> Dict:
        """
        Comprehensive player analysis across all available matches.
        This gives us Opta-style detailed statistics.

        Args:
            player_name: Player name to analyze
            competition_id: Optional competition filter
            season_id: Optional season filter

        Returns:
            Comprehensive player statistics dictionary
        """
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE ANALYSIS: {player_name}")
        print(f"{'='*80}\n")

        # Get competitions
        competitions = self.get_competitions()

        if competitions.empty:
            return {}

        # Filter if specified
        if competition_id and season_id:
            competitions = competitions[
                (competitions['competition_id'] == competition_id) &
                (competitions['season_id'] == season_id)
            ]

        # Collect all events for this player
        all_player_events = []
        matches_analyzed = 0

        for _, comp in competitions.iterrows():
            comp_id = comp['competition_id']
            seas_id = comp['season_id']

            print(f"Analyzing {comp['competition_name']} - {comp['season_name']}...")

            matches = self.get_matches(comp_id, seas_id)

            if matches.empty:
                continue

            # Analyze first 10 matches (to avoid too many API calls)
            for match_id in matches['match_id'].head(10):
                events = self.get_match_events(match_id)

                if events.empty:
                    continue

                # Filter events for this player
                player_events = events[
                    events['player.name'].str.contains(player_name, case=False, na=False)
                ]

                if not player_events.empty:
                    all_player_events.append(player_events)
                    matches_analyzed += 1

        if not all_player_events:
            print(f"No data found for {player_name}")
            return {}

        # Combine all events
        all_events_df = pd.concat(all_player_events, ignore_index=True)

        # Calculate comprehensive statistics
        stats = self._calculate_comprehensive_stats(all_events_df, player_name)
        stats['matches_analyzed'] = matches_analyzed

        return stats

    def _calculate_comprehensive_stats(self, events: pd.DataFrame,
                                      player_name: str) -> Dict:
        """
        Calculate Opta-style comprehensive statistics from events.

        Args:
            events: All events for the player
            player_name: Player name

        Returns:
            Comprehensive statistics dictionary
        """
        stats = {
            'player_name': player_name,
            'total_events': len(events),

            # Passing
            'passes_attempted': 0,
            'passes_completed': 0,
            'pass_completion_rate': 0.0,
            'key_passes': 0,
            'progressive_passes': 0,
            'long_passes': 0,
            'through_balls': 0,

            # Shooting
            'shots': 0,
            'shots_on_target': 0,
            'goals': 0,
            'expected_goals_xg': 0.0,
            'shot_accuracy': 0.0,

            # Dribbling
            'dribbles_attempted': 0,
            'dribbles_completed': 0,
            'dribble_success_rate': 0.0,

            # Defensive
            'tackles': 0,
            'interceptions': 0,
            'clearances': 0,
            'blocks': 0,
            'pressures': 0,
            'pressure_success_rate': 0.0,

            # Possession
            'touches': len(events),
            'dispossessed': 0,
            'miscontrols': 0,

            # Advanced
            'progressive_carries': 0,
            'carries_into_final_third': 0,
            'carries_into_box': 0,
        }

        # Calculate pass statistics
        pass_events = events[events['type.name'] == 'Pass']
        stats['passes_attempted'] = len(pass_events)

        if not pass_events.empty:
            completed_passes = pass_events[
                pass_events['pass.outcome.name'].isna()  # No outcome means successful
            ]
            stats['passes_completed'] = len(completed_passes)

            if stats['passes_attempted'] > 0:
                stats['pass_completion_rate'] = round(
                    (stats['passes_completed'] / stats['passes_attempted']) * 100, 1
                )

            # Key passes (assists)
            stats['key_passes'] = len(pass_events[
                pass_events['pass.goal_assist'] == True
            ])

            # Progressive passes
            stats['progressive_passes'] = len(pass_events[
                pass_events['pass.type.name'] == 'Progressive'
            ])

            # Long passes
            stats['long_passes'] = len(pass_events[
                pass_events['pass.length'].notna() & (pass_events['pass.length'] > 30)
            ])

            # Through balls
            stats['through_balls'] = len(pass_events[
                pass_events['pass.through_ball'] == True
            ])

        # Calculate shot statistics
        shot_events = events[events['type.name'] == 'Shot']
        stats['shots'] = len(shot_events)

        if not shot_events.empty:
            stats['goals'] = len(shot_events[
                shot_events['shot.outcome.name'] == 'Goal'
            ])

            stats['shots_on_target'] = len(shot_events[
                shot_events['shot.outcome.name'].isin(['Goal', 'Saved'])
            ])

            if stats['shots'] > 0:
                stats['shot_accuracy'] = round(
                    (stats['shots_on_target'] / stats['shots']) * 100, 1
                )

            # xG
            if 'shot.statsbomb_xg' in shot_events.columns:
                stats['expected_goals_xg'] = round(
                    shot_events['shot.statsbomb_xg'].sum(), 2
                )

        # Calculate dribble statistics
        dribble_events = events[events['type.name'] == 'Dribble']
        stats['dribbles_attempted'] = len(dribble_events)

        if not dribble_events.empty:
            stats['dribbles_completed'] = len(dribble_events[
                dribble_events['dribble.outcome.name'] == 'Complete'
            ])

            if stats['dribbles_attempted'] > 0:
                stats['dribble_success_rate'] = round(
                    (stats['dribbles_completed'] / stats['dribbles_attempted']) * 100, 1
                )

        # Calculate defensive statistics
        stats['tackles'] = len(events[events['type.name'] == 'Duel'])
        stats['interceptions'] = len(events[events['type.name'] == 'Interception'])
        stats['clearances'] = len(events[events['type.name'] == 'Clearance'])
        stats['blocks'] = len(events[events['type.name'] == 'Block'])

        pressure_events = events[events['type.name'] == 'Pressure']
        stats['pressures'] = len(pressure_events)

        # Calculate carry statistics
        carry_events = events[events['type.name'] == 'Carry']
        stats['progressive_carries'] = len(carry_events[
            carry_events['carry.end_location'].notna()
        ])

        return stats

    def get_player_heat_map_data(self, player_name: str,
                                 competition_id: int = None) -> List[Dict]:
        """
        Get player location data for heat map visualization.

        Args:
            player_name: Player name
            competition_id: Optional competition filter

        Returns:
            List of location dictionaries with x, y coordinates
        """
        # Implementation would collect all event locations for heat maps
        # This is what Opta uses for player positioning analysis
        pass

    def compare_players(self, player1: str, player2: str,
                       competition_id: int = None) -> pd.DataFrame:
        """
        Compare two players across all metrics.

        Args:
            player1: First player name
            player2: Second player name
            competition_id: Optional competition filter

        Returns:
            Comparison DataFrame
        """
        stats1 = self.analyze_player_comprehensive(player1, competition_id)
        stats2 = self.analyze_player_comprehensive(player2, competition_id)

        comparison = pd.DataFrame([stats1, stats2])

        return comparison


# Example usage
if __name__ == "__main__":
    print("\n" + "="*80)
    print("STATSBOMB ENHANCED DATA COLLECTION")
    print("Get Opta-level detail from FREE StatsBomb data!")
    print("="*80)

    api = StatsBombEnhancedAPI()

    # Get available competitions
    print("\nStep 1: Getting available free competitions...")
    competitions = api.get_competitions()

    if not competitions.empty:
        print(f"\n✓ Found {len(competitions)} competitions with FREE detailed data!")

        # Example: Analyze a player
        print("\n" + "="*80)
        print("Example: Comprehensive Player Analysis")
        print("="*80)

        # Get first competition
        comp_id = competitions.iloc[0]['competition_id']
        season_id = competitions.iloc[0]['season_id']

        print(f"\nAnalyzing competition: {competitions.iloc[0]['competition_name']}")

        # Get matches
        matches = api.get_matches(comp_id, season_id)

        if not matches.empty:
            print(f"Found {len(matches)} matches")

            # Analyze first match to get player names
            match_id = matches.iloc[0]['match_id']
            events = api.get_match_events(match_id)

            if not events.empty:
                # Get top players
                top_players = events['player.name'].value_counts().head(5)

                print(f"\nTop 5 players by events in match {match_id}:")
                print(top_players)

                # Comprehensive analysis of top player
                if len(top_players) > 0:
                    top_player = top_players.index[0]

                    print(f"\n{'='*80}")
                    print(f"COMPREHENSIVE ANALYSIS: {top_player}")
                    print(f"{'='*80}")

                    stats = api.analyze_player_comprehensive(
                        top_player,
                        comp_id,
                        season_id
                    )

                    print(f"\n📊 STATISTICS:")
                    print(f"  Passes: {stats['passes_completed']}/{stats['passes_attempted']} ({stats['pass_completion_rate']}%)")
                    print(f"  Shots: {stats['shots']} ({stats['shots_on_target']} on target)")
                    print(f"  Goals: {stats['goals']}")
                    print(f"  xG: {stats['expected_goals_xg']}")
                    print(f"  Key Passes: {stats['key_passes']}")
                    print(f"  Dribbles: {stats['dribbles_completed']}/{stats['dribbles_attempted']} ({stats['dribble_success_rate']}%)")
                    print(f"  Tackles: {stats['tackles']}")
                    print(f"  Interceptions: {stats['interceptions']}")
                    print(f"  Pressures: {stats['pressures']}")

                    print(f"\n✓ This is OPTA-LEVEL detail from FREE data!")
