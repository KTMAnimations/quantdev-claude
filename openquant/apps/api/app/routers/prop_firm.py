"""
Prop Firm Simulator API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PropFirmRequest, PropFirmResponse, PropFirmType
from app.services.prop_firm_simulator import PropFirmSimulator
import numpy as np

router = APIRouter()


@router.post("/simulate", response_model=PropFirmResponse)
async def simulate_prop_firm(request: PropFirmRequest):
    """
    Simulate prop firm challenge pass rates
    """
    try:
        daily_returns = np.array(request.daily_returns)
        prop_service = PropFirmSimulator(n_simulations=request.n_simulations)
        result = await prop_service.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=request.prop_firm,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/firms")
async def get_prop_firms():
    """
    Get supported prop firm configurations
    """
    return {
        "firms": [
            {
                "id": "ftmo",
                "name": "FTMO",
                "account_sizes": [10000, 25000, 50000, 100000, 200000],
                "challenge_cost": {"100k": 540},
                "profit_target_phase1": 0.10,
                "profit_target_phase2": 0.05,
                "max_daily_dd": 0.05,
                "max_total_dd": 0.10,
                "profit_split": 0.80
            },
            {
                "id": "the5ers",
                "name": "The5%ers",
                "account_sizes": [6000, 20000, 60000, 100000],
                "challenge_cost": {"100k": 235},
                "profit_target_phase1": 0.08,
                "profit_target_phase2": 0.05,
                "max_daily_dd": 0.05,
                "max_total_dd": 0.10,
                "profit_split": 0.80
            },
            {
                "id": "apex",
                "name": "Apex Trader Funding",
                "account_sizes": [25000, 50000, 100000, 150000, 250000],
                "challenge_cost": {"100k": 167},
                "profit_target_phase1": 0.06,
                "profit_target_phase2": 0.00,
                "max_daily_dd": 0.00,
                "max_total_dd": 0.03,
                "profit_split": 0.90,
                "trailing_drawdown": True
            },
            {
                "id": "e8",
                "name": "E8 Markets",
                "account_sizes": [25000, 50000, 100000, 250000],
                "challenge_cost": {"100k": 228},
                "profit_target_phase1": 0.08,
                "profit_target_phase2": 0.05,
                "max_daily_dd": 0.05,
                "max_total_dd": 0.08,
                "profit_split": 0.80
            }
        ]
    }


@router.get("/comparison")
async def compare_prop_firms():
    """
    Compare prop firms side by side
    """
    return {
        "comparison": {
            "headers": ["Firm", "Cost ($100k)", "Phase 1 Target", "Max Daily DD", "Max Total DD", "Profit Split"],
            "rows": [
                ["FTMO", "$540", "10%", "5%", "10%", "80%"],
                ["The5%ers", "$235", "8%", "5%", "10%", "80%"],
                ["Apex", "$167", "6%", "None", "3% (trailing)", "90%"],
                ["E8", "$228", "8%", "5%", "8%", "80%"]
            ]
        }
    }
