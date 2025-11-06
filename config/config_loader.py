"""Configuration loader for multi-sport analytics platform."""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any


class ConfigLoader:
    """Loads and manages configuration for sports analytics."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to configuration YAML file
        """
        if config_path is None:
            base_dir = Path(__file__).parent
            config_path = base_dir / "leagues_config.yaml"

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_sport_config(self, sport: str) -> Dict[str, Any]:
        """
        Get configuration for a specific sport.

        Args:
            sport: Sport name ('football' or 'basketball')

        Returns:
            Sport configuration dictionary
        """
        return self.config['sports'].get(sport, {})

    def get_leagues(self, sport: str) -> List[Dict[str, Any]]:
        """
        Get all leagues for a sport.

        Args:
            sport: Sport name ('football' or 'basketball')

        Returns:
            List of league configurations
        """
        sport_config = self.get_sport_config(sport)
        return sport_config.get('leagues', [])

    def get_league_by_id(self, sport: str, league_id: str) -> Dict[str, Any]:
        """
        Get specific league configuration.

        Args:
            sport: Sport name ('football' or 'basketball')
            league_id: League identifier

        Returns:
            League configuration dictionary
        """
        leagues = self.get_leagues(sport)
        for league in leagues:
            if league['id'] == league_id:
                return league
        return {}

    def get_analysis_metrics(self, sport: str, advanced: bool = False) -> List[str]:
        """
        Get analysis metrics for a sport.

        Args:
            sport: Sport name ('football' or 'basketball')
            advanced: If True, return advanced metrics

        Returns:
            List of metric names
        """
        analysis_config = self.config.get('analysis', {}).get(sport, {})
        key = 'advanced_metrics' if advanced else 'key_metrics'
        return analysis_config.get(key, [])

    def get_report_types(self) -> List[str]:
        """Get available report types."""
        return self.config.get('reports', {}).get('types', [])

    def get_export_formats(self) -> List[str]:
        """Get available export formats."""
        return self.config.get('reports', {}).get('export_formats', [])

    def get_all_sports(self) -> List[str]:
        """Get list of all configured sports."""
        return list(self.config['sports'].keys())


# Global configuration instance
_config_instance = None


def get_config() -> ConfigLoader:
    """Get global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance
