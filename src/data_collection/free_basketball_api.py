"""
Free Basketball Data Collection
Uses BallDontLie API (free, no key needed) and NBA official data
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json


class FreeBasketballAPI:
    """Collect real basketball data from free APIs."""

    def __init__(self, output_dir: str = "data/raw/basketball_free"):
        """Initialize free basketball API collector."""
        self.balldontlie_base = "https://www.balldontlie.io/api/v1"
        self.thesportsdb_base = "https://www.thesportsdb.com/api/v1/json/3"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling."""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(0.6)  # Rate limiting
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_nba_teams(self) -> pd.DataFrame:
        """
        Get all NBA teams.

        Returns:
            DataFrame with team data
        """
        print("Fetching NBA teams...")
        url = f"{self.balldontlie_base}/teams"

        data = self._make_request(url)

        if not data or 'data' not in data:
            return pd.DataFrame()

        teams = []
        for team in data['data']:
            team_data = {
                'team_id': team.get('id'),
                'abbreviation': team.get('abbreviation'),
                'city': team.get('city'),
                'conference': team.get('conference'),
                'division': team.get('division'),
                'full_name': team.get('full_name'),
                'name': team.get('name'),
            }
            teams.append(team_data)

        df = pd.DataFrame(teams)

        # Save to CSV
        output_file = self.output_dir / "nba_teams.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved {len(df)} teams to {output_file}")

        return df

    def get_nba_players(self, page: int = 1, per_page: int = 100) -> pd.DataFrame:
        """
        Get NBA players.

        Args:
            page: Page number
            per_page: Results per page (max 100)

        Returns:
            DataFrame with player data
        """
        print(f"Fetching NBA players (page {page})...")
        url = f"{self.balldontlie_base}/players"
        params = {'page': page, 'per_page': per_page}

        data = self._make_request(url, params)

        if not data or 'data' not in data:
            return pd.DataFrame()

        players = []
        for player in data['data']:
            player_data = {
                'player_id': player.get('id'),
                'first_name': player.get('first_name'),
                'last_name': player.get('last_name'),
                'full_name': f"{player.get('first_name')} {player.get('last_name')}",
                'position': player.get('position'),
                'height_feet': player.get('height_feet'),
                'height_inches': player.get('height_inches'),
                'weight_pounds': player.get('weight_pounds'),
                'team_id': player.get('team', {}).get('id'),
                'team_name': player.get('team', {}).get('full_name'),
                'team_abbreviation': player.get('team', {}).get('abbreviation'),
            }
            players.append(player_data)

        df = pd.DataFrame(players)
        print(f"Found {len(df)} players on page {page}")

        return df

    def get_all_nba_players(self, max_pages: int = 5) -> pd.DataFrame:
        """
        Get all NBA players (multiple pages).

        Args:
            max_pages: Maximum number of pages to fetch

        Returns:
            DataFrame with all players
        """
        all_players = []

        for page in range(1, max_pages + 1):
            players_df = self.get_nba_players(page=page, per_page=100)

            if players_df.empty:
                break

            all_players.append(players_df)
            time.sleep(1)  # Rate limiting

        if not all_players:
            return pd.DataFrame()

        df = pd.concat(all_players, ignore_index=True)

        # Save to CSV
        output_file = self.output_dir / "nba_players_all.csv"
        df.to_csv(output_file, index=False)
        print(f"\nTotal players collected: {len(df)}")

        return df

    def get_games(self, start_date: str = None, end_date: str = None, season: int = 2023) -> pd.DataFrame:
        """
        Get NBA games for a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            season: Season year

        Returns:
            DataFrame with game data
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        print(f"Fetching games from {start_date} to {end_date}...")

        url = f"{self.balldontlie_base}/games"
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'seasons[]': season,
            'per_page': 100
        }

        data = self._make_request(url, params)

        if not data or 'data' not in data:
            return pd.DataFrame()

        games = []
        for game in data['data']:
            game_data = {
                'game_id': game.get('id'),
                'date': game.get('date'),
                'season': game.get('season'),
                'status': game.get('status'),
                'period': game.get('period'),
                'time': game.get('time'),
                'postseason': game.get('postseason'),
                'home_team_id': game.get('home_team', {}).get('id'),
                'home_team': game.get('home_team', {}).get('full_name'),
                'home_team_abbreviation': game.get('home_team', {}).get('abbreviation'),
                'home_team_score': game.get('home_team_score'),
                'visitor_team_id': game.get('visitor_team', {}).get('id'),
                'visitor_team': game.get('visitor_team', {}).get('full_name'),
                'visitor_team_abbreviation': game.get('visitor_team', {}).get('abbreviation'),
                'visitor_team_score': game.get('visitor_team_score'),
            }
            games.append(game_data)

        df = pd.DataFrame(games)

        if not df.empty:
            # Save to CSV
            output_file = self.output_dir / f"nba_games_{start_date}_to_{end_date}.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved {len(df)} games to {output_file}")

        return df

    def get_player_stats(self, player_ids: List[int] = None, season: int = 2023, dates: List[str] = None) -> pd.DataFrame:
        """
        Get player statistics.

        Args:
            player_ids: List of player IDs
            season: Season year
            dates: List of dates to get stats for

        Returns:
            DataFrame with player stats
        """
        print("Fetching player statistics...")

        url = f"{self.balldontlie_base}/stats"
        params = {
            'seasons[]': season,
            'per_page': 100
        }

        if player_ids:
            params['player_ids[]'] = player_ids

        if dates:
            params['dates[]'] = dates

        data = self._make_request(url, params)

        if not data or 'data' not in data:
            return pd.DataFrame()

        stats = []
        for stat in data['data']:
            stat_data = {
                'game_id': stat.get('game', {}).get('id'),
                'game_date': stat.get('game', {}).get('date'),
                'player_id': stat.get('player', {}).get('id'),
                'player_name': f"{stat.get('player', {}).get('first_name')} {stat.get('player', {}).get('last_name')}",
                'team_id': stat.get('team', {}).get('id'),
                'team_name': stat.get('team', {}).get('full_name'),
                'minutes': stat.get('min'),
                'points': stat.get('pts'),
                'rebounds': stat.get('reb'),
                'assists': stat.get('ast'),
                'steals': stat.get('stl'),
                'blocks': stat.get('blk'),
                'turnovers': stat.get('turnover'),
                'field_goals_made': stat.get('fgm'),
                'field_goals_attempted': stat.get('fga'),
                'field_goal_pct': stat.get('fg_pct'),
                'three_pointers_made': stat.get('fg3m'),
                'three_pointers_attempted': stat.get('fg3a'),
                'three_point_pct': stat.get('fg3_pct'),
                'free_throws_made': stat.get('ftm'),
                'free_throws_attempted': stat.get('fta'),
                'free_throw_pct': stat.get('ft_pct'),
                'offensive_rebounds': stat.get('oreb'),
                'defensive_rebounds': stat.get('dreb'),
                'personal_fouls': stat.get('pf'),
            }
            stats.append(stat_data)

        df = pd.DataFrame(stats)

        if not df.empty:
            print(f"Found {len(df)} stat records")

        return df

    def get_season_averages(self, season: int = 2023, player_ids: List[int] = None) -> pd.DataFrame:
        """
        Get season average statistics for players.

        Args:
            season: Season year
            player_ids: List of player IDs (if None, gets top players)

        Returns:
            DataFrame with season averages
        """
        print(f"Fetching season averages for {season}...")

        # If no player_ids provided, get some popular players
        if player_ids is None:
            player_ids = [237, 192, 145, 115, 666, 2544, 140]  # LeBron, KD, Curry, etc.

        all_averages = []

        for player_id in player_ids:
            url = f"{self.balldontlie_base}/season_averages"
            params = {'season': season, 'player_ids[]': [player_id]}

            data = self._make_request(url, params)

            if data and 'data' in data and data['data']:
                avg = data['data'][0]
                avg_data = {
                    'player_id': avg.get('player_id'),
                    'season': avg.get('season'),
                    'games_played': avg.get('games_played'),
                    'minutes_per_game': avg.get('min'),
                    'points_per_game': avg.get('pts'),
                    'rebounds_per_game': avg.get('reb'),
                    'assists_per_game': avg.get('ast'),
                    'steals_per_game': avg.get('stl'),
                    'blocks_per_game': avg.get('blk'),
                    'turnovers_per_game': avg.get('turnover'),
                    'field_goal_pct': avg.get('fg_pct'),
                    'three_point_pct': avg.get('fg3_pct'),
                    'free_throw_pct': avg.get('ft_pct'),
                }
                all_averages.append(avg_data)

            time.sleep(0.6)  # Rate limiting

        df = pd.DataFrame(all_averages)

        if not df.empty:
            output_file = self.output_dir / f"nba_season_averages_{season}.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved season averages for {len(df)} players")

        return df

    def collect_full_nba_data(self, season: int = 2023) -> Dict[str, pd.DataFrame]:
        """
        Collect comprehensive NBA data.

        Args:
            season: Season year

        Returns:
            Dictionary with all NBA data
        """
        print(f"\n{'='*60}")
        print(f"COLLECTING FULL NBA DATA FOR {season}-{season+1} SEASON")
        print(f"{'='*60}\n")

        data = {}

        # 1. Teams
        print("🏀 Step 1: NBA Teams")
        data['teams'] = self.get_nba_teams()

        # 2. Players
        print("\n👥 Step 2: NBA Players")
        data['players'] = self.get_all_nba_players(max_pages=3)  # ~300 players

        # 3. Recent Games
        print("\n📊 Step 3: Recent Games")
        data['games'] = self.get_games(season=season)

        # 4. Season Averages (for top players)
        print("\n📈 Step 4: Season Averages")
        if not data['players'].empty:
            # Get season averages for first 50 players
            top_player_ids = data['players'].head(50)['player_id'].tolist()
            data['season_averages'] = self.get_season_averages(season, top_player_ids)

        print(f"\n{'='*60}")
        print("✓ NBA DATA COLLECTION COMPLETE")
        print(f"{'='*60}")

        # Summary
        print("\nDATA SUMMARY:")
        for key, value in data.items():
            if isinstance(value, pd.DataFrame):
                print(f"  {key}: {len(value)} records")

        return data

    def get_live_scores_thesportsdb(self, league: str = 'NBA') -> pd.DataFrame:
        """
        Get live scores from TheSportsDB (backup source).

        Args:
            league: League name

        Returns:
            DataFrame with live scores
        """
        print(f"Fetching live scores for {league} from TheSportsDB...")

        # NBA league ID in TheSportsDB
        league_id = '4387'

        url = f"{self.thesportsdb_base}/livescore.php?l={league_id}"
        data = self._make_request(url)

        if not data or 'events' not in data or not data['events']:
            print("No live games")
            return pd.DataFrame()

        games = []
        for event in data['events']:
            game = {
                'match_id': event.get('idEvent'),
                'date': event.get('dateEvent'),
                'time': event.get('strTime'),
                'home_team': event.get('strHomeTeam'),
                'away_team': event.get('strAwayTeam'),
                'home_score': event.get('intHomeScore'),
                'away_score': event.get('intAwayScore'),
                'status': event.get('strStatus'),
            }
            games.append(game)

        df = pd.DataFrame(games)
        print(f"Found {len(df)} live games")

        return df


if __name__ == "__main__":
    # Example usage
    api = FreeBasketballAPI()

    # Collect full NBA data
    nba_data = api.collect_full_nba_data(season=2023)

    print("\n" + "="*60)
    print("✓ BASKETBALL DATA COLLECTION COMPLETE!")
    print("="*60)
