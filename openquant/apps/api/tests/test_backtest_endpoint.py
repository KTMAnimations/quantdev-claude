from datetime import datetime

import pytest


@pytest.mark.anyio
async def test_backtest_symbols_and_timeframes(api_client):
    symbols = await api_client.get("/backtest/symbols")
    assert symbols.status_code == 200
    assert any(s.get("symbol") == "SPY" for s in symbols.json().get("symbols", []))

    timeframes = await api_client.get("/backtest/timeframes")
    assert timeframes.status_code == 200
    assert any(t.get("id") == "1D" for t in timeframes.json().get("timeframes", []))


@pytest.mark.anyio
async def test_backtest_run_smoke(api_client, mock_yfinance):
    payload = {
        "strategy_code": "//@version=5\nstrategy(\"Test\", overlay=true)\n",
        "symbol": "SPY",
        "timeframe": "1D",
        "start_date": datetime(2020, 1, 1).isoformat(),
        "end_date": datetime(2020, 9, 1).isoformat(),
        "initial_capital": 10_000,
    }
    resp = await api_client.post("/backtest/run", json=payload)
    assert resp.status_code == 200
    body = resp.json()

    assert isinstance(body["total_return"], float)
    assert isinstance(body["sharpe_ratio"], float)
    assert isinstance(body["max_drawdown"], float)
    assert isinstance(body["total_trades"], int)
    assert isinstance(body["trades"], list)
    assert isinstance(body["equity_curve"], list)
    assert body["total_trades"] >= 1

    trade = body["trades"][0]
    assert set(trade.keys()) == {"entry_time", "exit_time", "pnl", "return_pct"}

