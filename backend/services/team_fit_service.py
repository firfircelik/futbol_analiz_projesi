"""
TeamFitService - 7-dimensional team fit analysis
Analyzes how well a player fits a specific team
"""

from typing import Dict, Optional
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from team_fit.team_fit_analyzer import (
    TeamFitAnalyzer,
    PlayerProfile,
    TeamProfile,
    PlayingStyle,
    Personality
)
from core.redis_client import Cache

logger = logging.getLogger(__name__)


class TeamFitService:
    """
    Service for analyzing team fit compatibility.

    Analyzes 7 dimensions:
    1. Statistical Fit - Performance level and stats match
    2. Tactical Fit - Playing style compatibility
    3. Personality Fit - Mentality and character match
    4. Chemistry Fit - Squad age and experience compatibility
    5. Cultural Fit - League, language, adaptation
    6. Budget Fit - Market value vs team budget
    7. Age Fit - Age profile alignment

    Caching Strategy:
    - Team fit analyses: 7 days (relatively stable)
    """

    def __init__(self):
        """Initialize team fit service."""
        self.analyzer = TeamFitAnalyzer()
        logger.info("TeamFitService initialized")

    async def analyze_fit(
        self,
        player_id: str,
        player_data: Dict,
        team_id: str,
        team_data: Dict
    ) -> Dict:
        """
        Analyze how well a player fits a specific team.

        Args:
            player_id: Player identifier
            player_data: Player statistics and attributes
            team_id: Team identifier
            team_data: Team profile and requirements

        Returns:
            Complete fit analysis with score and recommendation:
            {
                'player_name': str,
                'team_name': str,
                'overall_fit_score': float,
                'fit_rating': str,
                'recommendation': str,
                'breakdown': {...},
                'key_strengths': [...],
                'potential_concerns': [...],
                'adaptation_timeline': str,
                'signing_priority': str
            }
        """
        cache_key = f"team_fit:{player_id}:{team_id}"

        # Check cache (7 days)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for team fit: {player_id} -> {team_id}")
            return cached

        logger.info(f"Analyzing team fit: {player_id} -> {team_id}")

        try:
            # Convert player data to PlayerProfile
            player_profile = self._create_player_profile(player_data)

            # Convert team data to TeamProfile
            team_profile = self._create_team_profile(team_data)

            # Run analysis
            result = self.analyzer.analyze_fit(player_profile, team_profile)

            # Cache for 7 days (604800 seconds)
            Cache.set(cache_key, result, ttl=604800)

            logger.info(
                f"Team fit analysis complete: {player_id} -> {team_id} = "
                f"{result['overall_fit_score']:.1f} ({result['fit_rating']})"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to analyze team fit: {e}", exc_info=True)
            # Return default response on error
            return {
                'player_name': player_data.get('player_name', 'Unknown'),
                'team_name': team_data.get('team_name', 'Unknown'),
                'overall_fit_score': 50.0,
                'fit_rating': 'MODERATE_FIT',
                'recommendation': 'Analysis unavailable - insufficient data',
                'breakdown': {},
                'key_strengths': [],
                'potential_concerns': ['Insufficient data for analysis'],
                'adaptation_timeline': 'UNKNOWN',
                'signing_priority': 'LOW - Requires further assessment'
            }

    def _create_player_profile(self, player_data: Dict) -> PlayerProfile:
        """Convert player data dictionary to PlayerProfile object."""

        # Get stats
        perf = player_data.get('performance_stats', {})
        basic = player_data.get('basic_stats', {})
        basic_info = player_data.get('basic_info', {})

        return PlayerProfile(
            player_name=player_data.get('player_name', 'Unknown'),
            age=basic_info.get('age', player_data.get('age', 25)),
            position=basic_info.get('position', player_data.get('position', 'MID')),
            nationality=basic_info.get('nationality', player_data.get('nationality', 'Unknown')),
            current_team=basic_info.get('team', player_data.get('team', 'Unknown')),
            market_value_millions=player_data.get('market_data', {}).get('market_value', 10.0),

            # Performance
            opta_index=player_data.get('opta_index', {}).get('opta_index', 60.0),
            goals=perf.get('goals', basic.get('goals', 0)),
            assists=perf.get('assists', basic.get('assists', 0)),
            matches_played=basic.get('matches', 38),

            # Physical attributes (use defaults if not available)
            pace=basic_info.get('pace', 70),
            strength=basic_info.get('strength', 70),
            stamina=basic_info.get('stamina', 70),

            # Technical attributes
            dribbling=basic_info.get('dribbling', 70),
            passing=basic_info.get('passing', 70),
            shooting=basic_info.get('shooting', 70),
            defending=basic_info.get('defending', 70),

            # Mental attributes
            work_rate=basic_info.get('work_rate', 70),
            decision_making=basic_info.get('decision_making', 70),
            composure=basic_info.get('composure', 70),
            leadership=basic_info.get('leadership', 50),

            # Personality
            personality_type=self._parse_personality(basic_info.get('personality', 'balanced')),
            temperament=basic_info.get('temperament', 'calm'),
            professionalism=basic_info.get('professionalism', 80),

            # Other
            preferred_foot=basic_info.get('preferred_foot', 'right'),
            languages=basic_info.get('languages', ['english']),
            injury_proneness=basic_info.get('injury_proneness', 'low'),
            contract_expiry_years=player_data.get('market_data', {}).get('contract_expires_years', 2.0),
        )

    def _create_team_profile(self, team_data: Dict) -> TeamProfile:
        """Convert team data dictionary to TeamProfile object."""

        return TeamProfile(
            team_name=team_data.get('team_name', 'Unknown Team'),
            league=team_data.get('league', 'Unknown'),
            playing_style=self._parse_playing_style(team_data.get('playing_style', 'possession_based')),
            formation=team_data.get('formation', '4-3-3'),
            average_age=team_data.get('average_age', 26.0),
            budget_millions=team_data.get('budget_millions', 30.0),

            # Team needs
            priority_positions=team_data.get('priority_positions', ['ST', 'CAM', 'LW']),
            desired_traits=team_data.get('desired_traits', ['pace', 'dribbling', 'leadership']),

            # Characteristics
            average_player_value=team_data.get('average_player_value', 15.0),
            team_personality=team_data.get('team_personality', 'disciplined'),
            preferred_foot=team_data.get('preferred_foot'),
            language=team_data.get('language', 'english'),

            # Tactical requirements
            requires_pace=team_data.get('requires_pace', False),
            requires_physicality=team_data.get('requires_physicality', False),
            requires_technique=team_data.get('requires_technique', False),
            requires_experience=team_data.get('requires_experience', False),

            # Squad gaps
            missing_attributes=team_data.get('missing_attributes', []),
        )

    def _parse_playing_style(self, style_str: str) -> PlayingStyle:
        """Parse playing style string to enum."""
        style_map = {
            'possession_based': PlayingStyle.POSSESSION_BASED,
            'counter_attack': PlayingStyle.COUNTER_ATTACK,
            'high_press': PlayingStyle.HIGH_PRESS,
            'defensive': PlayingStyle.DEFENSIVE,
            'direct': PlayingStyle.DIRECT,
            'wing_play': PlayingStyle.WING_PLAY,
            'through_middle': PlayingStyle.THROUGH_MIDDLE,
        }
        return style_map.get(style_str.lower(), PlayingStyle.POSSESSION_BASED)

    def _parse_personality(self, personality_str: str) -> Personality:
        """Parse personality string to enum."""
        personality_map = {
            'leader': Personality.LEADER,
            'professional': Personality.PROFESSIONAL,
            'ambitious': Personality.AMBITIOUS,
            'team_player': Personality.TEAM_PLAYER,
            'maverick': Personality.MAVERICK,
            'driven': Personality.DRIVEN,
            'balanced': Personality.BALANCED,
            'temperamental': Personality.TEMPERAMENTAL,
        }
        return personality_map.get(personality_str.lower(), Personality.BALANCED)


# Singleton instance
_team_fit_service_instance = None

def get_team_fit_service() -> TeamFitService:
    """Get or create TeamFitService singleton instance."""
    global _team_fit_service_instance
    if _team_fit_service_instance is None:
        _team_fit_service_instance = TeamFitService()
    return _team_fit_service_instance
