import numpy as np
import pytest

from app.models.schemas import PropFirmType
from app.services.prop_firm_simulator import PropFirmSimulator


@pytest.mark.anyio
async def test_prop_firm_simulator_ftmo(synthetic_daily_returns):
    sim = PropFirmSimulator(n_simulations=200)
    result = await sim.simulate_challenge(
        daily_returns=np.array(synthetic_daily_returns),
        prop_firm=PropFirmType.FTMO,
    )
    assert result["prop_firm"] == "FTMO"
    assert 0.0 <= result["combined_pass_rate"] <= 1.0
    assert "expected_value" in result
    assert "recommendation" in result["expected_value"]


@pytest.mark.anyio
async def test_prop_firm_simulator_unsupported_raises(synthetic_daily_returns):
    sim = PropFirmSimulator(n_simulations=10)
    with pytest.raises(ValueError, match="Unsupported prop firm"):
        await sim.simulate_challenge(
            daily_returns=np.array(synthetic_daily_returns),
            prop_firm=PropFirmType.MFF,
        )

