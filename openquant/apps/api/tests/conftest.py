import numpy as np
import pandas as pd
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(autouse=True)
def _seed_numpy():
    np.random.seed(12345)


def _make_synthetic_ohlcv(n: int = 260) -> pd.DataFrame:
    dates = pd.date_range("2020-01-01", periods=n, freq="D")

    quarter = n // 4
    close = np.concatenate(
        [
            np.linspace(100, 90, quarter, endpoint=False),
            np.linspace(90, 110, quarter, endpoint=False),
            np.linspace(110, 95, quarter, endpoint=False),
            np.linspace(95, 120, n - (3 * quarter)),
        ]
    )

    rng = np.random.default_rng(7)
    close = close + rng.normal(0, 0.25, size=n)
    open_ = close + rng.normal(0, 0.15, size=n)
    high = np.maximum(open_, close) + rng.uniform(0.05, 0.5, size=n)
    low = np.minimum(open_, close) - rng.uniform(0.05, 0.5, size=n)
    volume = (1_000_000 + rng.normal(0, 50_000, size=n)).clip(min=100_000)

    return pd.DataFrame(
        {
            "Open": open_,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        },
        index=dates,
    )


@pytest.fixture
def synthetic_ohlcv_df() -> pd.DataFrame:
    return _make_synthetic_ohlcv()


@pytest.fixture
def synthetic_daily_returns() -> list[float]:
    rng = np.random.default_rng(99)
    returns = rng.normal(loc=0.0008, scale=0.01, size=252)
    return np.clip(returns, -0.05, 0.05).tolist()


@pytest.fixture
def mock_yfinance(monkeypatch: pytest.MonkeyPatch, synthetic_ohlcv_df: pd.DataFrame):
    import yfinance as yf

    class DummyTicker:
        def __init__(self, df: pd.DataFrame):
            self._df = df

        def history(self, *args, **kwargs):
            df = self._df
            start = kwargs.get("start")
            end = kwargs.get("end")
            period = kwargs.get("period")

            if start is not None:
                df = df[df.index >= pd.Timestamp(start)]
            if end is not None:
                df = df[df.index <= pd.Timestamp(end)]
            if period:
                try:
                    if str(period).endswith("d"):
                        days = int(str(period)[:-1])
                        df = df.tail(days)
                except ValueError:
                    pass

            return df.copy()

    monkeypatch.setattr(yf, "Ticker", lambda symbol: DummyTicker(synthetic_ohlcv_df))


@pytest.fixture
async def api_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

