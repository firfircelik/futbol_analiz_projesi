"""
Team Fit Analysis System
Determines which players are perfect for your team based on:
- Statistical performance fit
- Tactical compatibility
- Personality and mentality
- Team chemistry
- Cultural adaptation
- Budget alignment
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PlayingStyle(Enum):
    """Team playing style classifications."""
    POSSESSION_BASED = "possession_based"
    COUNTER_ATTACK = "counter_attack"
    HIGH_PRESS = "high_press"
    DEFENSIVE = "defensive"
    DIRECT = "direct"
    WING_PLAY = "wing_play"
    THROUGH_MIDDLE = "through_middle"


class Personality(Enum):
    """Player personality types."""
    LEADER = "leader"
    PROFESSIONAL = "professional"
    AMBITIOUS = "ambitious"
    TEAM_PLAYER = "team_player"
    MAVERICK = "maverick"
    DRIVEN = "driven"
    BALANCED = "balanced"
    TEMPERAMENTAL = "temperamental"


class WorkRate(Enum):
    """Player work rate levels."""
    HIGH_HIGH = "high_high"
    HIGH_MEDIUM = "high_medium"
    MEDIUM_HIGH = "medium_high"
    MEDIUM_MEDIUM = "medium_medium"
    LOW_HIGH = "low_high"


@dataclass
class TeamProfile:
    """Team profile for fit analysis."""
    team_name: str
    league: str
    playing_style: PlayingStyle
    formation: str
    average_age: float
    budget_millions: float

    # Team needs
    priority_positions: List[str]  # ['ST', 'CAM', 'LW']
    desired_traits: List[str]  # ['pace', 'dribbling', 'leadership']

    # Team characteristics
    average_player_value: float
    team_personality: str  # 'aggressive', 'disciplined', 'creative'
    preferred_foot: Optional[str] = None  # 'right', 'left', 'both'
    language: str = 'english'

    # Tactical requirements
    requires_pace: bool = False
    requires_physicality: bool = False
    requires_technique: bool = False
    requires_experience: bool = False

    # Squad gaps
    missing_attributes: List[str] = None


@dataclass
class PlayerProfile:
    """Player profile for fit analysis."""
    player_name: str
    age: int
    position: str
    nationality: str
    current_team: str
    market_value_millions: float

    # Performance stats
    opta_index: float
    goals: int = 0
    assists: int = 0
    matches_played: int = 0

    # Physical attributes (0-100)
    pace: int = 70
    strength: int = 70
    stamina: int = 70

    # Technical attributes (0-100)
    dribbling: int = 70
    passing: int = 70
    shooting: int = 70
    defending: int = 70

    # Mental attributes (0-100)
    work_rate: int = 70
    decision_making: int = 70
    composure: int = 70
    leadership: int = 50

    # Personality
    personality_type: Personality = Personality.BALANCED
    temperament: str = 'calm'  # 'calm', 'aggressive', 'volatile'
    professionalism: int = 80

    # Other
    preferred_foot: str = 'right'
    languages: List[str] = None
    injury_proneness: str = 'low'  # 'low', 'medium', 'high'
    contract_expiry_years: float = 2.0


class TeamFitAnalyzer:
    """
    Analyze how well a player fits a specific team.
    Used by scouts and managers for transfer decisions.
    """

    def __init__(self):
        """Initialize team fit analyzer."""
        pass

    def analyze_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """
        Comprehensive team fit analysis.

        Args:
            player: Player profile
            team: Team profile

        Returns:
            Complete fit analysis with scores and recommendations
        """
        # Calculate individual fit components
        statistical_fit = self._calculate_statistical_fit(player, team)
        tactical_fit = self._calculate_tactical_fit(player, team)
        personality_fit = self._calculate_personality_fit(player, team)
        chemistry_fit = self._calculate_chemistry_fit(player, team)
        cultural_fit = self._calculate_cultural_fit(player, team)
        budget_fit = self._calculate_budget_fit(player, team)
        age_fit = self._calculate_age_fit(player, team)

        # Calculate overall fit score (weighted average)
        weights = {
            'statistical': 0.25,
            'tactical': 0.20,
            'personality': 0.15,
            'chemistry': 0.15,
            'cultural': 0.10,
            'budget': 0.10,
            'age': 0.05,
        }

        overall_score = (
            statistical_fit['score'] * weights['statistical'] +
            tactical_fit['score'] * weights['tactical'] +
            personality_fit['score'] * weights['personality'] +
            chemistry_fit['score'] * weights['chemistry'] +
            cultural_fit['score'] * weights['cultural'] +
            budget_fit['score'] * weights['budget'] +
            age_fit['score'] * weights['age']
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(overall_score, player, team)

        return {
            'player_name': player.player_name,
            'team_name': team.team_name,
            'overall_fit_score': round(overall_score, 1),
            'fit_rating': self._get_fit_rating(overall_score),
            'recommendation': recommendation,
            'breakdown': {
                'statistical_fit': statistical_fit,
                'tactical_fit': tactical_fit,
                'personality_fit': personality_fit,
                'chemistry_fit': chemistry_fit,
                'cultural_fit': cultural_fit,
                'budget_fit': budget_fit,
                'age_fit': age_fit,
            },
            'key_strengths': self._identify_fit_strengths(player, team),
            'potential_concerns': self._identify_fit_concerns(player, team),
            'adaptation_timeline': self._estimate_adaptation_time(cultural_fit['score'], age_fit['score']),
            'signing_priority': self._calculate_signing_priority(overall_score, team),
        }

    def _calculate_statistical_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate how well player's stats match team needs."""
        score = 50  # Base score

        # Position match
        if player.position in team.priority_positions:
            score += 20

        # Performance level
        if player.opta_index >= 75:
            score += 15
        elif player.opta_index >= 65:
            score += 10
        elif player.opta_index >= 55:
            score += 5

        # Specific attribute requirements
        if team.requires_pace and player.pace >= 80:
            score += 10
        if team.requires_physicality and player.strength >= 75:
            score += 10
        if team.requires_technique and player.dribbling >= 75:
            score += 10

        # Match team level
        value_ratio = player.market_value_millions / max(team.average_player_value, 1)
        if 0.8 <= value_ratio <= 1.5:  # Similar level
            score += 5

        return {
            'score': min(score, 100),
            'analysis': 'Statistical performance matches team requirements',
            'key_stats': {
                'opta_index': player.opta_index,
                'position_match': player.position in team.priority_positions,
            }
        }

    def _calculate_tactical_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate tactical compatibility."""
        score = 50

        # Playing style compatibility
        style_bonuses = {
            PlayingStyle.POSSESSION_BASED: {
                'bonus_for': ['passing', 'decision_making'],
                'threshold': 75
            },
            PlayingStyle.COUNTER_ATTACK: {
                'bonus_for': ['pace', 'stamina'],
                'threshold': 75
            },
            PlayingStyle.HIGH_PRESS: {
                'bonus_for': ['work_rate', 'stamina', 'pace'],
                'threshold': 80
            },
            PlayingStyle.WING_PLAY: {
                'bonus_for': ['pace', 'dribbling'],
                'threshold': 75
            },
        }

        if team.playing_style in style_bonuses:
            requirements = style_bonuses[team.playing_style]
            matched = 0
            for attr in requirements['bonus_for']:
                if hasattr(player, attr) and getattr(player, attr) >= requirements['threshold']:
                    matched += 1
            score += (matched / len(requirements['bonus_for'])) * 30

        # Work rate match
        if player.work_rate >= 75 and team.playing_style == PlayingStyle.HIGH_PRESS:
            score += 10

        return {
            'score': min(score, 100),
            'analysis': f'Tactical fit for {team.playing_style.value} style',
            'playing_style_match': True if score >= 70 else False,
        }

    def _calculate_personality_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate personality and mentality fit."""
        score = 60  # Base

        # Professionalism bonus
        if player.professionalism >= 85:
            score += 15
        elif player.professionalism >= 75:
            score += 10

        # Leadership for teams needing it
        if team.team_personality == 'ambitious' and player.leadership >= 75:
            score += 15

        # Team player personality
        if player.personality_type == Personality.TEAM_PLAYER:
            score += 10

        # Temperament check
        if player.temperament == 'volatile' and team.team_personality == 'disciplined':
            score -= 20  # Potential clash

        # Work rate
        if player.work_rate >= 80:
            score += 10

        return {
            'score': min(max(score, 0), 100),
            'analysis': f'{player.personality_type.value} personality',
            'personality_match': score >= 70,
            'concerns': ['Temperament concerns'] if player.temperament == 'volatile' else [],
        }

    def _calculate_chemistry_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate squad chemistry and compatibility."""
        score = 70  # Base

        # Age group compatibility
        age_diff = abs(player.age - team.average_age)
        if age_diff <= 3:
            score += 15
        elif age_diff <= 5:
            score += 10
        elif age_diff > 10:
            score -= 10

        # Experience factor
        if team.requires_experience and player.age >= 28:
            score += 10
        elif not team.requires_experience and player.age <= 24:
            score += 10

        return {
            'score': min(score, 100),
            'analysis': 'Squad chemistry assessment',
            'age_compatibility': age_diff <= 5,
        }

    def _calculate_cultural_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate cultural adaptation likelihood."""
        score = 70  # Base

        # Language compatibility
        if player.languages and team.language in player.languages:
            score += 20

        # League experience (if moving within same league)
        # This would be checked in real implementation
        score += 10  # Placeholder

        return {
            'score': min(score, 100),
            'analysis': 'Cultural adaptation assessment',
            'language_barrier': not (player.languages and team.language in player.languages),
        }

    def _calculate_budget_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate budget compatibility."""
        score = 0

        value_ratio = player.market_value_millions / team.budget_millions

        if value_ratio <= 0.3:
            score = 100  # Very affordable
        elif value_ratio <= 0.5:
            score = 85  # Affordable
        elif value_ratio <= 0.7:
            score = 70  # Reasonable
        elif value_ratio <= 0.9:
            score = 55  # Stretching budget
        else:
            score = 30  # Over budget

        # Contract situation bonus
        if player.contract_expiry_years <= 1:
            score += 10  # Cheaper transfer fee expected

        return {
            'score': min(score, 100),
            'analysis': f'Market value: €{player.market_value_millions}M vs Budget: €{team.budget_millions}M',
            'affordable': value_ratio <= 0.7,
            'value_ratio': round(value_ratio, 2),
        }

    def _calculate_age_fit(self, player: PlayerProfile, team: TeamProfile) -> Dict:
        """Calculate age profile fit."""
        score = 70

        # Ideal age range
        if 23 <= player.age <= 28:
            score = 100  # Prime age
        elif 21 <= player.age <= 30:
            score = 85  # Good age
        elif player.age < 21:
            score = 70  # Potential
        elif player.age > 30:
            score = 60  # Experience but declining

        # Match team strategy
        if team.requires_experience and player.age >= 28:
            score += 10
        elif player.age <= 23:  # Young talent
            score += 5

        return {
            'score': min(score, 100),
            'analysis': f'Age {player.age} - {"Prime" if 23 <= player.age <= 28 else "Good" if player.age <= 30 else "Experienced"}',
            'age_category': self._get_age_category(player.age),
        }

    def _get_age_category(self, age: int) -> str:
        """Categorize player age."""
        if age < 21:
            return 'YOUTH_PROSPECT'
        elif age <= 23:
            return 'EMERGING_TALENT'
        elif age <= 28:
            return 'PRIME'
        elif age <= 32:
            return 'EXPERIENCED'
        else:
            return 'VETERAN'

    def _get_fit_rating(self, score: float) -> str:
        """Get fit rating from score."""
        if score >= 85:
            return 'EXCELLENT_FIT'
        elif score >= 75:
            return 'STRONG_FIT'
        elif score >= 65:
            return 'GOOD_FIT'
        elif score >= 55:
            return 'MODERATE_FIT'
        elif score >= 45:
            return 'FAIR_FIT'
        else:
            return 'POOR_FIT'

    def _generate_recommendation(self, score: float, player: PlayerProfile, team: TeamProfile) -> str:
        """Generate signing recommendation."""
        if score >= 85:
            return f"STRONG BUY - {player.player_name} is an excellent fit for {team.team_name}. Highly recommended signing."
        elif score >= 75:
            return f"BUY - {player.player_name} fits {team.team_name} well. Recommended signing with confidence."
        elif score >= 65:
            return f"CONSIDER - {player.player_name} is a good fit for {team.team_name}. Worth pursuing if available."
        elif score >= 55:
            return f"MONITOR - {player.player_name} shows potential fit. Requires further assessment."
        elif score >= 45:
            return f"CAUTIOUS - {player.player_name} has mixed fit indicators. Proceed with caution."
        else:
            return f"PASS - {player.player_name} is not a good fit for {team.team_name}. Look for alternatives."

    def _identify_fit_strengths(self, player: PlayerProfile, team: TeamProfile) -> List[str]:
        """Identify key fit strengths."""
        strengths = []

        if player.position in team.priority_positions:
            strengths.append(f"Plays in priority position ({player.position})")

        if player.opta_index >= 70:
            strengths.append(f"High performance level (Opta: {player.opta_index})")

        if player.professionalism >= 85:
            strengths.append("Excellent professionalism")

        if player.work_rate >= 80:
            strengths.append("Strong work rate")

        if player.age >= 23 and player.age <= 28:
            strengths.append("Prime age bracket")

        if player.leadership >= 75:
            strengths.append("Natural leader")

        return strengths[:5]  # Top 5 strengths

    def _identify_fit_concerns(self, player: PlayerProfile, team: TeamProfile) -> List[str]:
        """Identify potential concerns."""
        concerns = []

        if player.market_value_millions > team.budget_millions:
            concerns.append(f"Over budget (€{player.market_value_millions}M vs €{team.budget_millions}M)")

        if player.injury_proneness == 'high':
            concerns.append("High injury risk")

        if player.temperament == 'volatile':
            concerns.append("Temperamental - discipline concerns")

        if player.age >= 32:
            concerns.append("Age concerns - limited resale value")

        if abs(player.age - team.average_age) > 8:
            concerns.append("Age gap with current squad")

        return concerns

    def _estimate_adaptation_time(self, cultural_score: float, age_score: float) -> str:
        """Estimate adaptation timeline."""
        avg_score = (cultural_score + age_score) / 2

        if avg_score >= 85:
            return "IMMEDIATE (0-1 months) - Quick adaptation expected"
        elif avg_score >= 70:
            return "SHORT (1-3 months) - Relatively quick adaptation"
        elif avg_score >= 55:
            return "MEDIUM (3-6 months) - Standard adaptation period"
        else:
            return "LONG (6-12 months) - Extended adaptation may be needed"

    def _calculate_signing_priority(self, fit_score: float, team: TeamProfile) -> str:
        """Calculate signing priority level."""
        if fit_score >= 85:
            return "URGENT - Top priority target"
        elif fit_score >= 75:
            return "HIGH - Priority signing"
        elif fit_score >= 65:
            return "MEDIUM - Consider if available"
        elif fit_score >= 55:
            return "LOW - Monitor situation"
        else:
            return "MINIMAL - Not a priority"


def find_best_players_for_team(candidates: List[PlayerProfile], team: TeamProfile, top_n: int = 10) -> pd.DataFrame:
    """
    Find best player matches for a team from candidate list.

    Args:
        candidates: List of player profiles
        team: Team profile
        top_n: Number of top matches to return

    Returns:
        DataFrame with ranked players by fit
    """
    analyzer = TeamFitAnalyzer()
    results = []

    for player in candidates:
        fit_analysis = analyzer.analyze_fit(player, team)
        results.append({
            'player_name': player.player_name,
            'position': player.position,
            'age': player.age,
            'market_value': player.market_value_millions,
            'fit_score': fit_analysis['overall_fit_score'],
            'fit_rating': fit_analysis['fit_rating'],
            'recommendation': fit_analysis['recommendation'],
            'key_strength': fit_analysis['key_strengths'][0] if fit_analysis['key_strengths'] else 'N/A',
        })

    df = pd.DataFrame(results)
    df = df.sort_values('fit_score', ascending=False).head(top_n)
    df['rank'] = range(1, len(df) + 1)

    return df[['rank', 'player_name', 'position', 'age', 'fit_score', 'fit_rating', 'market_value', 'recommendation']]
