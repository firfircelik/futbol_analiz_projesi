"""
Opta Performance Index - Professional Player Rating System
Used by Premier League teams, scouts, and analysts
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    """Core performance metrics for Opta Index calculation."""
    # Offensive actions
    goals: int = 0
    assists: int = 0
    shots: int = 0
    shots_on_target: int = 0
    key_passes: int = 0
    successful_dribbles: int = 0

    # Passing
    passes_attempted: int = 0
    passes_completed: int = 0
    pass_accuracy: float = 0.0
    progressive_passes: int = 0

    # Defensive actions
    tackles: int = 0
    interceptions: int = 0
    clearances: int = 0
    blocks: int = 0

    # Possession
    touches: int = 0
    possession_won: int = 0
    possession_lost: int = 0

    # Discipline
    fouls_committed: int = 0
    fouls_won: int = 0
    yellow_cards: int = 0
    red_cards: int = 0

    # Context
    minutes_played: int = 90
    team_goals_for: int = 0
    team_goals_against: int = 0


class OptaPerformanceIndex:
    """
    Calculate Opta-style Performance Index.

    The Opta Index is a comprehensive player rating system that considers:
    - Offensive contributions
    - Defensive actions
    - Passing efficiency
    - Tactical discipline
    - Position-specific weights
    """

    # Position weights for different actions
    POSITION_WEIGHTS = {
        'GK': {
            'saves': 3.0, 'clean_sheet': 5.0, 'goals_conceded': -2.0,
            'distribution': 1.0, 'sweeper_actions': 2.0
        },
        'DEF': {
            'tackles': 2.5, 'interceptions': 2.5, 'clearances': 1.5,
            'blocks': 2.0, 'clean_sheet': 4.0, 'goals': 6.0, 'assists': 3.0
        },
        'MID': {
            'passes_completed': 0.05, 'key_passes': 3.0, 'assists': 4.0,
            'goals': 5.0, 'tackles': 2.0, 'interceptions': 2.0,
            'progressive_passes': 0.5
        },
        'FWD': {
            'goals': 5.0, 'assists': 3.5, 'shots_on_target': 1.5,
            'key_passes': 2.0, 'successful_dribbles': 1.0
        }
    }

    def __init__(self):
        """Initialize Opta Performance Index calculator."""
        self.base_score = 30.0  # Starting score for all players

    def calculate_index(self, metrics: PerformanceMetrics, position: str = 'MID') -> Dict:
        """
        Calculate comprehensive Opta Performance Index.

        Args:
            metrics: Player performance metrics
            position: Player position (GK, DEF, MID, FWD)

        Returns:
            Dictionary with index score and breakdown
        """
        position = position.upper()
        if position not in self.POSITION_WEIGHTS:
            position = 'MID'

        # Base score
        total_score = self.base_score
        breakdown = {}

        # 1. Offensive contributions
        offensive_score = self._calculate_offensive_score(metrics, position)
        total_score += offensive_score
        breakdown['offensive'] = offensive_score

        # 2. Defensive contributions
        defensive_score = self._calculate_defensive_score(metrics, position)
        total_score += defensive_score
        breakdown['defensive'] = defensive_score

        # 3. Passing quality
        passing_score = self._calculate_passing_score(metrics, position)
        total_score += passing_score
        breakdown['passing'] = passing_score

        # 4. Possession management
        possession_score = self._calculate_possession_score(metrics)
        total_score += possession_score
        breakdown['possession'] = possession_score

        # 5. Discipline penalties
        discipline_penalty = self._calculate_discipline_penalty(metrics)
        total_score += discipline_penalty
        breakdown['discipline'] = discipline_penalty

        # 6. Playing time adjustment
        time_factor = min(metrics.minutes_played / 90.0, 1.0)
        total_score *= time_factor

        # Normalize to 0-100 scale (Opta typically uses 0-100+)
        final_index = max(min(total_score, 100), 0)

        return {
            'opta_index': round(final_index, 1),
            'rating': self._get_rating(final_index),
            'breakdown': {k: round(v, 2) for k, v in breakdown.items()},
            'percentile': self._calculate_percentile(final_index),
            'performance_level': self._get_performance_level(final_index),
        }

    def _calculate_offensive_score(self, m: PerformanceMetrics, position: str) -> float:
        """Calculate offensive contribution score."""
        weights = self.POSITION_WEIGHTS[position]
        score = 0.0

        # Goals (most important)
        if 'goals' in weights:
            score += m.goals * weights['goals']

        # Assists
        if 'assists' in weights:
            score += m.assists * weights['assists']

        # Shots quality
        if 'shots_on_target' in weights:
            score += m.shots_on_target * weights['shots_on_target']

        # Chance creation
        if 'key_passes' in weights:
            score += m.key_passes * weights['key_passes']

        # Dribbling
        if 'successful_dribbles' in weights:
            score += m.successful_dribbles * weights['successful_dribbles']

        return score

    def _calculate_defensive_score(self, m: PerformanceMetrics, position: str) -> float:
        """Calculate defensive contribution score."""
        weights = self.POSITION_WEIGHTS[position]
        score = 0.0

        if 'tackles' in weights:
            score += m.tackles * weights['tackles']

        if 'interceptions' in weights:
            score += m.interceptions * weights['interceptions']

        if 'clearances' in weights:
            score += m.clearances * weights['clearances']

        if 'blocks' in weights:
            score += m.blocks * weights['blocks']

        # Clean sheet bonus (if no goals conceded)
        if 'clean_sheet' in weights and m.team_goals_against == 0:
            score += weights['clean_sheet']

        return score

    def _calculate_passing_score(self, m: PerformanceMetrics, position: str) -> float:
        """Calculate passing quality score."""
        weights = self.POSITION_WEIGHTS[position]
        score = 0.0

        # Pass completion bonus
        if m.passes_attempted > 0:
            pass_accuracy = m.passes_completed / m.passes_attempted

            if 'passes_completed' in weights:
                score += m.passes_completed * weights['passes_completed']

            # Accuracy bonus (>85% is excellent)
            if pass_accuracy > 0.85:
                score += 2.0
            elif pass_accuracy > 0.75:
                score += 1.0

        # Progressive passes (advancing the ball)
        if 'progressive_passes' in weights:
            score += m.progressive_passes * weights['progressive_passes']

        return score

    def _calculate_possession_score(self, m: PerformanceMetrics) -> float:
        """Calculate possession management score."""
        score = 0.0

        # Reward winning possession
        score += m.possession_won * 0.5

        # Penalize losing possession carelessly
        score -= m.possession_lost * 0.3

        return score

    def _calculate_discipline_penalty(self, m: PerformanceMetrics) -> float:
        """Calculate discipline penalties."""
        penalty = 0.0

        # Yellow card penalty
        penalty -= m.yellow_cards * 2.0

        # Red card heavy penalty
        penalty -= m.red_cards * 10.0

        # Excessive fouls
        if m.fouls_committed > 3:
            penalty -= (m.fouls_committed - 3) * 0.5

        return penalty

    def _get_rating(self, index: float) -> str:
        """Convert index to rating."""
        if index >= 80:
            return 'EXCEPTIONAL'
        elif index >= 70:
            return 'EXCELLENT'
        elif index >= 60:
            return 'GOOD'
        elif index >= 50:
            return 'AVERAGE'
        elif index >= 40:
            return 'BELOW_AVERAGE'
        else:
            return 'POOR'

    def _calculate_percentile(self, index: float) -> int:
        """Estimate percentile ranking (0-100)."""
        # Simplified percentile based on normal distribution
        # Average player = 50th percentile (index ~55)
        percentile = int((index / 100) * 100)
        return max(min(percentile, 99), 1)

    def _get_performance_level(self, index: float) -> str:
        """Get performance level classification."""
        if index >= 75:
            return 'WORLD_CLASS'
        elif index >= 65:
            return 'TOP_LEVEL'
        elif index >= 55:
            return 'PROFESSIONAL'
        elif index >= 45:
            return 'DEVELOPING'
        else:
            return 'NEEDS_IMPROVEMENT'


class OptaBasketballIndex:
    """Basketball version of Opta Performance Index."""

    def __init__(self):
        """Initialize basketball index calculator."""
        self.base_score = 30.0

    def calculate_index(self, stats: Dict) -> Dict:
        """
        Calculate basketball performance index.

        Args:
            stats: Player statistics dictionary

        Returns:
            Performance index and breakdown
        """
        # Core stats
        ppg = stats.get('points_per_game', 0)
        rpg = stats.get('rebounds_per_game', 0)
        apg = stats.get('assists_per_game', 0)
        spg = stats.get('steals_per_game', 0)
        bpg = stats.get('blocks_per_game', 0)
        tpg = stats.get('turnovers_per_game', 0)

        # Efficiency
        fg_pct = stats.get('field_goal_pct', 0)
        three_pct = stats.get('three_point_pct', 0)
        ft_pct = stats.get('free_throw_pct', 0)

        # Calculate weighted score
        scoring_contribution = ppg * 1.5
        playmaking_contribution = apg * 2.0
        rebounding_contribution = rpg * 1.2
        defensive_contribution = (spg + bpg) * 2.5

        # Efficiency bonuses
        efficiency_bonus = (fg_pct * 20) + (three_pct * 15) + (ft_pct * 10)

        # Turnover penalty
        turnover_penalty = tpg * 2.0

        # Total index
        total = (
            self.base_score +
            scoring_contribution +
            playmaking_contribution +
            rebounding_contribution +
            defensive_contribution +
            efficiency_bonus -
            turnover_penalty
        )

        final_index = max(min(total, 100), 0)

        return {
            'opta_index': round(final_index, 1),
            'rating': self._get_rating(final_index),
            'breakdown': {
                'scoring': round(scoring_contribution, 2),
                'playmaking': round(playmaking_contribution, 2),
                'rebounding': round(rebounding_contribution, 2),
                'defense': round(defensive_contribution, 2),
                'efficiency': round(efficiency_bonus, 2),
            },
            'performance_level': self._get_performance_level(final_index),
        }

    def _get_rating(self, index: float) -> str:
        """Convert index to rating."""
        if index >= 80:
            return 'MVP_CALIBER'
        elif index >= 70:
            return 'ALL_STAR'
        elif index >= 60:
            return 'STARTER'
        elif index >= 50:
            return 'ROTATION'
        else:
            return 'BENCH'

    def _get_performance_level(self, index: float) -> str:
        """Get performance level."""
        if index >= 75:
            return 'ELITE'
        elif index >= 65:
            return 'VERY_GOOD'
        elif index >= 55:
            return 'GOOD'
        elif index >= 45:
            return 'AVERAGE'
        else:
            return 'BELOW_AVERAGE'


def calculate_team_opta_index(player_indexes: List[Dict]) -> Dict:
    """
    Calculate team-level Opta Index from player indexes.

    Args:
        player_indexes: List of player index dictionaries

    Returns:
        Team index and analysis
    """
    if not player_indexes:
        return {}

    # Calculate team average
    team_index = np.mean([p['opta_index'] for p in player_indexes])

    # Top performers
    top_3 = sorted(player_indexes, key=lambda x: x['opta_index'], reverse=True)[:3]

    # Consistency (standard deviation)
    consistency = np.std([p['opta_index'] for p in player_indexes])

    return {
        'team_opta_index': round(team_index, 1),
        'team_rating': _get_team_rating(team_index),
        'top_performers': [p.get('player_name', 'Unknown') for p in top_3],
        'consistency_score': round(100 - consistency, 1),  # Higher is better
        'depth_analysis': 'STRONG' if consistency < 10 else 'VARIABLE',
    }


def _get_team_rating(index: float) -> str:
    """Get team rating from index."""
    if index >= 70:
        return 'CHAMPIONSHIP_CONTENDER'
    elif index >= 60:
        return 'PLAYOFF_TEAM'
    elif index >= 50:
        return 'MID_TABLE'
    else:
        return 'STRUGGLING'
