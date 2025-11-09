"""Basketball-specific analysis module."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class BasketballAnalysis:
    """Advanced basketball analytics."""

    def __init__(self, games_df: pd.DataFrame = None, player_df: pd.DataFrame = None, team_df: pd.DataFrame = None):
        """
        Initialize basketball analysis.

        Args:
            games_df: DataFrame with game data
            player_df: DataFrame with player statistics
            team_df: DataFrame with team statistics
        """
        self.games_df = games_df
        self.player_df = player_df
        self.team_df = team_df

    def calculate_player_efficiency_rating(self, player_stats: Dict) -> float:
        """
        Calculate Player Efficiency Rating (PER).

        PER = (Points + Rebounds + Assists + Steals + Blocks - Missed FG - Missed FT - Turnovers) / Games

        Args:
            player_stats: Dictionary with player statistics

        Returns:
            PER value
        """
        points = player_stats.get('points_per_game', 0)
        rebounds = player_stats.get('rebounds_per_game', 0)
        assists = player_stats.get('assists_per_game', 0)
        steals = player_stats.get('steals_per_game', 0)
        blocks = player_stats.get('blocks_per_game', 0)
        turnovers = player_stats.get('turnovers_per_game', 0)
        fg_pct = player_stats.get('field_goal_pct', 0.45)

        # Simplified PER calculation
        per = (points + rebounds + assists + steals + blocks - turnovers) * fg_pct
        return round(per, 2)

    def calculate_true_shooting_percentage(self, points: float, fga: float, fta: float) -> float:
        """
        Calculate True Shooting Percentage.

        TS% = Points / (2 * (FGA + 0.44 * FTA))

        Args:
            points: Total points scored
            fga: Field goal attempts
            fta: Free throw attempts

        Returns:
            True shooting percentage
        """
        if fga + (0.44 * fta) == 0:
            return 0.0

        ts_pct = points / (2 * (fga + 0.44 * fta))
        return round(ts_pct, 3)

    def calculate_effective_field_goal_percentage(self, fg: float, three_pm: float, fga: float) -> float:
        """
        Calculate Effective Field Goal Percentage.

        eFG% = (FG + 0.5 * 3PM) / FGA

        Args:
            fg: Field goals made
            three_pm: Three-pointers made
            fga: Field goal attempts

        Returns:
            Effective field goal percentage
        """
        if fga == 0:
            return 0.0

        efg_pct = (fg + 0.5 * three_pm) / fga
        return round(efg_pct, 3)

    def calculate_usage_rate(self, fga: float, fta: float, tov: float, team_fga: float, team_fta: float, team_tov: float, minutes: float, team_minutes: float) -> float:
        """
        Calculate player usage rate.

        Usage% = 100 * ((FGA + 0.44 * FTA + TOV) * (Team Minutes / 5)) / (Minutes * (Team FGA + 0.44 * Team FTA + Team TOV))

        Args:
            fga: Player field goal attempts
            fta: Player free throw attempts
            tov: Player turnovers
            team_fga: Team field goal attempts
            team_fta: Team free throw attempts
            team_tov: Team turnovers
            minutes: Player minutes
            team_minutes: Team total minutes

        Returns:
            Usage rate percentage
        """
        if minutes == 0:
            return 0.0

        numerator = (fga + 0.44 * fta + tov) * (team_minutes / 5)
        denominator = minutes * (team_fga + 0.44 * team_fta + team_tov)

        if denominator == 0:
            return 0.0

        usage = 100 * (numerator / denominator)
        return round(usage, 2)

    def analyze_player_performance(self, player_name: str) -> Dict:
        """
        Comprehensive player performance analysis.

        Args:
            player_name: Name of the player

        Returns:
            Dictionary with performance metrics
        """
        if self.player_df is None:
            return {}

        player_data = self.player_df[self.player_df['player_name'] == player_name]

        if player_data.empty:
            return {}

        player = player_data.iloc[0]

        analysis = {
            'player_name': player_name,
            'team': player.get('team', 'N/A'),
            'games_played': player.get('games_played', 0),
            'minutes_per_game': player.get('minutes_per_game', 0),
            'scoring': {
                'points_per_game': player.get('points_per_game', 0),
                'field_goal_pct': player.get('field_goal_pct', 0),
                'three_point_pct': player.get('three_point_pct', 0),
                'free_throw_pct': player.get('free_throw_pct', 0),
            },
            'rebounding': {
                'rebounds_per_game': player.get('rebounds_per_game', 0),
            },
            'playmaking': {
                'assists_per_game': player.get('assists_per_game', 0),
                'turnovers_per_game': player.get('turnovers_per_game', 0),
                'assist_to_turnover_ratio': round(player.get('assists_per_game', 0) / max(player.get('turnovers_per_game', 1), 1), 2)
            },
            'defense': {
                'steals_per_game': player.get('steals_per_game', 0),
                'blocks_per_game': player.get('blocks_per_game', 0),
            },
            'advanced_metrics': {
                'plus_minus': player.get('plus_minus', 0),
                'per': self.calculate_player_efficiency_rating(player.to_dict()),
            }
        }

        return analysis

    def analyze_team_performance(self, team_name: str) -> Dict:
        """
        Comprehensive team performance analysis.

        Args:
            team_name: Name of the team

        Returns:
            Dictionary with team metrics
        """
        if self.team_df is None:
            return {}

        team_data = self.team_df[self.team_df['team_name'] == team_name]

        if team_data.empty:
            return {}

        team = team_data.iloc[0]

        analysis = {
            'team_name': team_name,
            'record': {
                'wins': team.get('wins', 0),
                'losses': team.get('losses', 0),
                'win_percentage': team.get('win_pct', 0),
            },
            'offense': {
                'points_per_game': team.get('points_per_game', 0),
                'offensive_rating': team.get('offensive_rating', 0),
            },
            'defense': {
                'points_allowed': team.get('points_allowed', 0),
                'defensive_rating': team.get('defensive_rating', 0),
            },
            'pace': team.get('pace', 0),
            'point_differential': team.get('point_diff', 0),
            'net_rating': round(team.get('offensive_rating', 0) - team.get('defensive_rating', 0), 2)
        }

        return analysis

    def get_top_players(self, metric: str = 'points_per_game', top_n: int = 10) -> pd.DataFrame:
        """
        Get top players by a specific metric.

        Args:
            metric: Metric to rank by
            top_n: Number of top players to return

        Returns:
            DataFrame with top players
        """
        if self.player_df is None:
            return pd.DataFrame()

        if metric not in self.player_df.columns:
            return pd.DataFrame()

        return self.player_df.nlargest(top_n, metric)[['player_name', 'team', metric]]

    def get_team_rankings(self, metric: str = 'win_pct') -> pd.DataFrame:
        """
        Get team rankings by a specific metric.

        Args:
            metric: Metric to rank by

        Returns:
            DataFrame with team rankings
        """
        if self.team_df is None:
            return pd.DataFrame()

        if metric not in self.team_df.columns:
            return pd.DataFrame()

        ranked = self.team_df.sort_values(by=metric, ascending=False).reset_index(drop=True)
        ranked['rank'] = ranked.index + 1
        return ranked[['rank', 'team_name', metric]]

    def predict_game_outcome(self, team1: str, team2: str) -> Dict:
        """
        Predict game outcome based on team statistics.

        Args:
            team1: First team name
            team2: Second team name

        Returns:
            Prediction dictionary
        """
        if self.team_df is None:
            return {}

        team1_data = self.team_df[self.team_df['team_name'] == team1]
        team2_data = self.team_df[self.team_df['team_name'] == team2]

        if team1_data.empty or team2_data.empty:
            return {}

        team1_stats = team1_data.iloc[0]
        team2_stats = team2_data.iloc[0]

        # Simple prediction based on net rating and win percentage
        team1_rating = (team1_stats.get('offensive_rating', 0) - team1_stats.get('defensive_rating', 0)) * 0.6 + team1_stats.get('win_pct', 0) * 40
        team2_rating = (team2_stats.get('offensive_rating', 0) - team2_stats.get('defensive_rating', 0)) * 0.6 + team2_stats.get('win_pct', 0) * 40

        total_rating = team1_rating + team2_rating
        team1_win_prob = team1_rating / total_rating if total_rating > 0 else 0.5

        prediction = {
            'team1': team1,
            'team2': team2,
            'team1_win_probability': round(team1_win_prob, 3),
            'team2_win_probability': round(1 - team1_win_prob, 3),
            'predicted_winner': team1 if team1_win_prob > 0.5 else team2,
            'confidence': round(abs(team1_win_prob - 0.5) * 2, 3)
        }

        return prediction

    def generate_league_summary(self) -> Dict:
        """
        Generate comprehensive league summary.

        Returns:
            Dictionary with league statistics
        """
        summary = {
            'total_teams': len(self.team_df) if self.team_df is not None else 0,
            'total_players': len(self.player_df) if self.player_df is not None else 0,
            'total_games': len(self.games_df) if self.games_df is not None else 0,
        }

        if self.player_df is not None and not self.player_df.empty:
            summary['scoring_leader'] = self.player_df.loc[self.player_df['points_per_game'].idxmax(), 'player_name']
            summary['assist_leader'] = self.player_df.loc[self.player_df['assists_per_game'].idxmax(), 'player_name']
            summary['rebound_leader'] = self.player_df.loc[self.player_df['rebounds_per_game'].idxmax(), 'player_name']
            summary['avg_points_per_game'] = round(self.player_df['points_per_game'].mean(), 2)

        if self.team_df is not None and not self.team_df.empty:
            summary['best_team'] = self.team_df.loc[self.team_df['win_pct'].idxmax(), 'team_name']
            summary['highest_scoring_team'] = self.team_df.loc[self.team_df['points_per_game'].idxmax(), 'team_name']
            summary['best_defense'] = self.team_df.loc[self.team_df['defensive_rating'].idxmin(), 'team_name']

        return summary
