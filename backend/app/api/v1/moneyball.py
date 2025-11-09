"""
Moneyball System API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.player import Player
from app.schemas.analytics import MoneyballAnalysis
from src.moneyball.player_valuation import PlayerValuation

router = APIRouter()


@router.get("/undervalued")
async def find_undervalued_players(
    position: str = None,
    league_id: int = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Find undervalued players with high value ratios
    """
    query = db.query(Player).filter(Player.market_value_millions.isnot(None))

    if position:
        query = query.filter(Player.position == position)
    if league_id:
        query = query.filter(Player.league_id == league_id)

    players = query.all()

    # Calculate value ratio for each
    results = []
    for player in players:
        if player.market_value_millions and player.market_value_millions > 0:
            value_ratio = player.opta_index / player.market_value_millions

            # Consider undervalued if good performance but low price
            if value_ratio > 5.0:  # Threshold for undervalued
                results.append({
                    "player_id": player.player_id,
                    "name": player.name,
                    "position": player.position,
                    "age": player.age,
                    "team": player.team.name if player.team else "N/A",
                    "opta_index": player.opta_index,
                    "market_value_millions": player.market_value_millions,
                    "value_ratio": round(value_ratio, 2),
                    "valuation_status": "undervalued",
                    "roi_potential": "high" if value_ratio > 8.0 else "medium"
                })

    # Sort by value ratio
    results.sort(key=lambda x: x['value_ratio'], reverse=True)

    return {
        "total_found": len(results),
        "players": results[:limit]
    }


@router.get("/value-analysis/{player_id}", response_model=MoneyballAnalysis)
async def get_value_analysis(
    player_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed Moneyball valuation analysis for a player
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Calculate value metrics
    market_value = player.market_value_millions or 10.0
    performance_score = player.opta_index
    value_ratio = performance_score / market_value if market_value > 0 else 0

    # Determine valuation status
    if value_ratio > 6.0:
        status = "undervalued"
        roi = "high"
        recommendation = "STRONG BUY - Excellent value for money"
        target_price = market_value * 0.8
    elif value_ratio > 4.0:
        status = "fair_value"
        roi = "medium"
        recommendation = "CONSIDER - Good value at current price"
        target_price = market_value
    else:
        status = "overvalued"
        roi = "low"
        recommendation = "MONITOR - May be overpriced"
        target_price = market_value * 1.2

    # Consistency score (simplified - would calculate from match history)
    consistency = 75.0 if player.form_rating == "good" else 60.0

    # Potential score (age-based)
    if player.age < 23:
        potential = 85.0
    elif player.age < 27:
        potential = 75.0
    else:
        potential = 60.0

    reasoning = f"{player.name} shows {performance_score:.1f} Opta Index performance with €{market_value}M valuation. "
    reasoning += f"Value ratio of {value_ratio:.2f} indicates {status} status. "
    reasoning += f"{'High' if player.age < 25 else 'Moderate'} potential for growth."

    return MoneyballAnalysis(
        player_id=player_id,
        player_name=player.name,
        position=player.position,
        estimated_market_value=market_value * value_ratio / 5.0,  # Normalized estimate
        actual_market_value=market_value,
        value_ratio=round(value_ratio, 2),
        valuation_status=status,
        roi_potential=roi,
        performance_score=performance_score,
        consistency_score=consistency,
        potential_score=potential,
        recommendation=recommendation,
        target_price=round(target_price, 2),
        reasoning=reasoning
    )


@router.post("/budget-optimizer")
async def optimize_squad_budget(
    budget: float,
    positions_needed: list,
    db: Session = Depends(get_db)
):
    """
    Optimize squad building within budget
    """
    # Get players for each needed position
    recommended_squad = []
    remaining_budget = budget

    for position in positions_needed:
        # Find best value players in position
        players = db.query(Player).filter(
            Player.position == position,
            Player.market_value_millions <= remaining_budget,
            Player.market_value_millions.isnot(None)
        ).all()

        if players:
            # Sort by value ratio
            players_with_ratio = []
            for p in players:
                if p.market_value_millions > 0:
                    ratio = p.opta_index / p.market_value_millions
                    players_with_ratio.append((p, ratio))

            players_with_ratio.sort(key=lambda x: x[1], reverse=True)

            # Pick best value
            if players_with_ratio:
                best_player, ratio = players_with_ratio[0]
                recommended_squad.append({
                    "player_id": best_player.player_id,
                    "name": best_player.name,
                    "position": position,
                    "cost_millions": best_player.market_value_millions,
                    "opta_index": best_player.opta_index,
                    "value_ratio": round(ratio, 2)
                })
                remaining_budget -= best_player.market_value_millions

    total_cost = sum(p['cost_millions'] for p in recommended_squad)
    avg_opta = sum(p['opta_index'] for p in recommended_squad) / len(recommended_squad) if recommended_squad else 0

    return {
        "total_budget": budget,
        "total_cost": round(total_cost, 2),
        "remaining_budget": round(remaining_budget, 2),
        "squad_size": len(recommended_squad),
        "average_opta_index": round(avg_opta, 2),
        "recommended_squad": recommended_squad
    }
