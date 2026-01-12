"""
Chat Router - Streaming chat endpoint for Quant Copilot
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str  # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    """Chat request payload."""
    messages: List[ChatMessage]
    stream: bool = True
    temperature: Optional[float] = None


QUANT_SYSTEM_PROMPT = """You are an expert quantitative trading assistant for OpenQuant, a professional trading platform. You help traders with:

1. **Strategy Development**: Designing trading strategies, entry/exit rules, position sizing, risk management
2. **Statistical Analysis**: Sharpe ratio, Sortino ratio, maximum drawdown, win rate, profit factor, expectancy
3. **Pine Script**: Writing and debugging TradingView Pine Script v5 code for strategies and indicators
4. **Risk Management**: Kelly criterion, Value at Risk (VaR), position sizing, portfolio allocation
5. **Backtesting**: Avoiding overfitting, walk-forward analysis, out-of-sample testing, Monte Carlo simulation
6. **Technical Analysis**: Technical indicators (RSI, MACD, Bollinger Bands, etc.), chart patterns, support/resistance
7. **Prop Firm Trading**: Challenge strategies, drawdown management, consistency rules

Guidelines:
- Provide specific, actionable advice with concrete examples
- Include formulas and calculations when relevant (use proper notation)
- Warn about common pitfalls: overfitting, data snooping, survivorship bias, curve fitting
- Be concise but thorough - traders value time efficiency
- When discussing Pine Script, always use v5 syntax
- For risk metrics, explain what the numbers mean practically
- If asked about specific strategies, discuss both potential advantages AND risks

You have access to OpenQuant's features:
- Edge Discovery: Analyze trading features for statistical significance
- Pine Script Generator: Convert natural language to TradingView code
- Monte Carlo Testing: Bootstrap analysis of backtest results
- Prop Firm Simulator: Simulate challenge pass rates

Always be professional and objective. Avoid overpromising returns - trading involves substantial risk."""


async def get_llm_service():
    """Dependency to get LLM service."""
    from app.core.config import get_settings
    from app.core.llm_service import LLMService

    settings = get_settings()
    return LLMService(settings)


@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    llm=Depends(get_llm_service)
):
    """
    Chat endpoint with optional streaming.

    Supports both streaming (SSE) and non-streaming responses.
    """
    # Build messages with system prompt
    messages = [{"role": "system", "content": QUANT_SYSTEM_PROMPT}]
    messages.extend([{"role": m.role, "content": m.content} for m in request.messages])

    if request.stream:
        # Streaming response using Server-Sent Events
        async def generate():
            try:
                async for chunk in llm.stream(messages, temperature=request.temperature):
                    # Format as SSE
                    data = json.dumps({"content": chunk})
                    yield f"data: {data}\n\n"

                # Send completion signal
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Chat streaming error: {e}")
                error_data = json.dumps({"error": str(e)})
                yield f"data: {error_data}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
    else:
        # Non-streaming response
        try:
            response = await llm.complete(messages, temperature=request.temperature)
            return {"content": response}
        except Exception as e:
            logger.error(f"Chat completion error: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def chat_health(llm=Depends(get_llm_service)):
    """
    Check if chat/LLM service is available.
    """
    from app.core.config import get_settings

    settings = get_settings()

    try:
        is_healthy = await llm.health_check()
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "base_url": settings.llm_base_url if settings.llm_provider == "chatmock" else "OpenAI API"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "provider": settings.llm_provider
        }


@router.post("/suggest")
async def suggest_questions(llm=Depends(get_llm_service)):
    """
    Get suggested questions based on context.
    """
    suggestions = [
        "How do I calculate the Sharpe ratio for my strategy?",
        "Explain the Kelly criterion for position sizing",
        "What is a good win rate for a scalping strategy?",
        "How do I avoid overfitting in backtests?",
        "Write a Pine Script for RSI divergence",
        "What's a safe daily drawdown limit for prop firm trading?",
        "How do I interpret Monte Carlo simulation results?",
        "Explain the difference between Sharpe and Sortino ratios",
    ]
    return {"suggestions": suggestions}
