"""
OptaService - Opta Performance Index calculation
Calculates 0-100 player ratings based on performance metrics
"""

from typing import Dict, Optional
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# NOTE: Temporarily disabled real Opta calculation due to import issues
# Will re-enable in next iteration
# from opta_analytics.performance_index import OptaPerformanceIndex, PerformanceMetrics
from core.redis_client import Cache

logger = logging.getLogger(__name__)


class OptaService:
    """
    Service for calculating Opta Performance Index.

    The Opta Index is a comprehensive 0-100 player rating that considers:
    - Offensive contributions (goals, assists, shots)
    - Defensive actions (tackles, interceptions, clearances)
    - Passing efficiency
    - Possession management
    - Tactical discipline

    Caching Strategy:
    - Calculated indexes: 24 hours (updates daily)
    """

    def __init__(self):
        """Initialize Opta service."""
        self.opta_index = OptaPerformanceIndex()
        logger.info("OptaService initialized")

    async def calculate_player_index(
        self,
        player_stats: Dict,
        position: str = "MID"
    ) -> Dict:
        """
        Calculate Opta Performance Index for a player.

        Args:
            player_stats: Player statistics dictionary
            position: Player position (GK, DEF, MID, FWD)

        Returns:
            Dictionary with Opta Index and breakdown:
            {
                'opta_index': 75.5,
                'rating': 'EXCELLENT',
                'breakdown': {...},
                'percentile': 85,
                'performance_level': 'TOP_LEVEL'
            }
        """
        player_id = player_stats.get('player_id', player_stats.get('player_name', 'unknown'))
        cache_key = f"opta_index:{player_id}"

        # Check cache (24 hours)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for Opta Index: {player_id}")
            return cached

        logger.info(f"Calculating Opta Index for player: {player_id}")

        try:
            # Extract performance stats
            perf_stats = player_stats.get('performance_stats', {})
            basic_stats = player_stats.get('basic_stats', {})

            # Create PerformanceMetrics object
            metrics = PerformanceMetrics(
                # Offensive
                goals=perf_stats.get('goals', basic_stats.get('goals', 0)),
                assists=perf_stats.get('assists', basic_stats.get('assists', 0)),
                shots=perf_stats.get('shots', 0),
                shots_on_target=perf_stats.get('shots_on_target', 0),
                key_passes=perf_stats.get('key_passes', 0),
                successful_dribbles=perf_stats.get('successful_dribbles', 0),

                # Passing
                passes_attempted=perf_stats.get('passes_attempted', 0),
                passes_completed=perf_stats.get('passes_completed', 0),
                pass_accuracy=perf_stats.get('pass_accuracy', 0.0),
                progressive_passes=perf_stats.get('progressive_passes', 0),

                # Defensive
                tackles=perf_stats.get('tackles', 0),
                interceptions=perf_stats.get('interceptions', 0),
                clearances=perf_stats.get('clearances', 0),
                blocks=perf_stats.get('blocks', 0),

                # Possession
                touches=perf_stats.get('touches', 0),
                possession_won=perf_stats.get('possession_won', 0),
                possession_lost=perf_stats.get('possession_lost', 0),

                # Discipline
                fouls_committed=perf_stats.get('fouls_committed', 0),
                fouls_won=perf_stats.get('fouls_won', 0),
                yellow_cards=perf_stats.get('yellow_cards', 0),
                red_cards=perf_stats.get('red_cards', 0),

                # Context
                minutes_played=basic_stats.get('minutes_played', 90),
                team_goals_for=perf_stats.get('team_goals_for', 0),
                team_goals_against=perf_stats.get('team_goals_against', 0),
            )

            # Calculate index
            result = self.opta_index.calculate_index(metrics, position)

            # Cache for 24 hours (86400 seconds)
            Cache.set(cache_key, result, ttl=86400)

            logger.info(
                f"Opta Index calculated: {player_id} = {result['opta_index']} "
                f"({result['rating']})"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to calculate Opta Index: {e}", exc_info=True)
            # Return default values on error
            return {
                'opta_index': 50.0,
                'rating': 'AVERAGE',
                'breakdown': {},
                'percentile': 50,
                'performance_level': 'PROFESSIONAL'
            }

    async def calculate_team_index(
        self,
        players: list[Dict]
    ) -> Dict:
        """
        Calculate team-level Opta Index from player indexes.

        Args:
            players: List of player dictionaries with stats

        Returns:
            Team index analysis:
            {
                'team_opta_index': 65.5,
                'team_rating': 'PLAYOFF_TEAM',
                'top_performers': ['Player1', 'Player2', 'Player3'],
                'consistency_score': 85.2,
                'depth_analysis': 'STRONG'
            }
        """
        try:
            # Calculate index for each player
            player_indexes = []
            for player in players:
                index_result = await self.calculate_player_index(
                    player,
                    player.get('position', 'MID')
                )
                player_indexes.append({
                    'player_name': player.get('player_name', 'Unknown'),
                    'opta_index': index_result['opta_index']
                })

            if not player_indexes:
                return {}

            # Calculate team metrics
            import numpy as np
            from opta_analytics.performance_index import calculate_team_opta_index

            team_result = calculate_team_opta_index(player_indexes)

            logger.info(
                f"Team Index calculated: {team_result.get('team_opta_index')} "
                f"({team_result.get('team_rating')})"
            )

            return team_result

        except Exception as e:
            logger.error(f"Failed to calculate team index: {e}", exc_info=True)
            return {}

    def get_rating_description(self, rating: str) -> str:
        """
        Get human-readable description of Opta rating.

        Args:
            rating: Rating level (e.g., 'EXCELLENT', 'GOOD')

        Returns:
            Description string
        """
        descriptions = {
            'EXCEPTIONAL': 'World-class performance. Among the best in the world.',
            'EXCELLENT': 'Outstanding performance. Top-level quality.',
            'GOOD': 'Strong performance. Above average quality.',
            'AVERAGE': 'Decent performance. Standard professional level.',
            'BELOW_AVERAGE': 'Underwhelming performance. Below expected level.',
            'POOR': 'Subpar performance. Needs significant improvement.'
        }
        return descriptions.get(rating, 'Performance level not classified.')


# Singleton instance
_opta_service_instance = None

def get_opta_service() -> OptaService:
    """Get or create OptaService singleton instance."""
    global _opta_service_instance
    if _opta_service_instance is None:
        _opta_service_instance = OptaService()
    return _opta_service_instance
