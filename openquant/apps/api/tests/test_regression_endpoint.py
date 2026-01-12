import pytest


@pytest.mark.anyio
async def test_regression_features(api_client):
    resp = await api_client.get("/regression/features")
    assert resp.status_code == 200
    feats = resp.json().get("features", [])
    assert any(f.get("id") == "volatility" for f in feats)


@pytest.mark.anyio
async def test_regression_empty_trades(api_client):
    resp = await api_client.post("/regression/analyze", json={"trades": [], "features": []})
    assert resp.status_code == 200
    body = resp.json()
    assert body["r_squared"] == 0.0
    assert body["factors"] == []


@pytest.mark.anyio
async def test_regression_non_empty_trades(api_client):
    trades = [
        {"return_pct": 0.01},
        {"return_pct": -0.005},
        {"return_pct": 0.002},
        {"return_pct": 0.004},
        {"return_pct": -0.003},
        {"return_pct": 0.006},
        {"return_pct": 0.0},
        {"return_pct": 0.008},
        {"return_pct": -0.002},
        {"return_pct": 0.003},
    ]
    resp = await api_client.post("/regression/analyze", json={"trades": trades, "features": []})
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body["r_squared"], float)
    assert len(body["factors"]) == 4


@pytest.mark.anyio
async def test_regression_small_sample_returns_empty(api_client):
    resp = await api_client.post(
        "/regression/analyze",
        json={"trades": [{"return_pct": 0.01}], "features": []},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["factors"] == []
