"""
Regression Analysis API Router
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.regression_service import RegressionService

router = APIRouter()
regression_service = RegressionService()


class RegressionRequest(BaseModel):
    trades: List[Dict[str, Any]]
    features: List[str] = []


class FactorResult(BaseModel):
    name: str
    coefficient: float
    p_value: float
    significance: str


class RegressionResponse(BaseModel):
    r_squared: float
    adjusted_r_squared: float
    factors: List[FactorResult]
    residuals_normality: bool
    durbin_watson: float


@router.post("/analyze", response_model=RegressionResponse)
async def run_regression_analysis(request: RegressionRequest):
    """
    Run regression analysis on backtest results
    """
    try:
        result = await regression_service.analyze(
            trades=request.trades,
            features=request.features
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/features")
async def get_available_features():
    """
    Get available features for regression analysis
    """
    return {
        "features": [
            {
                "id": "volatility",
                "name": "Volatility",
                "description": "Historical volatility at trade entry"
            },
            {
                "id": "trend_strength",
                "name": "Trend Strength",
                "description": "ADX value at trade entry"
            },
            {
                "id": "volume_ratio",
                "name": "Volume Ratio",
                "description": "Volume relative to average"
            },
            {
                "id": "time_of_day",
                "name": "Time of Day",
                "description": "Trading hour category"
            },
            {
                "id": "day_of_week",
                "name": "Day of Week",
                "description": "Trading day"
            },
            {
                "id": "market_regime",
                "name": "Market Regime",
                "description": "Bull/Bear/Sideways market classification"
            },
            {
                "id": "rsi_level",
                "name": "RSI Level",
                "description": "RSI value at entry"
            },
            {
                "id": "distance_from_ma",
                "name": "Distance from MA",
                "description": "Price distance from moving average"
            }
        ]
    }
