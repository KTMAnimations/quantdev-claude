"""
Monte Carlo Simulation API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import MonteCarloRequest, MonteCarloResponse
from app.services.monte_carlo_service import MonteCarloService
import pandas as pd

router = APIRouter()
mc_service = MonteCarloService()


@router.post("/analyze", response_model=MonteCarloResponse)
async def run_monte_carlo(request: MonteCarloRequest):
    """
    Run Monte Carlo simulation on backtest results
    """
    try:
        # Convert trades to DataFrame
        trades_df = pd.DataFrame([trade.model_dump() for trade in request.trades])

        # Create equity curve from trades
        equity_curve = pd.Series(
            (1 + trades_df["return_pct"]).cumprod()
        )

        result = await mc_service.run_full_analysis(
            trades=trades_df,
            equity_curve=equity_curve
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/methods")
async def get_monte_carlo_methods():
    """
    Get available Monte Carlo simulation methods
    """
    return {
        "methods": [
            {
                "id": "shuffle_trades",
                "name": "Trade Shuffle",
                "description": "Randomly shuffle trade order to test sequence dependency"
            },
            {
                "id": "bootstrap",
                "name": "Bootstrap Resampling",
                "description": "Resample trades with replacement for metric stability"
            },
            {
                "id": "random_entry",
                "name": "Random Entry",
                "description": "Compare strategy to random entry timing"
            }
        ]
    }
