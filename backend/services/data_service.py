"""
DataService - Multi-source player data aggregation
Handles player search and profile retrieval with caching
"""

from typing import List, Optional, Dict
import logging
import sys
import os

from core.redis_client import Cache
from schemas.player import PlayerSearchResult

logger = logging.getLogger(__name__)


class DataService:
    """
    Service for fetching and aggregating player data from multiple sources.

    Caching Strategy:
    - Player search results: 15 minutes
    - Player profiles: 24 hours
    - Team data: 1 hour

    NOTE: Phase 2 in progress - Currently using mock data while connecting to real sources.
    """

    def __init__(self):
        """Initialize data service."""
        logger.info("DataService initialized (using mock data)")

    async def search_players(
        self,
        query: str,
        league: Optional[str] = None,
        position: Optional[str] = None,
        limit: int = 20
    ) -> List[PlayerSearchResult]:
        """
        Search for players across multiple data sources.

        Args:
            query: Player name search query
            league: Optional league filter
            position: Optional position filter
            limit: Maximum results to return

        Returns:
            List of player search results
        """
        cache_key = f"search:{query}:{league}:{position}:{limit}"

        # Check cache (15 minutes)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for player search: {query}")
            return [PlayerSearchResult(**p) for p in cached]

        logger.info(f"Searching players: query='{query}', league={league}, position={position}")

        try:
            # TODO: Connect to real data sources
            # For now, return filtered mock data
            mock_players = [
                {'player_id': 'salah', 'name': 'Mohamed Salah', 'team': 'Liverpool FC', 'position': 'RW', 'league': 'Premier League', 'nationality': 'Egypt', 'market_value': 65.0},
                {'player_id': 'haaland', 'name': 'Erling Haaland', 'team': 'Manchester City', 'position': 'ST', 'league': 'Premier League', 'nationality': 'Norway', 'market_value': 180.0},
                {'player_id': 'mbappe', 'name': 'Kylian Mbappé', 'team': 'Real Madrid', 'position': 'LW', 'league': 'La Liga', 'nationality': 'France', 'market_value': 180.0},
                {'player_id': 'debruyne', 'name': 'Kevin De Bruyne', 'team': 'Manchester City', 'position': 'CAM', 'league': 'Premier League', 'nationality': 'Belgium', 'market_value': 80.0},
                {'player_id': 'benzema', 'name': 'Karim Benzema', 'team': 'Al Ittihad', 'position': 'ST', 'league': 'Saudi Pro League', 'nationality': 'France', 'market_value': 15.0},
            ]

            # Filter by query (case-insensitive)
            filtered = [p for p in mock_players if query.lower() in p['name'].lower()]

            # Filter by league if specified
            if league:
                filtered = [p for p in filtered if p['league'] == league]

            # Filter by position if specified
            if position:
                filtered = [p for p in filtered if p['position'] == position]

            # Convert to PlayerSearchResult format
            player_results = []
            for player in filtered[:limit]:
                player_result = PlayerSearchResult(
                    player_id=player['player_id'],
                    name=player['name'],
                    team=player['team'],
                    position=player['position'],
                    league=player['league'],
                    opta_index=None,  # Will be calculated on profile fetch
                    market_value=player.get('market_value'),
                    nationality=player.get('nationality')
                )
                player_results.append(player_result)

            # Cache for 15 minutes (900 seconds)
            Cache.set(cache_key, [p.dict() for p in player_results], ttl=900)

            logger.info(f"Found {len(player_results)} players for query '{query}'")
            return player_results

        except Exception as e:
            logger.error(f"Player search failed: {e}", exc_info=True)
            # Return empty list on error (graceful degradation)
            return []

    async def get_player_profile(
        self,
        player_id: str,
        player_name: Optional[str] = None,
        league: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get complete player profile with stats and analytics.

        Args:
            player_id: Player identifier
            player_name: Optional player name (for better search)
            league: Optional league hint

        Returns:
            Complete player profile dictionary or None if not found
        """
        cache_key = f"profile:{player_id}"

        # Check cache (24 hours)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for player profile: {player_id}")
            return cached

        logger.info(f"Fetching player profile: id={player_id}, name={player_name}")

        try:
            # If we have player_name, use it; otherwise try to get from ID
            search_name = player_name or player_id

            # TODO: Connect to real data sources
            # For now, return structured mock data
            profile = {
                'player_name': search_name,
                'player_id': player_id,
                'league': league or 'Premier League',
                'season': '2023-2024',
                'basic_info': {
                    'name': search_name,
                    'age': 26,
                    'position': 'MID',
                    'team': 'Liverpool FC',
                    'nationality': 'England',
                    'pace': 75,
                    'strength': 70,
                    'stamina': 75,
                    'dribbling': 75,
                    'passing': 80,
                    'shooting': 70,
                    'defending': 65,
                    'work_rate': 80,
                    'decision_making': 75,
                    'composure': 75,
                    'leadership': 60,
                    'personality': 'balanced',
                    'temperament': 'calm',
                    'professionalism': 85,
                    'preferred_foot': 'right',
                    'languages': ['english'],
                },
                'performance_stats': {
                    'goals': 12,
                    'assists': 8,
                    'minutes_played': 2500,
                    'matches': 30,
                    'shots': 60,
                    'shots_on_target': 30,
                    'key_passes': 45,
                    'passes_attempted': 1200,
                    'passes_completed': 1000,
                    'tackles': 40,
                    'interceptions': 25,
                    'progressive_passes': 120,
                    'progressive_carries': 80,
                    'shots_on_target_pct': 50.0,
                    'xg': 10.5,
                    'xa': 6.8,
                },
                'market_data': {
                    'market_value': 45.0,
                    'currency': 'EUR',
                    'contract_expires': '2026-06-30',
                    'contract_expires_years': 2.5,
                },
                'xg_stats': {
                    'total_xg': 10.5,
                    'shots': 60,
                    'average_xg_per_shot': 0.175,
                },
                'data_sources': ['mock'],
                'data_quality': {
                    'sources_used': 1,
                    'completeness': 0.7,
                    'confidence': 0.6,
                }
            }

            # Cache for 24 hours (86400 seconds)
            Cache.set(cache_key, profile, ttl=86400)

            logger.info(f"Player profile fetched successfully: {player_id}")
            return profile

        except Exception as e:
            logger.error(f"Failed to fetch player profile: {e}", exc_info=True)
            return None

    async def get_team_players(
        self,
        team_name: str,
        league: str,
        season: str = "2023-2024"
    ) -> List[Dict]:
        """
        Get all players for a specific team.

        Args:
            team_name: Team name
            league: League identifier
            season: Season year

        Returns:
            List of player profiles
        """
        cache_key = f"team_players:{team_name}:{league}:{season}"

        # Check cache (1 hour)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for team players: {team_name}")
            return cached

        logger.info(f"Fetching team players: {team_name} ({league})")

        try:
            # TODO: Connect to real data sources
            # For now, return empty list
            players = []

            # Cache for 1 hour (3600 seconds)
            Cache.set(cache_key, players, ttl=3600)

            logger.info(f"Team players endpoint not yet implemented: {team_name}")
            return players

        except Exception as e:
            logger.error(f"Failed to fetch team players: {e}", exc_info=True)
            return []

    async def get_league_top_players(
        self,
        league: str,
        season: str = "2023-2024",
        limit: int = 50
    ) -> List[Dict]:
        """
        Get top players in a league.

        Args:
            league: League identifier
            season: Season year
            limit: Number of players to return

        Returns:
            List of top player profiles
        """
        cache_key = f"league_top:{league}:{season}:{limit}"

        # Check cache (1 hour)
        cached = Cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for league top players: {league}")
            return cached

        logger.info(f"Fetching top players for league: {league}")

        try:
            # TODO: Connect to real data sources
            # For now, return empty list
            top_players = []

            # Cache for 1 hour (3600 seconds)
            Cache.set(cache_key, top_players, ttl=3600)

            logger.info(f"League top players endpoint not yet implemented: {league}")
            return top_players

        except Exception as e:
            logger.error(f"Failed to fetch league top players: {e}", exc_info=True)
            return []


# Singleton instance
_data_service_instance = None

def get_data_service() -> DataService:
    """Get or create DataService singleton instance."""
    global _data_service_instance
    if _data_service_instance is None:
        _data_service_instance = DataService()
    return _data_service_instance
