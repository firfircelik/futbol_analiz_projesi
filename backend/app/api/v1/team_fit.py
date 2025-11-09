"""
Team Fit Analyzer API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.player import Player
from app.schemas.analytics import TeamFitRequest, TeamFitResponse, TeamFitBatchRequest
from src.team_fit.team_fit_analyzer import TeamFitAnalyzer, PlayerProfile, TeamProfile, PlayingStyle, Personality

router = APIRouter()


@router.post("/analyze", response_model=TeamFitResponse)
async def analyze_team_fit(
    request: TeamFitRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze player-team compatibility
    """
    player = db.query(Player).filter(Player.player_id == request.player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Create player profile
    player_profile = PlayerProfile(
        player_name=player.name,
        age=player.age,
        position=player.position,
        opta_index=player.opta_index,
        pace=player.pace,
        dribbling=player.dribbling,
        passing=player.passing,
        shooting=player.shooting,
        defending=player.defending,
        physical=player.physical,
        personality_type=Personality[player.personality_type.upper()] if player.personality_type else Personality.PROFESSIONAL,
        temperament=player.temperament,
        professionalism=player.professionalism,
        languages=[player.nationality] if player.nationality else []
    )

    # Create team profile from request
    team_data = request.team_profile
    team_profile = TeamProfile(
        team_name=team_data.get('team_name', 'Team'),
        playing_style=PlayingStyle[team_data.get('playing_style', 'BALANCED').upper()],
        formation=team_data.get('formation', '4-3-3'),
        budget_millions=team_data.get('budget_millions', 50.0),
        priority_positions=team_data.get('priority_positions', []),
        desired_traits=team_data.get('desired_traits', []),
        requires_pace=team_data.get('requires_pace', False),
        requires_technique=team_data.get('requires_technique', False)
    )

    # Analyze fit
    analyzer = TeamFitAnalyzer()
    fit_result = analyzer.analyze_fit(player_profile, team_profile)

    return TeamFitResponse(
        player_id=request.player_id,
        player_name=player.name,
        team_name=team_profile.team_name,
        overall_fit_score=fit_result['overall_fit_score'],
        fit_rating=fit_result['fit_rating'],
        recommendation=fit_result['recommendation'],
        statistical_fit=fit_result['statistical_fit'],
        tactical_fit=fit_result['tactical_fit'],
        personality_fit=fit_result['personality_fit'],
        chemistry_fit=fit_result['chemistry_fit'],
        cultural_fit=fit_result['cultural_fit'],
        budget_fit=fit_result['budget_fit'],
        age_fit=fit_result['age_fit'],
        key_strengths=fit_result['key_strengths'],
        key_concerns=fit_result['key_concerns'],
        adaptation_timeline=fit_result['adaptation_timeline']
    )


@router.post("/batch")
async def batch_analyze_team_fit(
    request: TeamFitBatchRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze multiple players for team fit
    """
    # Get all players in position
    players = db.query(Player).filter(Player.position == request.position).limit(100).all()

    if not players:
        raise HTTPException(status_code=404, detail=f"No players found for position {request.position}")

    # Create team profile
    team_data = request.team_profile
    team_profile = TeamProfile(
        team_name=team_data.get('team_name', 'Team'),
        playing_style=PlayingStyle[team_data.get('playing_style', 'BALANCED').upper()],
        formation=team_data.get('formation', '4-3-3'),
        budget_millions=team_data.get('budget_millions', 50.0),
        priority_positions=team_data.get('priority_positions', []),
        desired_traits=team_data.get('desired_traits', []),
        requires_pace=team_data.get('requires_pace', False),
        requires_technique=team_data.get('requires_technique', False)
    )

    analyzer = TeamFitAnalyzer()
    results = []

    for player in players:
        player_profile = PlayerProfile(
            player_name=player.name,
            age=player.age,
            position=player.position,
            opta_index=player.opta_index,
            pace=player.pace,
            dribbling=player.dribbling,
            passing=player.passing,
            shooting=player.shooting,
            defending=player.defending,
            physical=player.physical,
            personality_type=Personality.PROFESSIONAL,
            temperament=player.temperament,
            professionalism=player.professionalism,
            languages=[]
        )

        fit_result = analyzer.analyze_fit(player_profile, team_profile)

        results.append({
            "player_id": player.player_id,
            "player_name": player.name,
            "age": player.age,
            "opta_index": player.opta_index,
            "fit_score": fit_result['overall_fit_score'],
            "fit_rating": fit_result['fit_rating'],
            "recommendation": fit_result['recommendation']
        })

    # Sort by fit score
    results.sort(key=lambda x: x['fit_score'], reverse=True)

    return {
        "position": request.position,
        "total_analyzed": len(results),
        "top_matches": results[:request.top_n]
    }
