"""
Moneyball Player Valuation Engine
Advanced player value assessment and market inefficiency detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class PlayerValuationEngine:
    """
    Moneyball-style player valuation engine.
    Identifies undervalued players and market inefficiencies.
    """

    def __init__(self, sport: str = 'basketball'):
        """
        Initialize valuation engine.

        Args:
            sport: 'basketball' or 'football'
        """
        self.sport = sport
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

    def calculate_player_value(self, player_stats: Dict) -> Dict:
        """
        Calculate comprehensive player value.

        Args:
            player_stats: Player statistics dictionary

        Returns:
            Value assessment dictionary
        """
        if self.sport == 'basketball':
            return self._calculate_basketball_value(player_stats)
        else:
            return self._calculate_football_value(player_stats)

    def _calculate_basketball_value(self, stats: Dict) -> Dict:
        """Calculate basketball player value (NBA-style)."""

        # Core metrics
        ppg = stats.get('points_per_game', 0)
        rpg = stats.get('rebounds_per_game', 0)
        apg = stats.get('assists_per_game', 0)
        spg = stats.get('steals_per_game', 0)
        bpg = stats.get('blocks_per_game', 0)
        tpg = stats.get('turnovers_per_game', 0)
        fg_pct = stats.get('field_goal_pct', 0)
        three_pct = stats.get('three_point_pct', 0)
        ft_pct = stats.get('free_throw_pct', 0)
        mpg = stats.get('minutes_per_game', 0)

        # Advanced metrics
        per = self._calculate_per(stats)
        ts_pct = self._calculate_true_shooting(stats)
        ws = self._estimate_win_shares(stats)
        vorp = self._estimate_vorp(stats)

        # Value calculation (weighted formula)
        offensive_value = (ppg * 1.0) + (apg * 1.5) + (ts_pct * 50)
        defensive_value = (rpg * 1.0) + (spg * 2.0) + (bpg * 2.0)
        efficiency_value = per * 2.0
        impact_value = (ws * 3.0) + (vorp * 2.0)

        # Penalties
        turnover_penalty = tpg * 1.5
        minutes_factor = min(mpg / 35.0, 1.0)  # Playing time adjustment

        raw_value = (offensive_value + defensive_value + efficiency_value + impact_value - turnover_penalty) * minutes_factor

        # Normalize to 0-100 scale
        normalized_value = min(max(raw_value, 0), 100)

        # Estimated market value (in millions)
        if normalized_value > 90:
            market_value = 40 + (normalized_value - 90) * 2  # Superstar: $40M+
        elif normalized_value > 75:
            market_value = 20 + (normalized_value - 75) * 1.33  # Star: $20-40M
        elif normalized_value > 60:
            market_value = 10 + (normalized_value - 60) * 0.67  # Starter: $10-20M
        elif normalized_value > 40:
            market_value = 3 + (normalized_value - 40) * 0.35  # Role player: $3-10M
        else:
            market_value = 1 + (normalized_value / 40) * 2  # Bench: $1-3M

        return {
            'player_value_score': round(normalized_value, 2),
            'estimated_market_value_millions': round(market_value, 2),
            'value_tier': self._get_value_tier(normalized_value),
            'offensive_value': round(offensive_value, 2),
            'defensive_value': round(defensive_value, 2),
            'efficiency_value': round(efficiency_value, 2),
            'impact_metrics': {
                'per': round(per, 2),
                'true_shooting_pct': round(ts_pct, 3),
                'win_shares': round(ws, 2),
                'vorp': round(vorp, 2),
            },
            'strengths': self._identify_strengths(stats),
            'weaknesses': self._identify_weaknesses(stats),
        }

    def _calculate_football_value(self, stats: Dict) -> Dict:
        """Calculate football player value."""

        # Core metrics
        goals = stats.get('goals', 0)
        assists = stats.get('assists', 0)
        minutes = stats.get('minutes_played', 0)
        matches = stats.get('matches_played', 0)

        # Per 90 metrics
        per_90 = minutes / 90.0 if minutes > 0 else 0
        goals_per_90 = goals / per_90 if per_90 > 0 else 0
        assists_per_90 = assists / per_90 if per_90 > 0 else 0

        # Advanced metrics
        xg = stats.get('expected_goals', goals * 0.8)  # Estimate if not available
        xa = stats.get('expected_assists', assists * 0.8)

        # Value calculation
        offensive_value = (goals_per_90 * 10) + (assists_per_90 * 7) + (xg * 0.5)
        creative_value = (xa * 0.5) + (assists_per_90 * 5)

        raw_value = offensive_value + creative_value
        normalized_value = min(max(raw_value * 3, 0), 100)

        # Market value estimation
        if normalized_value > 90:
            market_value = 80 + (normalized_value - 90) * 4  # World class: €80M+
        elif normalized_value > 75:
            market_value = 40 + (normalized_value - 75) * 2.67  # Star: €40-80M
        elif normalized_value > 60:
            market_value = 15 + (normalized_value - 60) * 1.67  # Quality: €15-40M
        elif normalized_value > 40:
            market_value = 5 + (normalized_value - 40) * 0.5  # Squad player: €5-15M
        else:
            market_value = 1 + (normalized_value / 40) * 4  # Backup: €1-5M

        return {
            'player_value_score': round(normalized_value, 2),
            'estimated_market_value_millions': round(market_value, 2),
            'value_tier': self._get_value_tier(normalized_value),
            'goals_per_90': round(goals_per_90, 2),
            'assists_per_90': round(assists_per_90, 2),
            'expected_goals': round(xg, 2),
            'expected_assists': round(xa, 2),
        }

    def find_undervalued_players(self, players_df: pd.DataFrame, budget: float = 20.0) -> pd.DataFrame:
        """
        Find undervalued players (Moneyball approach).

        Args:
            players_df: DataFrame with player statistics
            budget: Budget in millions

        Returns:
            DataFrame with undervalued players ranked by value/cost ratio
        """
        undervalued = []

        for idx, player in players_df.iterrows():
            value_assessment = self.calculate_player_value(player.to_dict())

            estimated_value = value_assessment['estimated_market_value_millions']
            actual_cost = player.get('market_value_millions', estimated_value)

            # Calculate value ratio (higher is better)
            value_ratio = estimated_value / max(actual_cost, 0.5)

            # Find players below budget with positive value ratio
            if actual_cost <= budget and value_ratio > 1.1:  # At least 10% undervalued
                undervalued.append({
                    'player_name': player.get('player_name', 'Unknown'),
                    'team': player.get('team', 'Unknown'),
                    'position': player.get('position', 'Unknown'),
                    'age': player.get('age', 0),
                    'estimated_value': estimated_value,
                    'actual_cost': actual_cost,
                    'value_ratio': value_ratio,
                    'savings_millions': estimated_value - actual_cost,
                    'player_value_score': value_assessment['player_value_score'],
                    'value_tier': value_assessment['value_tier'],
                    'moneyball_rating': 'EXCELLENT' if value_ratio > 1.5 else 'GOOD',
                })

        df = pd.DataFrame(undervalued)
        if not df.empty:
            df = df.sort_values('value_ratio', ascending=False)

        return df

    def compare_players(self, player1_stats: Dict, player2_stats: Dict) -> Dict:
        """
        Compare two players head-to-head.

        Args:
            player1_stats: First player statistics
            player2_stats: Second player statistics

        Returns:
            Comparison analysis
        """
        value1 = self.calculate_player_value(player1_stats)
        value2 = self.calculate_player_value(player2_stats)

        return {
            'player1': {
                'name': player1_stats.get('player_name', 'Player 1'),
                'value_score': value1['player_value_score'],
                'estimated_value': value1['estimated_market_value_millions'],
                'tier': value1['value_tier'],
            },
            'player2': {
                'name': player2_stats.get('player_name', 'Player 2'),
                'value_score': value2['player_value_score'],
                'estimated_value': value2['estimated_market_value_millions'],
                'tier': value2['value_tier'],
            },
            'winner': 'player1' if value1['player_value_score'] > value2['player_value_score'] else 'player2',
            'value_difference': abs(value1['player_value_score'] - value2['player_value_score']),
            'cost_difference': abs(value1['estimated_market_value_millions'] - value2['estimated_market_value_millions']),
            'recommendation': self._generate_comparison_recommendation(value1, value2),
        }

    def _calculate_per(self, stats: Dict) -> float:
        """Calculate Player Efficiency Rating."""
        ppg = stats.get('points_per_game', 0)
        rpg = stats.get('rebounds_per_game', 0)
        apg = stats.get('assists_per_game', 0)
        spg = stats.get('steals_per_game', 0)
        bpg = stats.get('blocks_per_game', 0)
        tpg = stats.get('turnovers_per_game', 0)
        fg_pct = stats.get('field_goal_pct', 0.45)

        per = (ppg + rpg + apg + spg + bpg - tpg) * fg_pct * 0.8
        return max(per, 0)

    def _calculate_true_shooting(self, stats: Dict) -> float:
        """Calculate True Shooting Percentage."""
        ppg = stats.get('points_per_game', 0)
        fga = ppg / stats.get('field_goal_pct', 0.45) if stats.get('field_goal_pct', 0) > 0 else 15
        fta = ppg * 0.25  # Estimate

        if fga + (0.44 * fta) > 0:
            return ppg / (2 * (fga + 0.44 * fta))
        return 0.5

    def _estimate_win_shares(self, stats: Dict) -> float:
        """Estimate Win Shares contribution."""
        ppg = stats.get('points_per_game', 0)
        rpg = stats.get('rebounds_per_game', 0)
        apg = stats.get('assists_per_game', 0)
        per = self._calculate_per(stats)

        ws = (ppg * 0.1 + rpg * 0.15 + apg * 0.2 + per * 0.05) * 0.6
        return max(ws, 0)

    def _estimate_vorp(self, stats: Dict) -> float:
        """Estimate Value Over Replacement Player."""
        per = self._calculate_per(stats)
        mpg = stats.get('minutes_per_game', 0)

        # Simplified VORP calculation
        vorp = ((per - 15) * mpg * 0.05)
        return max(vorp, -2)

    def _get_value_tier(self, value_score: float) -> str:
        """Get value tier classification."""
        if value_score >= 90:
            return 'SUPERSTAR'
        elif value_score >= 75:
            return 'STAR'
        elif value_score >= 60:
            return 'STARTER'
        elif value_score >= 40:
            return 'ROLE_PLAYER'
        else:
            return 'BENCH'

    def _identify_strengths(self, stats: Dict) -> List[str]:
        """Identify player strengths."""
        strengths = []

        if stats.get('points_per_game', 0) > 20:
            strengths.append('Elite Scorer')
        if stats.get('assists_per_game', 0) > 7:
            strengths.append('Elite Playmaker')
        if stats.get('rebounds_per_game', 0) > 10:
            strengths.append('Elite Rebounder')
        if stats.get('field_goal_pct', 0) > 0.50:
            strengths.append('Efficient Shooter')
        if stats.get('three_point_pct', 0) > 0.40:
            strengths.append('3-Point Specialist')
        if stats.get('steals_per_game', 0) + stats.get('blocks_per_game', 0) > 2:
            strengths.append('Strong Defender')

        return strengths if strengths else ['Well-Rounded']

    def _identify_weaknesses(self, stats: Dict) -> List[str]:
        """Identify player weaknesses."""
        weaknesses = []

        if stats.get('turnovers_per_game', 0) > 3:
            weaknesses.append('High Turnovers')
        if stats.get('field_goal_pct', 0) < 0.40:
            weaknesses.append('Low Shooting Efficiency')
        if stats.get('free_throw_pct', 0) < 0.70:
            weaknesses.append('Poor Free Throw Shooting')
        if stats.get('minutes_per_game', 0) < 20:
            weaknesses.append('Limited Playing Time')

        return weaknesses if weaknesses else ['No Major Weaknesses']

    def _generate_comparison_recommendation(self, value1: Dict, value2: Dict) -> str:
        """Generate recommendation for player comparison."""
        diff = abs(value1['player_value_score'] - value2['player_value_score'])
        cost_diff = abs(value1['estimated_market_value_millions'] - value2['estimated_market_value_millions'])

        if diff < 5:
            return "Very close in value. Consider team fit and cost."
        elif cost_diff > 20:
            return "Significant cost difference. Analyze value per dollar."
        elif value1['player_value_score'] > value2['player_value_score']:
            return "Player 1 offers superior value. Strong recommendation."
        else:
            return "Player 2 offers superior value. Strong recommendation."
