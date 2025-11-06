"""
Expected Goals (xG) Calculation Engine
Professional-grade xG model used by top teams and analysts
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ShotContext:
    """Context information for a shot."""
    distance_to_goal: float  # meters
    angle_to_goal: float  # degrees
    shot_type: str  # 'right_foot', 'left_foot', 'header'
    body_part: str  # 'foot', 'head', 'other'
    assist_type: str  # 'through_ball', 'cross', 'set_piece', 'none'
    game_state: str  # 'open_play', 'counter_attack', 'set_piece'
    defender_pressure: str  # 'high', 'medium', 'low'
    goalkeeper_position: str  # 'set', 'off_line', 'out'
    one_on_one: bool = False
    big_chance: bool = False


class ExpectedGoalsEngine:
    """
    Calculate Expected Goals (xG) for shots.

    xG represents the probability that a shot will result in a goal,
    based on historical data and shot characteristics.
    """

    # Base xG values by distance (meters from goal)
    DISTANCE_XG = {
        (0, 6): 0.50,    # Inside 6-yard box
        (6, 11): 0.15,   # Inside penalty area
        (11, 16.5): 0.08,  # Edge of box
        (16.5, 25): 0.03,  # Outside box
        (25, 35): 0.01,  # Long range
        (35, 100): 0.005  # Very long range
    }

    def __init__(self):
        """Initialize xG engine."""
        pass

    def calculate_xg(self, shot: ShotContext) -> Dict:
        """
        Calculate Expected Goals for a shot.

        Args:
            shot: Shot context information

        Returns:
            xG value and breakdown
        """
        # Start with base xG from distance
        base_xg = self._get_distance_xg(shot.distance_to_goal)

        # Apply multipliers based on context
        angle_multiplier = self._get_angle_multiplier(shot.angle_to_goal)
        body_part_multiplier = self._get_body_part_multiplier(shot.body_part)
        assist_multiplier = self._get_assist_multiplier(shot.assist_type)
        pressure_multiplier = self._get_pressure_multiplier(shot.defender_pressure)
        gk_multiplier = self._get_goalkeeper_multiplier(shot.goalkeeper_position)

        # Calculate final xG
        xg = base_xg * angle_multiplier * body_part_multiplier * assist_multiplier * pressure_multiplier * gk_multiplier

        # Bonuses for special situations
        if shot.one_on_one:
            xg *= 1.8
        if shot.big_chance:
            xg *= 1.5
        if shot.game_state == 'counter_attack':
            xg *= 1.2

        # Cap xG at 0.99 (no shot is 100% certain)
        xg = min(xg, 0.99)

        # Classify shot quality
        shot_quality = self._classify_shot_quality(xg)

        return {
            'xg': round(xg, 3),
            'xg_percentage': round(xg * 100, 1),
            'shot_quality': shot_quality,
            'breakdown': {
                'base_xg': round(base_xg, 3),
                'angle_factor': round(angle_multiplier, 2),
                'body_part_factor': round(body_part_multiplier, 2),
                'assist_factor': round(assist_multiplier, 2),
                'pressure_factor': round(pressure_multiplier, 2),
                'goalkeeper_factor': round(gk_multiplier, 2),
            },
            'recommendation': self._get_recommendation(xg, shot),
        }

    def calculate_match_xg(self, shots: List[ShotContext]) -> Dict:
        """
        Calculate team xG for a match.

        Args:
            shots: List of shot contexts

        Returns:
            Match xG statistics
        """
        if not shots:
            return {'total_xg': 0.0, 'shots': 0, 'big_chances': 0}

        total_xg = 0.0
        big_chances = 0
        shot_quality_dist = {'excellent': 0, 'good': 0, 'average': 0, 'poor': 0}

        for shot in shots:
            xg_result = self.calculate_xg(shot)
            total_xg += xg_result['xg']

            if shot.big_chance:
                big_chances += 1

            shot_quality_dist[xg_result['shot_quality']] += 1

        return {
            'total_xg': round(total_xg, 2),
            'shots': len(shots),
            'big_chances': big_chances,
            'average_xg_per_shot': round(total_xg / len(shots), 3),
            'shot_quality_distribution': shot_quality_dist,
            'expected_goals_description': self._describe_xg(total_xg),
        }

    def calculate_xg_performance(self, actual_goals: int, expected_goals: float) -> Dict:
        """
        Analyze performance vs expectation.

        Args:
            actual_goals: Actual goals scored
            expected_goals: Total xG

        Returns:
            Performance analysis
        """
        difference = actual_goals - expected_goals
        percentage_difference = (difference / expected_goals * 100) if expected_goals > 0 else 0

        if difference > 1.5:
            performance = 'CLINICAL - Exceptional finishing'
        elif difference > 0.5:
            performance = 'EFFICIENT - Above expected'
        elif difference > -0.5:
            performance = 'ON_PAR - Meeting expectations'
        elif difference > -1.5:
            performance = 'WASTEFUL - Below expected'
        else:
            performance = 'POOR - Significantly underperforming'

        return {
            'actual_goals': actual_goals,
            'expected_goals': round(expected_goals, 2),
            'difference': round(difference, 2),
            'percentage_difference': round(percentage_difference, 1),
            'performance_rating': performance,
            'conversion_analysis': self._analyze_conversion(actual_goals, expected_goals),
        }

    def _get_distance_xg(self, distance: float) -> float:
        """Get base xG from distance to goal."""
        for (min_dist, max_dist), xg_value in self.DISTANCE_XG.items():
            if min_dist <= distance < max_dist:
                return xg_value
        return 0.005  # Very low for extremely long shots

    def _get_angle_multiplier(self, angle: float) -> float:
        """
        Calculate multiplier based on angle to goal.
        0° = straight on, 90° = from side
        """
        if angle <= 15:
            return 1.3  # Central position
        elif angle <= 30:
            return 1.1  # Good angle
        elif angle <= 45:
            return 1.0  # Moderate angle
        elif angle <= 60:
            return 0.8  # Wide angle
        else:
            return 0.5  # Very wide/tight angle

    def _get_body_part_multiplier(self, body_part: str) -> float:
        """Get multiplier based on body part used."""
        multipliers = {
            'foot': 1.0,
            'head': 0.7,  # Headers generally lower conversion
            'other': 0.5,  # Rare situations
        }
        return multipliers.get(body_part, 1.0)

    def _get_assist_multiplier(self, assist_type: str) -> float:
        """Get multiplier based on assist quality."""
        multipliers = {
            'through_ball': 1.4,  # Usually creates good chances
            'cross': 0.9,  # Headers/volleys are harder
            'cutback': 1.3,  # Often creates good chances
            'set_piece': 0.8,  # More defenders present
            'none': 1.0,  # Individual effort
        }
        return multipliers.get(assist_type, 1.0)

    def _get_pressure_multiplier(self, pressure: str) -> float:
        """Get multiplier based on defender pressure."""
        multipliers = {
            'low': 1.3,  # Unmarked
            'medium': 1.0,  # Normal
            'high': 0.7,  # Heavily marked
        }
        return multipliers.get(pressure, 1.0)

    def _get_goalkeeper_multiplier(self, gk_position: str) -> float:
        """Get multiplier based on goalkeeper positioning."""
        multipliers = {
            'out': 1.5,  # Goalkeeper off line/beaten
            'off_line': 1.2,  # Goalkeeper not set
            'set': 1.0,  # Normal position
        }
        return multipliers.get(gk_position, 1.0)

    def _classify_shot_quality(self, xg: float) -> str:
        """Classify shot quality based on xG."""
        if xg >= 0.35:
            return 'excellent'  # Big chance
        elif xg >= 0.15:
            return 'good'  # Quality chance
        elif xg >= 0.05:
            return 'average'  # Half-chance
        else:
            return 'poor'  # Low probability

    def _get_recommendation(self, xg: float, shot: ShotContext) -> str:
        """Get tactical recommendation based on xG."""
        if xg > 0.5:
            return "Excellent chance - Must score situation"
        elif xg > 0.25:
            return "Good opportunity - Expected to score occasionally"
        elif xg > 0.10:
            return "Half-chance - Worth taking"
        elif shot.distance_to_goal > 25:
            return "Low percentage - Consider passing"
        else:
            return "Difficult chance - Needs precision"

    def _describe_xg(self, xg: float) -> str:
        """Describe total xG value."""
        if xg >= 3.0:
            return "Dominant performance - Created many high-quality chances"
        elif xg >= 2.0:
            return "Strong attacking display - Good chance creation"
        elif xg >= 1.0:
            return "Decent chances created - Expected to score"
        elif xg >= 0.5:
            return "Limited chances - Struggled to create quality opportunities"
        else:
            return "Poor attacking performance - Very few chances"

    def _analyze_conversion(self, goals: int, xg: float) -> str:
        """Analyze conversion efficiency."""
        if xg < 0.5:
            return "Insufficient chances to analyze"

        if goals > xg * 1.5:
            return "Clinical finishing - Exceeded expectations significantly"
        elif goals > xg:
            return "Good finishing - Better than expected"
        elif goals >= xg * 0.8:
            return "Average finishing - Close to expected"
        elif goals >= xg * 0.5:
            return "Poor finishing - Missing clear chances"
        else:
            return "Very poor finishing - Major concern"


class ExpectedAssists:
    """Calculate Expected Assists (xA) - probability a pass leads to a goal."""

    def calculate_xa(self, pass_context: Dict) -> float:
        """
        Calculate Expected Assists for a pass.

        Args:
            pass_context: Dictionary with pass context

        Returns:
            xA value (0-1)
        """
        # Simplified xA calculation
        # In reality, this would use the xG of the resulting shot

        pass_type = pass_context.get('type', 'normal')
        receiver_distance = pass_context.get('receiver_distance_to_goal', 20)
        defender_pressure = pass_context.get('defender_pressure', 'medium')

        # Base xA from pass type
        type_xa = {
            'through_ball': 0.20,
            'cross': 0.10,
            'cutback': 0.25,
            'key_pass': 0.15,
            'normal': 0.05,
        }.get(pass_type, 0.05)

        # Adjust for receiver position
        if receiver_distance < 10:
            type_xa *= 1.5
        elif receiver_distance > 20:
            type_xa *= 0.7

        # Adjust for pressure
        if defender_pressure == 'low':
            type_xa *= 1.3
        elif defender_pressure == 'high':
            type_xa *= 0.7

        return min(type_xa, 0.99)


# Example usage
if __name__ == "__main__":
    engine = ExpectedGoalsEngine()

    # Example shot
    shot = ShotContext(
        distance_to_goal=8.0,
        angle_to_goal=10.0,
        shot_type='right_foot',
        body_part='foot',
        assist_type='through_ball',
        game_state='counter_attack',
        defender_pressure='low',
        goalkeeper_position='off_line',
        one_on_one=True,
        big_chance=True
    )

    result = engine.calculate_xg(shot)
    print(f"xG: {result['xg']} ({result['xg_percentage']}%)")
    print(f"Quality: {result['shot_quality']}")
    print(f"Recommendation: {result['recommendation']}")
