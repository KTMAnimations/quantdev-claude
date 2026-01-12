"""
Pine Script Generator API Router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PineScriptRequest, PineScriptResponse, PineScriptFixRequest
from app.services.pine_generator import PineScriptGenerator

router = APIRouter()


def get_pine_service():
    """Get Pine Script Generator with LLM and RAG services"""
    from app.main import get_llm_service, get_pine_rag
    return PineScriptGenerator(
        llm_service=get_llm_service(),
        rag=get_pine_rag()
    )


@router.post("/generate", response_model=PineScriptResponse)
async def generate_pine_script(request: PineScriptRequest):
    """
    Generate Pine Script from natural language description.

    Uses RAG to retrieve relevant examples and LLM to generate code.
    Falls back to templates if LLM is unavailable.
    """
    try:
        pine_service = get_pine_service()
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
    Fix Pine Script compile errors using LLM.

    Iteratively attempts to fix errors up to 3 times.
    """
    try:
        pine_service = get_pine_service()
        result = await pine_service.fix_compile_errors(
            code=request.code,
            error_message=request.error_message
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_pine_script(request: dict):
    """
    Validate Pine Script syntax.
    """
    code = request.get("code", "")
    pine_service = get_pine_service()
    validation = pine_service._validate_pine_syntax(code)
    return validation


@router.get("/templates")
async def get_pine_templates():
    """
    Get available Pine Script templates.
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
                "name": "MACD",
                "type": "indicator",
                "description": "MACD with histogram coloring"
            },
            {
                "name": "Volume Spike",
                "type": "strategy",
                "description": "Volume spike detection strategy"
            }
        ]
    }


@router.get("/examples/{name}")
async def get_pine_example(name: str):
    """
    Get a specific Pine Script example by name.
    """
    from app.main import get_pine_rag
    rag = get_pine_rag()

    if rag:
        code = rag.get_example_code(name)
        if code:
            return {"name": name, "code": code}

    raise HTTPException(status_code=404, detail=f"Example '{name}' not found")
