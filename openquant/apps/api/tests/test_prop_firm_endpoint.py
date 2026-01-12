import pytest


@pytest.mark.anyio
async def test_prop_firm_firms_and_comparison(api_client):
    firms = await api_client.get("/prop-firm/firms")
    assert firms.status_code == 200
    assert any(f.get("id") == "ftmo" for f in firms.json().get("firms", []))

    comparison = await api_client.get("/prop-firm/comparison")
    assert comparison.status_code == 200
    assert "headers" in comparison.json().get("comparison", {})


@pytest.mark.anyio
async def test_prop_firm_simulate_smoke(api_client, synthetic_daily_returns):
    payload = {"daily_returns": synthetic_daily_returns, "prop_firm": "ftmo", "n_simulations": 200}
    resp = await api_client.post("/prop-firm/simulate", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert 0.0 <= body["combined_pass_rate"] <= 1.0
    assert "expected_value" in body
    assert "recommendation" in body["expected_value"]


@pytest.mark.anyio
async def test_prop_firm_simulate_unsupported_firm(api_client, synthetic_daily_returns):
    payload = {"daily_returns": synthetic_daily_returns, "prop_firm": "mff", "n_simulations": 50}
    resp = await api_client.post("/prop-firm/simulate", json=payload)
    assert resp.status_code == 400
    assert "Unsupported prop firm" in resp.json()["detail"]

