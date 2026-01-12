"""
Backtesting API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import BacktestRequest, BacktestResponse
from app.services.backtest_service import BacktestService

router = APIRouter()
backtest_service = BacktestService()


@router.post("/run", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Run a backtest on a Pine Script strategy
    """
    try:
        result = await backtest_service.run_backtest(
            strategy_code=request.strategy_code,
            symbol=request.symbol,
            timeframe=request.timeframe,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/symbols")
async def get_available_symbols():
    """
    Get available trading symbols
    """
    return {
        "symbols": [
            {"symbol": "SPY", "name": "S&P 500 ETF", "type": "etf"},
            {"symbol": "QQQ", "name": "Nasdaq 100 ETF", "type": "etf"},
            {"symbol": "AAPL", "name": "Apple Inc.", "type": "stock"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "type": "stock"},
            {"symbol": "TSLA", "name": "Tesla Inc.", "type": "stock"},
            {"symbol": "BTCUSD", "name": "Bitcoin/USD", "type": "crypto"},
            {"symbol": "ETHUSD", "name": "Ethereum/USD", "type": "crypto"},
            {"symbol": "EURUSD", "name": "Euro/USD", "type": "forex"},
            {"symbol": "GBPUSD", "name": "British Pound/USD", "type": "forex"},
        ]
    }


@router.get("/timeframes")
async def get_available_timeframes():
    """
    Get available timeframes
    """
    return {
        "timeframes": [
            {"id": "1m", "name": "1 Minute"},
            {"id": "5m", "name": "5 Minutes"},
            {"id": "15m", "name": "15 Minutes"},
            {"id": "1h", "name": "1 Hour"},
            {"id": "4h", "name": "4 Hours"},
            {"id": "1D", "name": "Daily"},
            {"id": "1W", "name": "Weekly"},
        ]
    }
