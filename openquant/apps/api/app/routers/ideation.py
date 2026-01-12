"""
Edge Discovery API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import EdgeAnalysisRequest, EdgeAnalysisResponse
from app.services.edge_discovery import EdgeDiscoveryService

router = APIRouter()


def get_edge_service():
    """Get Edge Discovery Service with LLM"""
    from app.main import get_llm_service
    return EdgeDiscoveryService(llm_service=get_llm_service())


@router.post("/analyze", response_model=EdgeAnalysisResponse)
async def analyze_edge(request: EdgeAnalysisRequest):
    """
    Analyze a trading feature/signal for predictive power.

    Uses LLM to parse natural language feature descriptions,
    then runs statistical and ML analysis.
    """
    try:
        edge_service = get_edge_service()
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
    Get suggested trading features to analyze.
    """
    return {
        "features": [
            {
                "name": "RSI Crossover",
                "description": "RSI crosses above/below 30/70 levels",
                "category": "momentum",
                "example_query": "RSI crosses below 30 after being above 70"
            },
            {
                "name": "Volume Spike",
                "description": "Volume exceeds 2x average volume",
                "category": "volume",
                "example_query": "Volume spike above 2x 20-day average with bullish candle"
            },
            {
                "name": "EMA Crossover",
                "description": "Fast EMA crosses slow EMA",
                "category": "trend",
                "example_query": "9 EMA crosses above 21 EMA"
            },
            {
                "name": "Bollinger Band Touch",
                "description": "Price touches upper/lower Bollinger Band",
                "category": "volatility",
                "example_query": "Price touches lower Bollinger Band with RSI below 30"
            },
            {
                "name": "MACD Histogram",
                "description": "MACD histogram changes direction",
                "category": "momentum",
                "example_query": "MACD histogram turns positive after being negative for 3 days"
            },
            {
                "name": "Price Breakout",
                "description": "Price breaks above/below recent high/low",
                "category": "breakout",
                "example_query": "Price breaks above 20-day high with volume confirmation"
            },
            {
                "name": "Stochastic Oversold",
                "description": "Stochastic enters oversold territory",
                "category": "momentum",
                "example_query": "Stochastic K below 20 with D crossing above K"
            }
        ]
    }


@router.get("/symbols")
async def get_available_symbols():
    """
    Get symbols available for analysis.
    """
    return {
        "symbols": [
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "type": "ETF"},
            {"symbol": "QQQ", "name": "Invesco QQQ Trust", "type": "ETF"},
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "Stock"},
            {"symbol": "MSFT", "name": "Microsoft Corp.", "type": "Stock"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "type": "Stock"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "type": "Stock"},
            {"symbol": "NVDA", "name": "NVIDIA Corp.", "type": "Stock"},
            {"symbol": "AMD", "name": "AMD Inc.", "type": "Stock"},
            {"symbol": "META", "name": "Meta Platforms", "type": "Stock"},
            {"symbol": "AMZN", "name": "Amazon.com", "type": "Stock"},
        ],
        "timeframes": ["1d", "1h", "4h", "1wk"]
    }
