"""
Pine Script Generator API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PineScriptRequest, PineScriptResponse, PineScriptFixRequest
from app.services.pine_generator import PineScriptGenerator

router = APIRouter()
pine_service = PineScriptGenerator()


@router.post("/generate", response_model=PineScriptResponse)
async def generate_pine_script(request: PineScriptRequest):
    """
    Generate Pine Script from natural language description
    """
    try:
        result = await pine_service.generate_pine_script(
            description=request.description,
            script_type=request.script_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix", response_model=PineScriptResponse)
async def fix_pine_script(request: PineScriptFixRequest):
    """
    Fix Pine Script compile errors
    """
    try:
        result = await pine_service.fix_compile_errors(
            code=request.code,
            error_message=request.error_message
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_pine_script(code: str):
    """
    Validate Pine Script syntax
    """
    validation = pine_service._validate_pine_syntax(code)
    return validation


@router.get("/templates")
async def get_pine_templates():
    """
    Get Pine Script templates
    """
    return {
        "templates": [
            {
                "name": "RSI Strategy",
                "type": "strategy",
                "description": "Basic RSI overbought/oversold strategy"
            },
            {
                "name": "EMA Crossover",
                "type": "strategy",
                "description": "Moving average crossover with ATR stops"
            },
            {
                "name": "Bollinger Bands",
                "type": "indicator",
                "description": "Bollinger Bands with custom settings"
            },
            {
                "name": "VWAP Deviation",
                "type": "indicator",
                "description": "VWAP with standard deviation bands"
            }
        ]
    }
