import numpy as np
import pandas as pd
import pytest

from app.services.monte_carlo_service import MonteCarloConfig, MonteCarloService


def test_monte_carlo_percentiles_empty():
    svc = MonteCarloService(MonteCarloConfig(n_simulations=10))
    p = svc._calculate_percentiles([])
    assert set(p.keys()) == {"p5", "p10", "p25", "p50", "p75", "p90", "p95", "p99"}
    assert all(v == 0.0 for v in p.values())


@pytest.mark.anyio
async def test_monte_carlo_run_full_analysis_smoke():
    trades = pd.DataFrame(
        {
            "entry_time": pd.date_range("2020-01-01", periods=30, freq="D"),
            "exit_time": pd.date_range("2020-01-02", periods=30, freq="D"),
            "pnl": np.linspace(-10, 20, 30),
            "return_pct": np.linspace(-0.01, 0.02, 30),
        }
    )
    equity_curve = pd.Series((1 + trades["return_pct"]).cumprod())

    svc = MonteCarloService(MonteCarloConfig(n_simulations=100))
    result = await svc.run_full_analysis(trades=trades, equity_curve=equity_curve)

    assert "bootstrap" in result
    assert "summary" in result
    assert "verdict" in result["summary"]

