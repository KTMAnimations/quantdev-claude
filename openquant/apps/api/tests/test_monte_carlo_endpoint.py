from datetime import datetime, timedelta

import pytest


def _sample_trades(n: int = 50):
    base = datetime(2020, 1, 1)
    trades = []
    for i in range(n):
        entry = base + timedelta(days=i * 2)
        exit_ = entry + timedelta(days=1)
        return_pct = (i % 7 - 3) * 0.002  # deterministic [-0.006, 0.006]
        pnl = 1000 * return_pct
        trades.append(
            {
                "entry_time": entry.isoformat(),
                "exit_time": exit_.isoformat(),
                "pnl": pnl,
                "return_pct": return_pct,
            }
        )
    return trades


@pytest.mark.anyio
async def test_monte_carlo_methods(api_client):
    resp = await api_client.get("/monte-carlo/methods")
    assert resp.status_code == 200
    methods = resp.json().get("methods", [])
    assert any(m.get("id") == "bootstrap" for m in methods)


@pytest.mark.anyio
async def test_monte_carlo_analyze_smoke(api_client):
    payload = {"trades": _sample_trades(60), "n_simulations": 200}
    resp = await api_client.post("/monte-carlo/analyze", json=payload)
    assert resp.status_code == 200
    body = resp.json()

    assert "shuffle_trades" in body
    assert "bootstrap" in body
    assert "random_entry" in body
    assert "drawdown_distribution" in body
    assert "risk_of_ruin" in body
    assert "expectancy_ci" in body
    assert "summary" in body

    assert "verdict" in body["summary"]
    assert "edge_score" in body["summary"]

