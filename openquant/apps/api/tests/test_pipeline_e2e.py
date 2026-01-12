from datetime import datetime

import pytest


@pytest.mark.anyio
async def test_pipeline_ideation_to_prop_firm(api_client, mock_yfinance, monkeypatch, synthetic_ohlcv_df):
    from app.routers import ideation

    original_bootstrap = ideation.edge_service._bootstrap_analysis
    monkeypatch.setattr(
        ideation.edge_service,
        "_bootstrap_analysis",
        lambda feature, prices, n_iterations=10000: original_bootstrap(feature, prices, n_iterations=200),
    )

    description = "EMA crossover strategy"

    ideation_resp = await api_client.post(
        "/ideation/analyze",
        json={"description": description, "symbol": "SPY", "timeframe": "1D", "lookback_days": 200},
    )
    assert ideation_resp.status_code == 200

    pine_resp = await api_client.post(
        "/pine/generate",
        json={"description": description, "script_type": "strategy"},
    )
    assert pine_resp.status_code == 200
    pine_code = pine_resp.json()["code"]

    backtest_resp = await api_client.post(
        "/backtest/run",
        json={
            "strategy_code": pine_code,
            "symbol": "SPY",
            "timeframe": "1D",
            "start_date": datetime(2020, 1, 1).isoformat(),
            "end_date": datetime(2020, 9, 1).isoformat(),
            "initial_capital": 10_000,
        },
    )
    assert backtest_resp.status_code == 200
    backtest_body = backtest_resp.json()
    assert backtest_body["total_trades"] >= 1

    trades = backtest_body["trades"]

    mc_resp = await api_client.post(
        "/monte-carlo/analyze",
        json={"trades": trades, "n_simulations": 200},
    )
    assert mc_resp.status_code == 200

    reg_resp = await api_client.post("/regression/analyze", json={"trades": trades, "features": []})
    assert reg_resp.status_code == 200

    daily_returns = synthetic_ohlcv_df["Close"].pct_change().dropna().tolist()
    pf_resp = await api_client.post(
        "/prop-firm/simulate",
        json={"daily_returns": daily_returns, "prop_firm": "ftmo", "n_simulations": 200},
    )
    assert pf_resp.status_code == 200

