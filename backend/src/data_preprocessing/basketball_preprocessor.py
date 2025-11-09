"""Basketball data preprocessing module."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional


class BasketballPreprocessor:
    """Preprocesses basketball data for analysis."""

    def __init__(self, input_dir: str = "data/raw/basketball", output_dir: str = "data/processed/basketball"):
        """
        Initialize basketball preprocessor.

        Args:
            input_dir: Directory containing raw data
            output_dir: Directory to save processed data
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def preprocess_games(self, games_df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess game data.

        Args:
            games_df: Raw game data

        Returns:
            Preprocessed game data
        """
        if games_df.empty:
            return games_df

        # Convert date to datetime
        if 'date' in games_df.columns:
            games_df['date'] = pd.to_datetime(games_df['date'])

        # Calculate game winner
        if 'home_score' in games_df.columns and 'away_score' in games_df.columns:
            games_df['winner'] = games_df.apply(
                lambda row: row['home_team'] if row['home_score'] > row['away_score'] else row['away_team'],
                axis=1
            )
            games_df['margin'] = abs(games_df['home_score'] - games_df['away_score'])
            games_df['total_points'] = games_df['home_score'] + games_df['away_score']

        # Remove duplicates
        if 'game_id' in games_df.columns:
            games_df = games_df.drop_duplicates(subset=['game_id'])

        return games_df

    def preprocess_player_stats(self, player_df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess player statistics.

        Args:
            player_df: Raw player data

        Returns:
            Preprocessed player data with advanced metrics
        """
        if player_df.empty:
            return player_df

        # Fill missing values
        numeric_columns = player_df.select_dtypes(include=[np.number]).columns
        player_df[numeric_columns] = player_df[numeric_columns].fillna(0)

        # Calculate advanced metrics
        if 'field_goal_pct' in player_df.columns:
            # True Shooting Percentage (simplified)
            player_df['true_shooting_pct'] = player_df['field_goal_pct']

        if 'points_per_game' in player_df.columns and 'minutes_per_game' in player_df.columns:
            # Points per 36 minutes
            player_df['points_per_36'] = (player_df['points_per_game'] / player_df['minutes_per_game']) * 36
            player_df['points_per_36'] = player_df['points_per_36'].replace([np.inf, -np.inf], 0)

        if 'assists_per_game' in player_df.columns and 'turnovers_per_game' in player_df.columns:
            # Assist to Turnover Ratio
            player_df['ast_to_ratio'] = player_df['assists_per_game'] / player_df['turnovers_per_game'].replace(0, 1)

        # Player Efficiency Rating (simplified)
        if all(col in player_df.columns for col in ['points_per_game', 'rebounds_per_game', 'assists_per_game', 'steals_per_game', 'blocks_per_game', 'turnovers_per_game']):
            player_df['per'] = (
                player_df['points_per_game'] +
                player_df['rebounds_per_game'] +
                player_df['assists_per_game'] +
                player_df['steals_per_game'] +
                player_df['blocks_per_game'] -
                player_df['turnovers_per_game']
            )

        # Remove duplicates
        if 'player_id' in player_df.columns:
            player_df = player_df.drop_duplicates(subset=['player_id', 'season'])

        return player_df

    def preprocess_team_stats(self, team_df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess team statistics.

        Args:
            team_df: Raw team data

        Returns:
            Preprocessed team data with advanced metrics
        """
        if team_df.empty:
            return team_df

        # Fill missing values
        numeric_columns = team_df.select_dtypes(include=[np.number]).columns
        team_df[numeric_columns] = team_df[numeric_columns].fillna(0)

        # Calculate net rating
        if 'offensive_rating' in team_df.columns and 'defensive_rating' in team_df.columns:
            team_df['net_rating'] = team_df['offensive_rating'] - team_df['defensive_rating']

        # Calculate expected wins based on point differential
        if 'point_diff' in team_df.columns and 'wins' in team_df.columns and 'losses' in team_df.columns:
            total_games = team_df['wins'] + team_df['losses']
            # Pythagorean expectation for basketball
            team_df['expected_wins'] = total_games * (1 / (1 + ((-team_df['point_diff']) / 10) ** 2))

        # Remove duplicates
        if 'team_id' in team_df.columns:
            team_df = team_df.drop_duplicates(subset=['team_id', 'season'])

        return team_df

    def process_all(self, league: str, season: str) -> Dict[str, pd.DataFrame]:
        """
        Process all data for a league and season.

        Args:
            league: League name
            season: Season identifier

        Returns:
            Dictionary of processed DataFrames
        """
        processed_data = {}

        # Process games
        games_file = self.input_dir / f"{league.lower()}_games_{season.replace('/', '_')}.csv"
        if games_file.exists():
            games_df = pd.read_csv(games_file)
            processed_games = self.preprocess_games(games_df)
            output_file = self.output_dir / f"{league.lower()}_games_processed.csv"
            processed_games.to_csv(output_file, index=False)
            processed_data['games'] = processed_games
            print(f"Processed {len(processed_games)} games")

        # Process player stats
        players_file = self.input_dir / f"{league.lower()}_player_stats_{season.replace('/', '_')}.csv"
        if players_file.exists():
            players_df = pd.read_csv(players_file)
            processed_players = self.preprocess_player_stats(players_df)
            output_file = self.output_dir / f"{league.lower()}_players_processed.csv"
            processed_players.to_csv(output_file, index=False)
            processed_data['players'] = processed_players
            print(f"Processed {len(processed_players)} players")

        # Process team stats
        teams_file = self.input_dir / f"{league.lower()}_team_stats_{season.replace('/', '_')}.csv"
        if teams_file.exists():
            teams_df = pd.read_csv(teams_file)
            processed_teams = self.preprocess_team_stats(teams_df)
            output_file = self.output_dir / f"{league.lower()}_teams_processed.csv"
            processed_teams.to_csv(output_file, index=False)
            processed_data['teams'] = processed_teams
            print(f"Processed {len(processed_teams)} teams")

        return processed_data
