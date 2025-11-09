"""
MoneyballService - Player valuation and market inefficiency detection
Identifies undervalued players and calculates ROI potential
"""

from typing import Dict, List, Optional
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from moneyball.player_valuation import PlayerValuationEngine
from core.redis_client import Cache

logger = logging.getLogger(__name__)


class MoneyballService:
    """
    Service for Moneyball-style player valuation.

    Identifies:
    - Undervalued players (market value < calculated value)
    - Overvalued players (market value > calculated value)
    - Market inefficiencies
    - ROI potential

    Categories:
    - BARGAIN: Value ratio > 1.5 (50%+ undervalued)
    - UNDERVALUED: Value ratio 1.2-1.5 (20-50% undervalued)
    - FAIR: Value ratio 0.8-1.2 (fair market value)
    - OVERVALUED: Value ratio < 0.8 (overvalued)

    Caching Strategy:
    - Valuations: 24 hours (market values change daily)
    """

    def __init__(self):
        """Initialize Moneyball service."""
        self.valuation_engine = PlayerValuationEngine(sport='football')
        logger.info("MoneyballService initialized")

    async def calculate_valuation(
        self,
        player_id: str,
        player_stats: Dict,
        market_value: Optional[float] = None
    ) -> Dict:
        """
        Calculate Moneyball-style player valuation.

        Args:
            player_id: Player identifier
            player_stats: Player statistics
            market_value: Current market value in millions (optional)

        Returns:
            Valuation analysis:
            {
                'player_id': str,
                'player_name': str,
                'market_value': float,
                'calculated_value': float,
                'value_ratio': float,
                'category': str (BARGAIN/UNDERVALUED/FAIR/OVERVALUED),
                'roi_potential': float,
                'recommendation': str (STRONG_BUY/BUY/HOLD/SELL),
                'comparable_players': [...]
            }
        """
        cache_key = f"moneyball:{player_id}"

        # Check cache (24 hours)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for Moneyball valuation: {player_id}")
            return cached

        logger.info(f"Calculating Moneyball valuation for: {player_id}")

        try:
            # Calculate player value using engine
            value_assessment = self.valuation_engine.calculate_player_value(player_stats)

            calculated_value = value_assessment['estimated_market_value_millions']

            # Get or estimate market value
            if market_value is None:
                market_value = player_stats.get('market_data', {}).get('market_value', calculated_value)

            # Calculate value ratio (calculated / market)
            value_ratio = calculated_value / max(market_value, 0.5)

            # Determine category and recommendation
            category = self._get_value_category(value_ratio)
            recommendation = self._get_recommendation(value_ratio, calculated_value, market_value)

            # Calculate ROI potential (%)
            roi_potential = ((calculated_value - market_value) / market_value) * 100

            result = {
                'player_id': player_id,
                'player_name': player_stats.get('player_name', 'Unknown'),
                'market_value': round(market_value, 2),
                'calculated_value': round(calculated_value, 2),
                'value_ratio': round(value_ratio, 2),
                'category': category,
                'roi_potential': round(roi_potential, 1),
                'recommendation': recommendation,
                'value_score': value_assessment.get('player_value_score', 50),
                'value_tier': value_assessment.get('value_tier', 'ROLE_PLAYER'),
                'comparable_players': [],  # TODO: Implement similarity search
            }

            # Cache for 24 hours (86400 seconds)
            Cache.set(cache_key, result, ttl=86400)

            logger.info(
                f"Moneyball valuation complete: {player_id} - "
                f"Market: €{market_value}M, Calculated: €{calculated_value}M "
                f"({category})"
            )

            return result

        except Exception as e:
            logger.error(f"Failed to calculate Moneyball valuation: {e}", exc_info=True)
            # Return default values on error
            return {
                'player_id': player_id,
                'player_name': player_stats.get('player_name', 'Unknown'),
                'market_value': market_value or 10.0,
                'calculated_value': market_value or 10.0,
                'value_ratio': 1.0,
                'category': 'FAIR',
                'roi_potential': 0.0,
                'recommendation': 'HOLD',
                'value_score': 50,
                'value_tier': 'ROLE_PLAYER',
                'comparable_players': [],
            }

    async def find_undervalued_players(
        self,
        players: List[Dict],
        budget: float = 20.0,
        min_value_ratio: float = 1.2
    ) -> List[Dict]:
        """
        Find undervalued players from a list.

        Args:
            players: List of player dictionaries with stats
            budget: Maximum budget in millions
            min_value_ratio: Minimum value ratio to consider (default 1.2 = 20% undervalued)

        Returns:
            List of undervalued players ranked by value ratio
        """
        logger.info(f"Searching for undervalued players: budget=€{budget}M, min_ratio={min_value_ratio}")

        undervalued = []

        for player in players:
            try:
                player_id = player.get('player_id', player.get('player_name', 'unknown'))
                market_value = player.get('market_data', {}).get('market_value', 10.0)

                # Skip if over budget
                if market_value > budget:
                    continue

                # Calculate valuation
                valuation = await self.calculate_valuation(
                    player_id=player_id,
                    player_stats=player,
                    market_value=market_value
                )

                # Check if undervalued enough
                if valuation['value_ratio'] >= min_value_ratio:
                    undervalued.append({
                        'player_id': player_id,
                        'player_name': valuation['player_name'],
                        'position': player.get('position', 'Unknown'),
                        'age': player.get('age', 25),
                        'market_value': valuation['market_value'],
                        'calculated_value': valuation['calculated_value'],
                        'value_ratio': valuation['value_ratio'],
                        'category': valuation['category'],
                        'roi_potential': valuation['roi_potential'],
                        'recommendation': valuation['recommendation'],
                    })

            except Exception as e:
                logger.warning(f"Failed to value player {player.get('player_name', 'Unknown')}: {e}")
                continue

        # Sort by value ratio (best deals first)
        undervalued.sort(key=lambda x: x['value_ratio'], reverse=True)

        logger.info(f"Found {len(undervalued)} undervalued players within budget")

        return undervalued

    async def compare_players(
        self,
        player1_id: str,
        player1_stats: Dict,
        player2_id: str,
        player2_stats: Dict
    ) -> Dict:
        """
        Compare two players head-to-head for value.

        Args:
            player1_id: First player ID
            player1_stats: First player stats
            player2_id: Second player ID
            player2_stats: Second player stats

        Returns:
            Comparison analysis with recommendation
        """
        logger.info(f"Comparing players: {player1_id} vs {player2_id}")

        try:
            # Calculate valuations
            val1 = await self.calculate_valuation(player1_id, player1_stats)
            val2 = await self.calculate_valuation(player2_id, player2_stats)

            # Determine winner
            if val1['value_ratio'] > val2['value_ratio']:
                winner = 'player1'
                better_value = val1['player_name']
            elif val2['value_ratio'] > val1['value_ratio']:
                winner = 'player2'
                better_value = val2['player_name']
            else:
                winner = 'tie'
                better_value = 'Equal value'

            return {
                'player1': {
                    'name': val1['player_name'],
                    'market_value': val1['market_value'],
                    'calculated_value': val1['calculated_value'],
                    'value_ratio': val1['value_ratio'],
                    'category': val1['category'],
                    'roi_potential': val1['roi_potential'],
                },
                'player2': {
                    'name': val2['player_name'],
                    'market_value': val2['market_value'],
                    'calculated_value': val2['calculated_value'],
                    'value_ratio': val2['value_ratio'],
                    'category': val2['category'],
                    'roi_potential': val2['roi_potential'],
                },
                'winner': winner,
                'better_value': better_value,
                'value_difference': abs(val1['value_ratio'] - val2['value_ratio']),
                'cost_difference': abs(val1['market_value'] - val2['market_value']),
                'recommendation': self._generate_comparison_recommendation(val1, val2),
            }

        except Exception as e:
            logger.error(f"Failed to compare players: {e}", exc_info=True)
            return {
                'error': 'Comparison failed',
                'message': str(e)
            }

    def _get_value_category(self, value_ratio: float) -> str:
        """Categorize value based on ratio."""
        if value_ratio >= 1.5:
            return 'BARGAIN'
        elif value_ratio >= 1.2:
            return 'UNDERVALUED'
        elif value_ratio >= 0.8:
            return 'FAIR'
        else:
            return 'OVERVALUED'

    def _get_recommendation(
        self,
        value_ratio: float,
        calculated_value: float,
        market_value: float
    ) -> str:
        """Generate investment recommendation."""
        if value_ratio >= 1.5:
            return 'STRONG_BUY'
        elif value_ratio >= 1.2:
            return 'BUY'
        elif value_ratio >= 0.9:
            return 'HOLD'
        elif value_ratio >= 0.7:
            return 'CONSIDER_SELLING'
        else:
            return 'SELL'

    def _generate_comparison_recommendation(self, val1: Dict, val2: Dict) -> str:
        """Generate comparison recommendation."""
        ratio_diff = abs(val1['value_ratio'] - val2['value_ratio'])
        cost_diff = abs(val1['market_value'] - val2['market_value'])

        if ratio_diff < 0.1:
            return f"Similar value. Choose based on team fit and budget (€{cost_diff:.1f}M difference)."
        elif val1['value_ratio'] > val2['value_ratio']:
            savings = val2['market_value'] - val1['market_value']
            if savings > 0:
                return f"{val1['name']} offers better value AND costs €{savings:.1f}M less. Clear choice."
            else:
                return f"{val1['name']} offers {((val1['value_ratio'] - val2['value_ratio']) * 100):.0f}% better value. Worth the premium."
        else:
            savings = val1['market_value'] - val2['market_value']
            if savings > 0:
                return f"{val2['name']} offers better value AND costs €{savings:.1f}M less. Clear choice."
            else:
                return f"{val2['name']} offers {((val2['value_ratio'] - val1['value_ratio']) * 100):.0f}% better value. Worth the premium."


# Singleton instance
_moneyball_service_instance = None

def get_moneyball_service() -> MoneyballService:
    """Get or create MoneyballService singleton instance."""
    global _moneyball_service_instance
    if _moneyball_service_instance is None:
        _moneyball_service_instance = MoneyballService()
    return _moneyball_service_instance
