from datetime import datetime

import pytest


@pytest.mark.anyio
async def test_ideation_suggested_features(api_client):
    resp = await api_client.get("/ideation/features")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body.get("features"), list)
    assert any(f.get("name") == "RSI Crossover" for f in body["features"])


@pytest.mark.anyio
async def test_ideation_analyze_smoke(api_client, mock_yfinance, monkeypatch):
    from app.routers import ideation

    original = ideation.edge_service._bootstrap_analysis
    monkeypatch.setattr(
        ideation.edge_service,
        "_bootstrap_analysis",
        lambda feature, prices, n_iterations=10000: original(feature, prices, n_iterations=200),
    )

    payload = {
        "description": "RSI crossover signal",
        "symbol": "SPY",
        "timeframe": "1D",
        "lookback_days": 200,
    }
    resp = await api_client.post("/ideation/analyze", json=payload)
    assert resp.status_code == 200
    body = resp.json()

    assert body["feature_name"] == payload["description"]
    assert "statistical_significance" in body
    assert "ml_importance" in body
    assert "confidence_intervals" in body
    assert "recommendation" in body

    assert isinstance(body["statistical_significance"]["p_value"], float)
    assert isinstance(body["statistical_significance"]["is_significant"], bool)

