"""
Free Football Data Collection using TheSportsDB API
No API key required - completely free!
"""

import requests
import pandas as pd
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json

from config.api_config import FREE_APIS, THESPORTSDB_LEAGUE_IDS


class FreeFootballAPI:
    """Collect real football data from free APIs."""

    def __init__(self, output_dir: str = "data/raw/football_free"):
        """Initialize free football API collector."""
        self.base_url = FREE_APIS['football']['thesportsdb']['base_url']
        self.endpoints = FREE_APIS['football']['thesportsdb']['endpoints']
        self.league_ids = THESPORTSDB_LEAGUE_IDS['football']
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make API request with rate limiting.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            JSON response or None
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(2)  # Rate limiting: 1 request per 2 seconds
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_live_scores(self, league_name: str = 'EPL') -> pd.DataFrame:
        """
        Get live scores for a league.

        Args:
            league_name: League identifier (e.g., 'EPL', 'LALIGA')

        Returns:
            DataFrame with live match data
        """
        print(f"Fetching live scores for {league_name}...")

        league_id = self.league_ids.get(league_name)
        if not league_id:
            print(f"League {league_name} not found")
            return pd.DataFrame()

        endpoint = self.endpoints['live_scores'].format(league_id=league_id)
        data = self._make_request(endpoint)

        if not data or 'events' not in data or not data['events']:
            print(f"No live matches for {league_name}")
            return pd.DataFrame()

        # Parse live matches
        matches = []
        for event in data['events']:
            match = {
                'match_id': event.get('idEvent'),
                'league': event.get('strLeague'),
                'date': event.get('dateEvent'),
                'time': event.get('strTime'),
                'home_team': event.get('strHomeTeam'),
                'away_team': event.get('strAwayTeam'),
                'home_score': event.get('intHomeScore'),
                'away_score': event.get('intAwayScore'),
                'status': event.get('strStatus'),
                'round': event.get('intRound'),
                'venue': event.get('strVenue'),
            }
            matches.append(match)

        df = pd.DataFrame(matches)
        print(f"Found {len(df)} live/recent matches")
        return df

    def get_league_fixtures(self, league_name: str = 'EPL', next_matches: bool = True) -> pd.DataFrame:
        """
        Get upcoming or past fixtures for a league.

        Args:
            league_name: League identifier
            next_matches: If True, get upcoming matches; else get past matches

        Returns:
            DataFrame with fixtures
        """
        league_id = self.league_ids.get(league_name)
        if not league_id:
            print(f"League {league_name} not found")
            return pd.DataFrame()

        endpoint_key = 'fixtures' if next_matches else 'results'
        endpoint = self.endpoints[endpoint_key].format(league_id=league_id)

        print(f"Fetching {'upcoming' if next_matches else 'past'} fixtures for {league_name}...")
        data = self._make_request(endpoint)

        if not data or 'events' not in data or not data['events']:
            print(f"No fixtures found for {league_name}")
            return pd.DataFrame()

        matches = []
        for event in data['events']:
            match = {
                'match_id': event.get('idEvent'),
                'league': event.get('strLeague'),
                'season': event.get('strSeason'),
                'date': event.get('dateEvent'),
                'time': event.get('strTime'),
                'home_team': event.get('strHomeTeam'),
                'away_team': event.get('strAwayTeam'),
                'home_score': event.get('intHomeScore'),
                'away_score': event.get('intAwayScore'),
                'round': event.get('intRound'),
                'venue': event.get('strVenue'),
                'status': event.get('strStatus'),
                'spectators': event.get('intSpectators'),
            }
            matches.append(match)

        df = pd.DataFrame(matches)

        # Save to CSV
        filename = f"{league_name}_{'fixtures' if next_matches else 'results'}.csv"
        output_file = self.output_dir / filename
        df.to_csv(output_file, index=False)
        print(f"Saved {len(df)} matches to {output_file}")

        return df

    def get_league_standings(self, league_name: str = 'EPL', season: str = '2023-2024') -> pd.DataFrame:
        """
        Get league standings/table.

        Args:
            league_name: League identifier
            season: Season (e.g., '2023-2024')

        Returns:
            DataFrame with standings
        """
        league_id = self.league_ids.get(league_name)
        if not league_id:
            print(f"League {league_name} not found")
            return pd.DataFrame()

        endpoint = self.endpoints['standings'].format(league_id=league_id, season=season)
        print(f"Fetching standings for {league_name} {season}...")

        data = self._make_request(endpoint)

        if not data or 'table' not in data or not data['table']:
            print(f"No standings data for {league_name}")
            return pd.DataFrame()

        standings = []
        for team in data['table']:
            standing = {
                'position': team.get('intRank'),
                'team': team.get('strTeam'),
                'team_id': team.get('idTeam'),
                'played': team.get('intPlayed'),
                'wins': team.get('intWin'),
                'draws': team.get('intDraw'),
                'losses': team.get('intLoss'),
                'goals_for': team.get('intGoalsFor'),
                'goals_against': team.get('intGoalsAgainst'),
                'goal_difference': team.get('intGoalDifference'),
                'points': team.get('intPoints'),
                'form': team.get('strForm'),
            }
            standings.append(standing)

        df = pd.DataFrame(standings)
        df = df.sort_values('position')

        # Save to CSV
        output_file = self.output_dir / f"{league_name}_standings_{season}.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved standings to {output_file}")

        return df

    def get_team_details(self, team_id: str) -> Dict:
        """
        Get detailed team information.

        Args:
            team_id: TheSportsDB team ID

        Returns:
            Dictionary with team details
        """
        endpoint = self.endpoints['team_details'].format(team_id=team_id)
        print(f"Fetching team details for ID {team_id}...")

        data = self._make_request(endpoint)

        if not data or 'teams' not in data or not data['teams']:
            return {}

        team = data['teams'][0]
        return {
            'team_id': team.get('idTeam'),
            'name': team.get('strTeam'),
            'short_name': team.get('strTeamShort'),
            'alternate_name': team.get('strAlternate'),
            'formed_year': team.get('intFormedYear'),
            'stadium': team.get('strStadium'),
            'stadium_capacity': team.get('intStadiumCapacity'),
            'stadium_location': team.get('strStadiumLocation'),
            'league': team.get('strLeague'),
            'manager': team.get('strManager'),
            'website': team.get('strWebsite'),
            'description': team.get('strDescriptionEN'),
            'country': team.get('strCountry'),
        }

    def get_team_players(self, team_id: str) -> pd.DataFrame:
        """
        Get all players for a team.

        Args:
            team_id: TheSportsDB team ID

        Returns:
            DataFrame with player data
        """
        endpoint = self.endpoints['team_players'].format(team_id=team_id)
        print(f"Fetching players for team ID {team_id}...")

        data = self._make_request(endpoint)

        if not data or 'player' not in data or not data['player']:
            print("No players found")
            return pd.DataFrame()

        players = []
        for player in data['player']:
            player_data = {
                'player_id': player.get('idPlayer'),
                'name': player.get('strPlayer'),
                'nationality': player.get('strNationality'),
                'position': player.get('strPosition'),
                'birth_date': player.get('dateBorn'),
                'height': player.get('strHeight'),
                'weight': player.get('strWeight'),
                'number': player.get('strNumber'),
                'wage': player.get('strWage'),
                'description': player.get('strDescriptionEN'),
            }
            players.append(player_data)

        df = pd.DataFrame(players)
        print(f"Found {len(df)} players")
        return df

    def collect_full_league_data(self, league_name: str = 'EPL', season: str = '2023-2024') -> Dict[str, pd.DataFrame]:
        """
        Collect comprehensive league data.

        Args:
            league_name: League identifier
            season: Season

        Returns:
            Dictionary with all league data
        """
        print(f"\n{'='*60}")
        print(f"COLLECTING FULL DATA FOR {league_name} - {season}")
        print(f"{'='*60}\n")

        data = {}

        # 1. Live scores
        print("📊 Step 1: Live Scores")
        data['live_scores'] = self.get_live_scores(league_name)

        # 2. Upcoming fixtures
        print("\n📅 Step 2: Upcoming Fixtures")
        data['fixtures'] = self.get_league_fixtures(league_name, next_matches=True)

        # 3. Past results
        print("\n📈 Step 3: Past Results")
        data['results'] = self.get_league_fixtures(league_name, next_matches=False)

        # 4. League standings
        print("\n🏆 Step 4: League Standings")
        data['standings'] = self.get_league_standings(league_name, season)

        # 5. Team details and players
        if not data['standings'].empty:
            print("\n👥 Step 5: Team Details & Players")
            teams_data = []
            all_players = []

            for idx, row in data['standings'].head(5).iterrows():  # Top 5 teams
                team_id = row['team_id']
                team_name = row['team']

                print(f"\n  Processing {team_name}...")

                # Get team details
                team_details = self.get_team_details(team_id)
                if team_details:
                    teams_data.append(team_details)

                # Get team players
                players_df = self.get_team_players(team_id)
                if not players_df.empty:
                    players_df['team'] = team_name
                    all_players.append(players_df)

                time.sleep(2)  # Rate limiting

            if teams_data:
                data['teams'] = pd.DataFrame(teams_data)

            if all_players:
                data['players'] = pd.concat(all_players, ignore_index=True)

        print(f"\n{'='*60}")
        print("✓ DATA COLLECTION COMPLETE")
        print(f"{'='*60}")

        return data

    def collect_multiple_leagues(self, league_names: List[str] = None, season: str = '2023-2024') -> Dict:
        """
        Collect data for multiple leagues.

        Args:
            league_names: List of league identifiers
            season: Season

        Returns:
            Dictionary with data for all leagues
        """
        if league_names is None:
            league_names = ['EPL', 'LALIGA', 'BUNDESLIGA', 'SERIEA', 'LIGUE1']

        all_data = {}

        for league in league_names:
            try:
                all_data[league] = self.collect_full_league_data(league, season)
                time.sleep(5)  # Longer pause between leagues
            except Exception as e:
                print(f"Error collecting data for {league}: {e}")
                continue

        return all_data


if __name__ == "__main__":
    # Example usage
    api = FreeFootballAPI()

    # Collect data for English Premier League
    epl_data = api.collect_full_league_data('EPL', '2023-2024')

    print("\n" + "="*60)
    print("DATA SUMMARY:")
    print("="*60)
    for key, value in epl_data.items():
        if isinstance(value, pd.DataFrame):
            print(f"{key}: {len(value)} records")
