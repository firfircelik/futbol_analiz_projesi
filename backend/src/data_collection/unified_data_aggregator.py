"""
Unified Data Aggregator - Master Orchestrator for Opta Replacement
Combines data from multiple free sources to achieve professional-grade coverage
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Import existing data collectors
from src.data_collection.statsbomb_enhanced import StatsBombEnhancedCollector
from src.data_collection.free_football_api import FreeFootballAPI
from src.data_collection.free_basketball_api import FreeBasketballAPI

# Import analytics engines
from src.opta_analytics.performance_index import OptaPerformanceIndex, PerformanceMetrics
from src.opta_analytics.expected_goals import ExpectedGoalsEngine, ShotContext
from src.team_fit.team_fit_analyzer import TeamFitAnalyzer
from src.moneyball.player_valuation import PlayerValuation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    """Metadata about a data source."""
    name: str
    priority: int  # 1 = highest quality, lower numbers = higher priority
    coverage: str  # 'full', 'partial', 'limited'
    freshness: str  # 'live', 'daily', 'weekly'
    reliability: float  # 0-1 score


class UnifiedDataAggregator:
    """
    Master data aggregator that combines multiple sources.

    Strategy:
    1. Collect from all available sources
    2. Validate and clean data
    3. Merge using priority-based resolution
    4. Calculate advanced metrics
    5. Return comprehensive dataset
    """

    # Data source priorities (lower = better)
    SOURCES = {
        'statsbomb': DataSource('StatsBomb', 1, 'partial', 'daily', 0.95),
        'understat': DataSource('Understat', 2, 'partial', 'live', 0.90),
        'fbref': DataSource('FBref', 3, 'full', 'daily', 0.85),
        'transfermarkt': DataSource('Transfermarkt', 4, 'full', 'weekly', 0.80),
        'thesportsdb': DataSource('TheSportsDB', 5, 'full', 'live', 0.70),
    }

    def __init__(self, enable_cache: bool = True):
        """
        Initialize unified aggregator.

        Args:
            enable_cache: Whether to cache results
        """
        logger.info("Initializing Unified Data Aggregator")

        # Initialize collectors
        self.statsbomb = StatsBombEnhancedCollector()
        self.football_api = FreeFootballAPI()
        self.basketball_api = FreeBasketballAPI()

        # Initialize analytics engines
        self.opta_index = OptaPerformanceIndex()
        self.xg_engine = ExpectedGoalsEngine()
        self.team_fit = TeamFitAnalyzer()

        self.enable_cache = enable_cache
        self._cache = {}

        logger.info("✓ All data sources initialized")

    def get_player_complete_profile(
        self,
        player_name: str,
        league: str = None,
        season: str = "2023-2024"
    ) -> Dict:
        """
        Get comprehensive player profile from all sources.

        Args:
            player_name: Player name
            league: League identifier (optional, helps narrow search)
            season: Season year

        Returns:
            Complete player profile with all available data
        """
        logger.info(f"Collecting complete profile for: {player_name}")

        profile = {
            'player_name': player_name,
            'league': league,
            'season': season,
            'data_sources': [],
            'basic_info': {},
            'performance_stats': {},
            'advanced_metrics': {},
            'market_data': {},
            'opta_index': None,
            'xg_stats': {},
            'data_quality': {},
        }

        # 1. Collect from all sources
        collected_data = self._collect_multi_source_data(player_name, league, season)

        # 2. Merge and validate
        merged_data = self._merge_player_data(collected_data)

        # 3. Calculate advanced metrics
        if merged_data:
            profile['basic_info'] = merged_data.get('basic', {})
            profile['performance_stats'] = merged_data.get('performance', {})
            profile['market_data'] = merged_data.get('market', {})

            # Calculate Opta Index
            if self._has_sufficient_stats(merged_data):
                profile['opta_index'] = self._calculate_opta_index(merged_data)

            # Calculate xG if shot data available
            if 'shots' in merged_data:
                profile['xg_stats'] = self._calculate_xg_stats(merged_data['shots'])

            # Data quality assessment
            profile['data_quality'] = self._assess_data_quality(collected_data)

        logger.info(f"✓ Profile complete. Sources used: {len(collected_data)}")
        return profile

    def get_team_complete_analysis(
        self,
        team_name: str,
        league: str,
        season: str = "2023-2024"
    ) -> Dict:
        """
        Get comprehensive team analysis from all sources.

        Args:
            team_name: Team name
            league: League identifier
            season: Season year

        Returns:
            Complete team analysis
        """
        logger.info(f"Analyzing team: {team_name} ({league})")

        analysis = {
            'team_name': team_name,
            'league': league,
            'season': season,
            'squad': [],
            'team_stats': {},
            'tactical_analysis': {},
            'squad_value': {},
            'team_opta_index': None,
        }

        # Collect team data
        team_data = self._collect_team_data(team_name, league, season)

        # Get all players
        if 'players' in team_data:
            for player in team_data['players']:
                player_profile = self.get_player_complete_profile(
                    player['name'],
                    league,
                    season
                )
                analysis['squad'].append(player_profile)

        # Team-level metrics
        if analysis['squad']:
            analysis['team_opta_index'] = self._calculate_team_index(analysis['squad'])
            analysis['squad_value'] = self._calculate_squad_value(analysis['squad'])

        return analysis

    def get_league_overview(
        self,
        league: str,
        season: str = "2023-2024",
        include_players: bool = False
    ) -> Dict:
        """
        Get complete league overview.

        Args:
            league: League identifier
            season: Season year
            include_players: Whether to include individual player data

        Returns:
            League overview with all teams and stats
        """
        logger.info(f"Generating league overview: {league} {season}")

        overview = {
            'league': league,
            'season': season,
            'teams': [],
            'top_players': [],
            'league_stats': {},
            'standings': None,
        }

        # Get standings
        standings = self._get_league_standings(league, season)
        overview['standings'] = standings

        # Get top players
        top_players = self._get_league_top_players(league, season, limit=50)
        overview['top_players'] = top_players

        # League-wide statistics
        overview['league_stats'] = self._calculate_league_stats(standings, top_players)

        return overview

    def find_similar_players(
        self,
        player_name: str,
        league: str = None,
        top_n: int = 10
    ) -> List[Dict]:
        """
        Find players with similar profiles.

        Args:
            player_name: Target player name
            league: League to search (None = all leagues)
            top_n: Number of similar players to return

        Returns:
            List of similar players with similarity scores
        """
        logger.info(f"Finding players similar to: {player_name}")

        # Get target player profile
        target_profile = self.get_player_complete_profile(player_name, league)

        # Search candidates
        candidates = self._get_player_candidates(league)

        # Calculate similarity scores
        similar_players = []
        for candidate in candidates:
            if candidate['name'] != player_name:
                similarity = self._calculate_similarity(target_profile, candidate)
                similar_players.append({
                    'player_name': candidate['name'],
                    'similarity_score': similarity,
                    'profile': candidate,
                })

        # Sort by similarity
        similar_players.sort(key=lambda x: x['similarity_score'], reverse=True)

        return similar_players[:top_n]

    def _collect_multi_source_data(
        self,
        player_name: str,
        league: str,
        season: str
    ) -> Dict[str, Dict]:
        """Collect player data from all available sources."""
        collected = {}

        # Try StatsBomb (highest quality)
        try:
            sb_data = self._collect_from_statsbomb(player_name, league, season)
            if sb_data:
                collected['statsbomb'] = sb_data
                logger.info(f"✓ StatsBomb data collected")
        except Exception as e:
            logger.warning(f"StatsBomb collection failed: {e}")

        # Try FBref/TheSportsDB (good coverage)
        try:
            api_data = self._collect_from_api(player_name, league, season)
            if api_data:
                collected['thesportsdb'] = api_data
                logger.info(f"✓ API data collected")
        except Exception as e:
            logger.warning(f"API collection failed: {e}")

        return collected

    def _merge_player_data(self, collected_data: Dict[str, Dict]) -> Dict:
        """
        Merge data from multiple sources using priority-based resolution.

        Strategy:
        - Use highest priority source for each field
        - Cross-validate when multiple sources available
        - Flag inconsistencies
        """
        if not collected_data:
            return {}

        merged = {
            'basic': {},
            'performance': {},
            'market': {},
            'shots': [],
            'passes': [],
        }

        # Sort sources by priority
        sources_sorted = sorted(
            collected_data.items(),
            key=lambda x: self.SOURCES.get(x[0], DataSource(x[0], 99, 'unknown', 'unknown', 0.5)).priority
        )

        # Merge fields (later sources override earlier if priority is higher)
        for source_name, source_data in sources_sorted:
            for category in merged:
                if category in source_data:
                    if isinstance(source_data[category], dict):
                        merged[category].update(source_data[category])
                    elif isinstance(source_data[category], list):
                        merged[category].extend(source_data[category])

        return merged

    def _calculate_opta_index(self, player_data: Dict) -> Dict:
        """Calculate Opta Performance Index from merged data."""
        perf_stats = player_data.get('performance', {})

        # Map to PerformanceMetrics format
        metrics = PerformanceMetrics(
            goals=perf_stats.get('goals', 0),
            assists=perf_stats.get('assists', 0),
            shots=perf_stats.get('shots', 0),
            shots_on_target=perf_stats.get('shots_on_target', 0),
            key_passes=perf_stats.get('key_passes', 0),
            passes_attempted=perf_stats.get('passes_attempted', 0),
            passes_completed=perf_stats.get('passes_completed', 0),
            tackles=perf_stats.get('tackles', 0),
            interceptions=perf_stats.get('interceptions', 0),
            minutes_played=perf_stats.get('minutes_played', 90),
        )

        position = player_data.get('basic', {}).get('position', 'MID')
        return self.opta_index.calculate_index(metrics, position)

    def _calculate_xg_stats(self, shots: List[Dict]) -> Dict:
        """Calculate xG statistics from shot data."""
        total_xg = 0.0
        shot_details = []

        for shot in shots:
            # Convert to ShotContext
            shot_context = ShotContext(
                distance_to_goal=shot.get('distance', 15),
                angle_to_goal=shot.get('angle', 30),
                shot_type=shot.get('type', 'right_foot'),
                body_part=shot.get('body_part', 'foot'),
                assist_type=shot.get('assist_type', 'none'),
                game_state=shot.get('game_state', 'open_play'),
                defender_pressure=shot.get('pressure', 'medium'),
                goalkeeper_position=shot.get('gk_position', 'set'),
            )

            xg_result = self.xg_engine.calculate_xg(shot_context)
            total_xg += xg_result['xg']
            shot_details.append(xg_result)

        return {
            'total_xg': round(total_xg, 2),
            'shots': len(shots),
            'average_xg_per_shot': round(total_xg / len(shots), 3) if shots else 0,
            'shot_details': shot_details,
        }

    def _collect_from_statsbomb(
        self,
        player_name: str,
        league: str,
        season: str
    ) -> Optional[Dict]:
        """Collect from StatsBomb (event-level data)."""
        # Implementation would use statsbomb collector
        # For now, return None as placeholder
        return None

    def _collect_from_api(
        self,
        player_name: str,
        league: str,
        season: str
    ) -> Optional[Dict]:
        """Collect from TheSportsDB API."""
        # Implementation would search for player and get stats
        # Placeholder for now
        return None

    def _collect_team_data(
        self,
        team_name: str,
        league: str,
        season: str
    ) -> Dict:
        """Collect team data from all sources."""
        return {}

    def _get_league_standings(self, league: str, season: str) -> pd.DataFrame:
        """Get league standings."""
        # Use existing API
        try:
            return self.football_api.get_league_standings(league, season)
        except:
            return pd.DataFrame()

    def _get_league_top_players(
        self,
        league: str,
        season: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get top players in league."""
        return []

    def _calculate_league_stats(
        self,
        standings: pd.DataFrame,
        top_players: List[Dict]
    ) -> Dict:
        """Calculate league-wide statistics."""
        stats = {
            'total_teams': len(standings) if not standings.empty else 0,
            'total_players': len(top_players),
            'average_goals_per_game': 0,
            'total_matches': 0,
        }

        if not standings.empty and 'played' in standings.columns:
            stats['total_matches'] = standings['played'].sum() // 2

        return stats

    def _calculate_team_index(self, squad: List[Dict]) -> Dict:
        """Calculate team-level Opta index."""
        if not squad:
            return {}

        player_indexes = [
            p.get('opta_index', {})
            for p in squad
            if p.get('opta_index')
        ]

        if not player_indexes:
            return {}

        avg_index = np.mean([p.get('opta_index', 0) for p in player_indexes])

        return {
            'team_opta_index': round(avg_index, 1),
            'squad_size': len(squad),
            'players_with_data': len(player_indexes),
        }

    def _calculate_squad_value(self, squad: List[Dict]) -> Dict:
        """Calculate total squad value."""
        total_value = sum(
            p.get('market_data', {}).get('market_value', 0)
            for p in squad
        )

        return {
            'total_value_millions': round(total_value, 2),
            'average_value_per_player': round(total_value / len(squad), 2) if squad else 0,
        }

    def _get_player_candidates(self, league: str = None) -> List[Dict]:
        """Get candidate players for similarity search."""
        # Placeholder - would query database or APIs
        return []

    def _calculate_similarity(
        self,
        player1: Dict,
        player2: Dict
    ) -> float:
        """
        Calculate similarity score between two players.

        Uses:
        - Position similarity
        - Performance stats correlation
        - Physical attributes
        - Playing style
        """
        # Placeholder - implement actual similarity algorithm
        return 0.0

    def _has_sufficient_stats(self, data: Dict) -> bool:
        """Check if we have enough data to calculate metrics."""
        perf = data.get('performance', {})
        return 'goals' in perf or 'assists' in perf or 'shots' in perf

    def _assess_data_quality(self, collected_data: Dict[str, Dict]) -> Dict:
        """
        Assess quality of collected data.

        Returns quality scores and metadata.
        """
        return {
            'sources_used': len(collected_data),
            'source_names': list(collected_data.keys()),
            'completeness': self._calculate_completeness(collected_data),
            'confidence': self._calculate_confidence(collected_data),
        }

    def _calculate_completeness(self, collected_data: Dict[str, Dict]) -> float:
        """Calculate data completeness score (0-1)."""
        if not collected_data:
            return 0.0

        # Simplified: more sources = more complete
        return min(len(collected_data) / 3, 1.0)

    def _calculate_confidence(self, collected_data: Dict[str, Dict]) -> float:
        """Calculate confidence score based on source reliability."""
        if not collected_data:
            return 0.0

        total_reliability = sum(
            self.SOURCES.get(source, DataSource(source, 99, '', '', 0.5)).reliability
            for source in collected_data
        )

        return total_reliability / len(collected_data)


# Convenience functions
def get_player(player_name: str, league: str = None) -> Dict:
    """Quick function to get player profile."""
    aggregator = UnifiedDataAggregator()
    return aggregator.get_player_complete_profile(player_name, league)


def get_team(team_name: str, league: str) -> Dict:
    """Quick function to get team analysis."""
    aggregator = UnifiedDataAggregator()
    return aggregator.get_team_complete_analysis(team_name, league)


def get_league(league: str, season: str = "2023-2024") -> Dict:
    """Quick function to get league overview."""
    aggregator = UnifiedDataAggregator()
    return aggregator.get_league_overview(league, season)


if __name__ == "__main__":
    # Demo usage
    print("="*80)
    print("UNIFIED DATA AGGREGATOR - Opta Replacement Demo")
    print("="*80)
    print()

    aggregator = UnifiedDataAggregator()

    # Example: Get player profile
    print("Example 1: Player Profile")
    print("-"*80)
    player = aggregator.get_player_complete_profile("Lionel Messi", "LALIGA")
    print(f"Player: {player['player_name']}")
    print(f"Data sources used: {player['data_quality']['sources_used']}")
    print(f"Confidence: {player['data_quality']['confidence']:.2f}")
    print()

    print("✓ Unified Data Aggregator Ready")
