"""
API Client for Backend Communication
"""

import requests
from typing import Dict, List, Optional
import streamlit as st

API_BASE_URL = "http://localhost:8000/api/v1"


class APIClient:
    """Client for communicating with FastAPI backend"""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.timeout = 10

    @st.cache_data(ttl=300)
    def get_leagues(_self, sport: Optional[str] = None) -> List[Dict]:
        """Get all leagues"""
        try:
            params = {"sport": sport} if sport else {}
            response = requests.get(
                f"{_self.base_url}/leagues",
                params=params,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching leagues: {e}")
            return []

    @st.cache_data(ttl=300)
    def get_league_standings(_self, league_id: str, season: str = "2023-24") -> Dict:
        """Get league standings"""
        try:
            response = requests.get(
                f"{_self.base_url}/leagues/{league_id}/standings",
                params={"season": season},
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching standings: {e}")
            return {}

    @st.cache_data(ttl=300)
    def search_players(_self, query: Optional[str] = None, position: Optional[str] = None,
                       league_id: Optional[int] = None, min_opta_index: Optional[float] = None,
                       page: int = 1, page_size: int = 20) -> List[Dict]:
        """Search players"""
        try:
            payload = {
                "query": query,
                "position": position,
                "league_id": league_id,
                "min_opta_index": min_opta_index,
                "page": page,
                "page_size": page_size
            }
            # Remove None values
            payload = {k: v for k, v in payload.items() if v is not None}

            response = requests.post(
                f"{_self.base_url}/players/search",
                json=payload,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error searching players: {e}")
            return []

    @st.cache_data(ttl=300)
    def get_player(_self, player_id: str) -> Dict:
        """Get player details"""
        try:
            response = requests.get(
                f"{_self.base_url}/players/{player_id}",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching player: {e}")
            return {}

    @st.cache_data(ttl=300)
    def get_player_stats(_self, player_id: str) -> Dict:
        """Get player statistics"""
        try:
            response = requests.get(
                f"{_self.base_url}/players/{player_id}/stats",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching player stats: {e}")
            return {}

    @st.cache_data(ttl=300)
    def get_opta_index(_self, player_id: str) -> Dict:
        """Get Opta Performance Index"""
        try:
            response = requests.get(
                f"{_self.base_url}/analytics/opta-index/{player_id}",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching Opta Index: {e}")
            return {}

    def analyze_team_fit(_self, player_id: str, team_profile: Dict) -> Dict:
        """Analyze player-team fit"""
        try:
            payload = {
                "player_id": player_id,
                "team_profile": team_profile
            }
            response = requests.post(
                f"{_self.base_url}/team-fit/analyze",
                json=payload,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error analyzing team fit: {e}")
            return {}

    def batch_team_fit(_self, position: str, team_profile: Dict, top_n: int = 10) -> Dict:
        """Batch team fit analysis"""
        try:
            payload = {
                "league": "all",
                "position": position,
                "team_profile": team_profile,
                "top_n": top_n
            }
            response = requests.post(
                f"{_self.base_url}/team-fit/batch",
                json=payload,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error in batch analysis: {e}")
            return {}

    @st.cache_data(ttl=600)
    def get_scouting_report(_self, player_id: str) -> Dict:
        """Get scouting report"""
        try:
            response = requests.get(
                f"{_self.base_url}/scouting/report/{player_id}",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching scouting report: {e}")
            return {}

    @st.cache_data(ttl=300)
    def get_undervalued_players(_self, position: Optional[str] = None,
                                 league_id: Optional[int] = None,
                                 limit: int = 20) -> Dict:
        """Get undervalued players"""
        try:
            params = {"limit": limit}
            if position:
                params["position"] = position
            if league_id:
                params["league_id"] = league_id

            response = requests.get(
                f"{_self.base_url}/moneyball/undervalued",
                params=params,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching undervalued players: {e}")
            return {}

    @st.cache_data(ttl=300)
    def get_value_analysis(_self, player_id: str) -> Dict:
        """Get value analysis"""
        try:
            response = requests.get(
                f"{_self.base_url}/moneyball/value-analysis/{player_id}",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching value analysis: {e}")
            return {}

    def compare_players(_self, player_ids: List[str]) -> Dict:
        """Compare multiple players"""
        try:
            payload = {"player_ids": player_ids}
            response = requests.post(
                f"{_self.base_url}/players/compare",
                json=payload,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error comparing players: {e}")
            return {}

    @st.cache_data(ttl=300)
    def get_teams(_self, league_id: Optional[int] = None) -> List[Dict]:
        """Get teams"""
        try:
            params = {"league_id": league_id} if league_id else {}
            response = requests.get(
                f"{_self.base_url}/teams",
                params=params,
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching teams: {e}")
            return []

    @st.cache_data(ttl=300)
    def get_team(_self, team_id: str) -> Dict:
        """Get team details"""
        try:
            response = requests.get(
                f"{_self.base_url}/teams/{team_id}",
                timeout=_self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching team: {e}")
            return {}


# Global instance
api_client = APIClient()
