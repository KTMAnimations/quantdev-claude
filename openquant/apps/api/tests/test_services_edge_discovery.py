import numpy as np
import pytest

from app.services.edge_discovery import EdgeDiscoveryService


@pytest.mark.anyio
async def test_edge_discovery_parse_feature_description():
    svc = EdgeDiscoveryService()
    assert (await svc._parse_feature_description("RSI crossover"))["type"] == "rsi"
    assert (await svc._parse_feature_description("EMA crossover"))["type"] == "ema"
    assert (await svc._parse_feature_description("Volume spike"))["type"] == "volume_spike"
    assert (await svc._parse_feature_description("Bollinger bands touch"))["type"] == "bollinger"


def test_edge_discovery_compute_and_stats(synthetic_ohlcv_df):
    svc = EdgeDiscoveryService()
    prices = synthetic_ohlcv_df.copy()
    prices.columns = prices.columns.str.lower()

    feature = svc._compute_feature(prices, {"type": "rsi", "period": 14})
    assert len(feature) == len(prices)

    finite = feature.dropna()
    assert len(finite) > 0
    assert np.isfinite(finite).all()
    assert (finite >= 0).all()
    assert (finite <= 100).all()

    stats = svc._run_statistical_tests(feature, prices)
    assert set(stats.keys()) == {
        "correlation_1d",
        "correlation_5d",
        "ic_mean",
        "ic_std",
        "ic_ir",
        "t_statistic",
        "p_value",
        "is_significant",
        "quantile_returns",
    }
    assert isinstance(stats["p_value"], float)
    assert isinstance(stats["quantile_returns"], dict)


def test_edge_discovery_ml_and_bootstrap(synthetic_ohlcv_df):
    svc = EdgeDiscoveryService()
    prices = synthetic_ohlcv_df.copy()
    prices.columns = prices.columns.str.lower()
    feature = svc._compute_feature(prices, {"type": "momentum", "period": 10})

    ml = svc._run_ml_analysis(feature, prices)
    assert set(ml.keys()) == {
        "cv_accuracy",
        "cv_std",
        "feature_importance",
        "has_predictive_power",
        "shap_summary",
    }
    assert 0.0 <= ml["cv_accuracy"] <= 1.0

    bootstrap = svc._bootstrap_analysis(feature, prices, n_iterations=200)
    assert 0.0 <= bootstrap["probability_positive"] <= 1.0
    assert bootstrap["ci_lower_95"] <= bootstrap["ci_upper_95"]
    assert bootstrap["ci_lower_99"] <= bootstrap["ci_upper_99"]

