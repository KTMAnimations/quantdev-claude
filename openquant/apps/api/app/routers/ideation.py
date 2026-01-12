"""
Edge Discovery API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import EdgeAnalysisRequest, EdgeAnalysisResponse
from app.services.edge_discovery import EdgeDiscoveryService

router = APIRouter()
edge_service = EdgeDiscoveryService()


@router.post("/analyze", response_model=EdgeAnalysisResponse)
async def analyze_edge(request: EdgeAnalysisRequest):
    """
    Analyze a trading feature/signal for predictive power
    """
    try:
        result = await edge_service.analyze_feature(
            feature_description=request.description,
            symbol=request.symbol,
            timeframe=request.timeframe,
            lookback_days=request.lookback_days
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/features")
async def get_suggested_features():
    """
    Get suggested trading features to analyze
    """
    return {
        "features": [
            {
                "name": "RSI Crossover",
                "description": "RSI crosses above/below 30/70 levels",
                "category": "momentum"
            },
            {
                "name": "Volume Spike",
                "description": "Volume exceeds 2x average volume",
                "category": "volume"
            },
            {
                "name": "EMA Crossover",
                "description": "Fast EMA crosses slow EMA",
                "category": "trend"
            },
            {
                "name": "Bollinger Band Touch",
                "description": "Price touches upper/lower Bollinger Band",
                "category": "volatility"
            },
            {
                "name": "MACD Histogram",
                "description": "MACD histogram changes direction",
                "category": "momentum"
            }
        ]
    }
