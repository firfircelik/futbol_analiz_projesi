"""Basketball-specific visualizations."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional


class BasketballVisualizer:
    """Creates professional basketball visualizations."""

    def __init__(self, output_dir: str = "data/visualizations/basketball"):
        """
        Initialize basketball visualizer.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set professional styling
        sns.set_style("whitegrid")
        sns.set_palette("husl")

    def create_shot_chart(self, shot_data: pd.DataFrame, player_name: str = None) -> str:
        """
        Create NBA-style shot chart.

        Args:
            shot_data: DataFrame with shot locations and results
            player_name: Optional player name for title

        Returns:
            Path to saved visualization
        """
        fig, ax = plt.subplots(figsize=(12, 11))

        # Draw court
        self._draw_basketball_court(ax)

        # Plot shots (mock data for demonstration)
        # In production, this would use real shot location data
        makes = np.random.rand(50, 2) * [50, 47]
        misses = np.random.rand(50, 2) * [50, 47]

        ax.scatter(makes[:, 0], makes[:, 1], c='green', s=100, alpha=0.6,
                   edgecolors='darkgreen', linewidth=2, label='Made')
        ax.scatter(misses[:, 0], misses[:, 1], c='red', s=100, alpha=0.6,
                   edgecolors='darkred', linewidth=2, label='Missed')

        title = f"{player_name} Shot Chart" if player_name else "Shot Chart"
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=12)

        ax.set_xlim(0, 50)
        ax.set_ylim(0, 47)
        ax.axis('off')

        filename = f"shot_chart_{player_name.replace(' ', '_') if player_name else 'team'}.png"
        output_path = self.output_dir / filename
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Shot chart saved: {output_path}")
        return str(output_path)

    def _draw_basketball_court(self, ax):
        """Draw basketball court lines."""
        # Outer box
        ax.plot([0, 0, 50, 50, 0], [0, 47, 47, 0, 0], 'black', linewidth=2)

        # Three-point line
        three_point = plt.Circle((25, 5.25), 23.75, fill=False, color='black', linewidth=2)
        ax.add_patch(three_point)

        # Paint/Key
        ax.plot([17, 17, 33, 33], [0, 19, 19, 0], 'black', linewidth=2)

        # Free throw circle
        free_throw = plt.Circle((25, 19), 6, fill=False, color='black', linewidth=2)
        ax.add_patch(free_throw)

        # Basket
        basket = plt.Circle((25, 5.25), 0.75, fill=False, color='orange', linewidth=2)
        ax.add_patch(basket)

        # Center court
        center = plt.Circle((25, 47), 6, fill=False, color='black', linewidth=2)
        ax.add_patch(center)

    def create_player_comparison_radar(self, players_data: List[Dict], metrics: List[str]) -> str:
        """
        Create radar chart comparing multiple players.

        Args:
            players_data: List of player statistics dictionaries
            metrics: List of metric names to compare

        Returns:
            Path to saved visualization
        """
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='polar')

        # Number of metrics
        num_vars = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        # Plot each player
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        for idx, player in enumerate(players_data[:5]):  # Max 5 players
            values = [player.get(metric, 0) for metric in metrics]
            values += values[:1]

            ax.plot(angles, values, 'o-', linewidth=2,
                   label=player.get('name', f'Player {idx+1}'),
                   color=colors[idx % len(colors)])
            ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])

        # Formatting
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, size=10)
        ax.set_ylim(0, 100)
        ax.set_title("Player Comparison - Key Metrics", size=16,
                    fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)

        output_path = self.output_dir / "player_comparison_radar.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Player comparison radar saved: {output_path}")
        return str(output_path)

    def create_team_stats_dashboard(self, team_df: pd.DataFrame) -> str:
        """
        Create comprehensive team statistics dashboard.

        Args:
            team_df: DataFrame with team statistics

        Returns:
            Path to saved visualization
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('League Team Statistics Dashboard', fontsize=18, fontweight='bold')

        # 1. Win Percentage
        if 'win_pct' in team_df.columns:
            team_df_sorted = team_df.sort_values('win_pct', ascending=True).tail(10)
            axes[0, 0].barh(team_df_sorted['team_name'], team_df_sorted['win_pct'],
                           color='steelblue')
            axes[0, 0].set_xlabel('Win Percentage')
            axes[0, 0].set_title('Top 10 Teams by Win %', fontweight='bold')
            axes[0, 0].grid(axis='x', alpha=0.3)

        # 2. Points Per Game vs Points Allowed
        if 'points_per_game' in team_df.columns and 'points_allowed' in team_df.columns:
            axes[0, 1].scatter(team_df['points_per_game'], team_df['points_allowed'],
                             s=200, alpha=0.6, c=team_df['win_pct'], cmap='RdYlGn')
            axes[0, 1].set_xlabel('Points Per Game')
            axes[0, 1].set_ylabel('Points Allowed')
            axes[0, 1].set_title('Offensive vs Defensive Performance', fontweight='bold')
            axes[0, 1].grid(alpha=0.3)

            # Add diagonal line (equal offense/defense)
            lims = [
                min(axes[0, 1].get_xlim()[0], axes[0, 1].get_ylim()[0]),
                max(axes[0, 1].get_xlim()[1], axes[0, 1].get_ylim()[1])
            ]
            axes[0, 1].plot(lims, lims, 'k--', alpha=0.5, zorder=0)

        # 3. Offensive vs Defensive Rating
        if 'offensive_rating' in team_df.columns and 'defensive_rating' in team_df.columns:
            axes[1, 0].scatter(team_df['offensive_rating'], team_df['defensive_rating'],
                             s=200, alpha=0.6, c=team_df['win_pct'], cmap='RdYlGn')
            axes[1, 0].set_xlabel('Offensive Rating')
            axes[1, 0].set_ylabel('Defensive Rating')
            axes[1, 0].set_title('Advanced Ratings Comparison', fontweight='bold')
            axes[1, 0].grid(alpha=0.3)
            axes[1, 0].invert_yaxis()  # Lower defensive rating is better

        # 4. Pace Distribution
        if 'pace' in team_df.columns:
            axes[1, 1].hist(team_df['pace'], bins=15, color='coral', alpha=0.7, edgecolor='black')
            axes[1, 1].set_xlabel('Pace (Possessions per 48 minutes)')
            axes[1, 1].set_ylabel('Number of Teams')
            axes[1, 1].set_title('League Pace Distribution', fontweight='bold')
            axes[1, 1].grid(axis='y', alpha=0.3)

        output_path = self.output_dir / "team_stats_dashboard.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Team stats dashboard saved: {output_path}")
        return str(output_path)

    def create_player_performance_trends(self, player_data: pd.DataFrame, player_name: str) -> str:
        """
        Create player performance trend over time.

        Args:
            player_data: DataFrame with player game-by-game data
            player_name: Player name

        Returns:
            Path to saved visualization
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'{player_name} - Performance Trends', fontsize=18, fontweight='bold')

        # Mock game data for demonstration
        games = np.arange(1, 21)
        points = 15 + 10 * np.random.randn(20).cumsum() / 10
        rebounds = 5 + 3 * np.random.randn(20).cumsum() / 10
        assists = 3 + 2 * np.random.randn(20).cumsum() / 10
        fg_pct = 0.45 + 0.05 * np.random.randn(20)

        # Points trend
        axes[0, 0].plot(games, points, marker='o', linewidth=2, markersize=6)
        axes[0, 0].set_xlabel('Game Number')
        axes[0, 0].set_ylabel('Points')
        axes[0, 0].set_title('Points Per Game Trend', fontweight='bold')
        axes[0, 0].grid(alpha=0.3)

        # Rebounds trend
        axes[0, 1].plot(games, rebounds, marker='s', linewidth=2, markersize=6, color='green')
        axes[0, 1].set_xlabel('Game Number')
        axes[0, 1].set_ylabel('Rebounds')
        axes[0, 1].set_title('Rebounds Per Game Trend', fontweight='bold')
        axes[0, 1].grid(alpha=0.3)

        # Assists trend
        axes[1, 0].plot(games, assists, marker='^', linewidth=2, markersize=6, color='orange')
        axes[1, 0].set_xlabel('Game Number')
        axes[1, 0].set_ylabel('Assists')
        axes[1, 0].set_title('Assists Per Game Trend', fontweight='bold')
        axes[1, 0].grid(alpha=0.3)

        # FG% trend
        axes[1, 1].plot(games, fg_pct, marker='d', linewidth=2, markersize=6, color='red')
        axes[1, 1].set_xlabel('Game Number')
        axes[1, 1].set_ylabel('Field Goal %')
        axes[1, 1].set_title('Field Goal % Trend', fontweight='bold')
        axes[1, 1].grid(alpha=0.3)
        axes[1, 1].axhline(y=0.45, color='gray', linestyle='--', alpha=0.5, label='League Avg')
        axes[1, 1].legend()

        output_path = self.output_dir / f"{player_name.replace(' ', '_')}_trends.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Player performance trends saved: {output_path}")
        return str(output_path)

    def create_league_leaders_chart(self, leaders_data: Dict[str, List]) -> str:
        """
        Create league leaders visualization.

        Args:
            leaders_data: Dictionary with leader categories and player lists

        Returns:
            Path to saved visualization
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('League Leaders', fontsize=18, fontweight='bold')

        categories = ['Points', 'Rebounds', 'Assists']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

        for idx, (category, color) in enumerate(zip(categories, colors)):
            # Mock data
            players = [f'Player {i+1}' for i in range(10)]
            values = np.linspace(30, 20, 10) if idx == 0 else np.linspace(12, 8, 10)

            axes[idx].barh(players, values, color=color, alpha=0.7)
            axes[idx].set_xlabel(category)
            axes[idx].set_title(f'{category} Leaders', fontweight='bold')
            axes[idx].grid(axis='x', alpha=0.3)

            # Add value labels
            for i, v in enumerate(values):
                axes[idx].text(v, i, f' {v:.1f}', va='center')

        output_path = self.output_dir / "league_leaders.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"League leaders chart saved: {output_path}")
        return str(output_path)
