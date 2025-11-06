"""
Chart Utilities for Visualization
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List


def create_radar_chart(player_data: Dict, attributes: List[str] = None) -> go.Figure:
    """Create radar chart for player attributes"""

    if attributes is None:
        attributes = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

    values = [player_data.get(attr, 50) for attr in attributes]
    labels = [attr.capitalize() for attr in attributes]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=player_data.get('name', 'Player'),
        line=dict(color='#667eea', width=2),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Player Attributes",
        height=400
    )

    return fig


def create_comparison_radar(players: List[Dict], attributes: List[str] = None) -> go.Figure:
    """Create radar chart comparing multiple players"""

    if attributes is None:
        attributes = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

    labels = [attr.capitalize() for attr in attributes]

    fig = go.Figure()

    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']

    for idx, player in enumerate(players[:4]):  # Max 4 players
        values = [player.get(attr, 50) for attr in attributes]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name=player.get('name', f'Player {idx+1}'),
            line=dict(color=colors[idx % len(colors)], width=2),
            fillcolor=f'rgba({int(colors[idx % len(colors)][1:3], 16)}, {int(colors[idx % len(colors)][3:5], 16)}, {int(colors[idx % len(colors)][5:7], 16)}, 0.2)'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Player Comparison",
        height=500
    )

    return fig


def create_opta_breakdown_chart(breakdown: Dict) -> go.Figure:
    """Create bar chart for Opta Index breakdown"""

    categories = list(breakdown.keys())
    values = list(breakdown.values())

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(
                color=values,
                colorscale='Viridis',
                showscale=True,
                cmin=0,
                cmax=max(values) if values else 100
            ),
            text=[f'{v:.1f}' for v in values],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title="Opta Index Breakdown",
        xaxis_title="Category",
        yaxis_title="Score",
        height=400,
        showlegend=False
    )

    return fig


def create_team_fit_chart(fit_scores: Dict) -> go.Figure:
    """Create horizontal bar chart for team fit dimensions"""

    dimensions = [
        'Statistical Fit',
        'Tactical Fit',
        'Personality Fit',
        'Chemistry Fit',
        'Cultural Fit',
        'Budget Fit',
        'Age Fit'
    ]

    scores = [
        fit_scores.get('statistical_fit', 0),
        fit_scores.get('tactical_fit', 0),
        fit_scores.get('personality_fit', 0),
        fit_scores.get('chemistry_fit', 0),
        fit_scores.get('cultural_fit', 0),
        fit_scores.get('budget_fit', 0),
        fit_scores.get('age_fit', 0)
    ]

    # Color based on score
    colors = ['#22c55e' if s >= 75 else '#eab308' if s >= 50 else '#ef4444' for s in scores]

    fig = go.Figure(go.Bar(
        x=scores,
        y=dimensions,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{s:.1f}' for s in scores],
        textposition='outside'
    ))

    fig.update_layout(
        title="Team Fit Analysis - 7 Dimensions",
        xaxis_title="Fit Score (0-100)",
        xaxis=dict(range=[0, 100]),
        height=400,
        showlegend=False
    )

    return fig


def create_value_scatter(players: List[Dict]) -> go.Figure:
    """Create scatter plot for value analysis (Moneyball)"""

    df = pd.DataFrame(players)

    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x='market_value_millions' if 'market_value_millions' in df.columns else 'cost_millions',
        y='opta_index',
        size='value_ratio' if 'value_ratio' in df.columns else None,
        color='value_ratio' if 'value_ratio' in df.columns else 'opta_index',
        hover_name='name' if 'name' in df.columns else 'player_name',
        hover_data=['position', 'age'] if all(c in df.columns for c in ['position', 'age']) else None,
        title="Player Value Analysis",
        labels={
            'market_value_millions': 'Market Value (€M)',
            'cost_millions': 'Cost (€M)',
            'opta_index': 'Opta Index',
            'value_ratio': 'Value Ratio'
        },
        color_continuous_scale='RdYlGn'
    )

    fig.update_layout(height=500)

    return fig


def create_performance_timeline(stats: List[Dict]) -> go.Figure:
    """Create line chart for performance over time"""

    df = pd.DataFrame(stats)

    if df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.get('date', df.index),
        y=df.get('opta_index', []),
        mode='lines+markers',
        name='Opta Index',
        line=dict(color='#667eea', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title="Performance Timeline",
        xaxis_title="Date",
        yaxis_title="Opta Index",
        height=400,
        hovermode='x unified'
    )

    return fig


def create_stats_comparison_table(comparison: Dict) -> pd.DataFrame:
    """Create comparison table for multiple players"""

    if 'players' not in comparison:
        return pd.DataFrame()

    players = comparison['players']

    data = []
    for player in players:
        metrics = player.get('metrics', {})
        data.append({
            'Player': player.get('name', 'Unknown'),
            'Position': player.get('position', '-'),
            'Age': player.get('age', '-'),
            'Team': player.get('team', '-'),
            'Opta Index': metrics.get('opta_index', 0),
            'Goals': metrics.get('goals', 0),
            'Assists': metrics.get('assists', 0),
            'Pace': metrics.get('pace', 0),
            'Shooting': metrics.get('shooting', 0),
            'Passing': metrics.get('passing', 0)
        })

    return pd.DataFrame(data)


def create_gauge_chart(value: float, title: str, max_value: float = 100) -> go.Figure:
    """Create gauge chart for single metric"""

    # Determine color based on value
    if value >= 85:
        color = '#22c55e'  # Green
    elif value >= 70:
        color = '#eab308'  # Yellow
    elif value >= 50:
        color = '#f97316'  # Orange
    else:
        color = '#ef4444'  # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"},
                {'range': [50, 70], 'color': "rgba(249, 115, 22, 0.2)"},
                {'range': [70, 85], 'color': "rgba(234, 179, 8, 0.2)"},
                {'range': [85, max_value], 'color': "rgba(34, 197, 94, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(height=300)

    return fig
