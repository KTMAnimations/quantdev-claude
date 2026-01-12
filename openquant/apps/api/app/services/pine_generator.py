"""
Pine Script Generator Service - RAG-enhanced LLM code generation
"""
import re
import logging
from typing import Dict, Optional

from app.core.llm_service import LLMService
from app.rag.pine_rag import PineScriptRAG


class PineScriptGenerator:
    """
    RAG-enhanced Pine Script generator using LLM.
    Retrieves relevant examples and documentation before generating code.
    """

    SYSTEM_PROMPT = """You are an expert Pine Script v5 developer for TradingView.

Rules:
1. ALWAYS start with //@version=5
2. Use indicator() for visual tools, strategy() for backtestable systems
3. Include input() declarations for all configurable parameters
4. Handle na values with na() checks or nz() defaults
5. Use ta.* functions for indicators (ta.rsi, ta.ema, ta.atr, ta.macd, etc.)
6. For strategies: use strategy.entry(), strategy.close(), strategy.exit()
7. Add descriptive comments explaining the logic
8. Use meaningful variable names
9. Return ONLY the Pine Script code, no explanations or markdown

{context}

Generate complete, compilable Pine Script v5 code."""

    FIX_PROMPT = """You are a Pine Script debugging expert.

Fix this Pine Script compile error. Return ONLY the corrected code, no explanations.

Error: {error}

Code:
```pinescript
{code}
```

Corrected code:"""

    def __init__(self, llm_service: Optional[LLMService] = None, rag: Optional[PineScriptRAG] = None):
        """
        Initialize Pine Script Generator.

        Args:
            llm_service: LLM service for generation (optional, falls back to templates)
            rag: RAG system for context retrieval (optional)
        """
        self.llm = llm_service
        self.rag = rag
        self.logger = logging.getLogger(__name__)

    async def generate_pine_script(
        self,
        description: str,
        script_type: str = "strategy"
    ) -> Dict:
        """
        Generate Pine Script from natural language description.

        Args:
            description: Natural language description of the strategy/indicator
            script_type: "strategy" or "indicator"

        Returns:
            Dict with code, validation status, errors, and warnings
        """
        # Try LLM generation if available
        if self.llm:
            try:
                return await self._generate_with_llm(description, script_type)
            except Exception as e:
                self.logger.warning(f"LLM generation failed, falling back to templates: {e}")

        # Fallback to template-based generation
        return self._generate_from_template(description, script_type)

    async def _generate_with_llm(self, description: str, script_type: str) -> Dict:
        """Generate using LLM with RAG context."""

        # Retrieve relevant context from RAG
        context = ""
        if self.rag:
            retrieved = self.rag.retrieve(description, n_results=5)
            if retrieved:
                context = "Relevant Pine Script documentation and examples:\n\n"
                for i, doc in enumerate(retrieved, 1):
                    context += f"--- Example {i} ---\n{doc['content']}\n\n"

        # Build system prompt with context
        system_prompt = self.SYSTEM_PROMPT.format(
            context=context if context else "No additional context available."
        )

        # User prompt
        user_prompt = f"Create a {script_type} for: {description}"

        # Generate with LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        code = await self.llm.complete(messages, temperature=0.3)

        # Extract code from markdown if wrapped
        code = self._extract_code(code)

        # Validate syntax
        validation = self._validate_pine_syntax(code)

        return {
            "code": code.strip(),
            "is_valid": validation["is_valid"],
            "errors": validation["errors"],
            "warnings": validation["warnings"]
        }

    async def fix_compile_errors(
        self,
        code: str,
        error_message: str,
        max_iterations: int = 3
    ) -> Dict:
        """
        Iteratively fix Pine Script compile errors using LLM.

        Args:
            code: Original Pine Script code
            error_message: Compile error message
            max_iterations: Maximum fix attempts

        Returns:
            Dict with fixed code and validation status
        """
        if not self.llm:
            # Return as-is if no LLM
            return {
                "code": code.strip(),
                "is_valid": False,
                "errors": [error_message],
                "warnings": [],
                "iterations": 0
            }

        current_code = code
        current_error = error_message

        for iteration in range(max_iterations):
            try:
                messages = [
                    {"role": "system", "content": "You are a Pine Script debugging expert. Fix errors and return ONLY the corrected code."},
                    {"role": "user", "content": self.FIX_PROMPT.format(
                        error=current_error,
                        code=current_code
                    )}
                ]

                fixed_code = await self.llm.complete(messages, temperature=0.1)
                fixed_code = self._extract_code(fixed_code)

                validation = self._validate_pine_syntax(fixed_code)

                if validation["is_valid"]:
                    return {
                        "code": fixed_code.strip(),
                        "is_valid": True,
                        "errors": [],
                        "warnings": validation["warnings"],
                        "iterations": iteration + 1
                    }

                current_code = fixed_code
                current_error = "; ".join(validation["errors"])

            except Exception as e:
                self.logger.error(f"Error fixing code in iteration {iteration + 1}: {e}")
                break

        # Return last attempt
        validation = self._validate_pine_syntax(current_code)
        return {
            "code": current_code.strip(),
            "is_valid": validation["is_valid"],
            "errors": validation["errors"],
            "warnings": validation["warnings"],
            "iterations": max_iterations
        }

    def _generate_from_template(self, description: str, script_type: str) -> Dict:
        """Fallback template-based generation."""
        description_lower = description.lower()

        # Match to template based on description
        if "rsi" in description_lower:
            template = self._get_rsi_template(script_type)
        elif "ema" in description_lower or "crossover" in description_lower:
            template = self._get_ema_crossover_template(script_type)
        elif "bollinger" in description_lower:
            template = self._get_bollinger_template()
        elif "macd" in description_lower:
            template = self._get_macd_template(script_type)
        elif "volume" in description_lower:
            template = self._get_volume_template(script_type)
        else:
            template = self._get_generic_template(description, script_type)

        validation = self._validate_pine_syntax(template)

        return {
            "code": template.strip(),
            "is_valid": validation["is_valid"],
            "errors": validation["errors"],
            "warnings": validation["warnings"]
        }

    def _extract_code(self, text: str) -> str:
        """Extract code from markdown code blocks."""
        # Try to find Pine Script code block
        match = re.search(r'```(?:pinescript|pine)?\n?(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Try generic code block
        match = re.search(r'```\n?(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Return as-is
        return text.strip()

    def _validate_pine_syntax(self, code: str) -> Dict:
        """Basic Pine Script syntax validation."""
        errors = []
        warnings = []

        # Check version declaration
        if "//@version=5" not in code and "//@version=4" not in code:
            errors.append("Missing version declaration (//@version=5)")

        # Check for indicator or strategy declaration
        if "indicator(" not in code and "strategy(" not in code and "library(" not in code:
            errors.append("Missing indicator(), strategy(), or library() declaration")

        # Check matching parentheses
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")

        if code.count("[") != code.count("]"):
            errors.append("Mismatched brackets")

        # Check for common issues
        if "var " in code:
            var_idx = code.find("var ")
            next_50 = code[var_idx:var_idx + 50]
            if "=" not in next_50:
                warnings.append("'var' keyword may be incorrectly used")

        # Check for deprecated syntax
        if "study(" in code:
            warnings.append("'study()' is deprecated in Pine Script v5, use 'indicator()' instead")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    # Template methods
    def _get_rsi_template(self, script_type: str) -> str:
        return '''
//@version=5
strategy("RSI Strategy", overlay=false)

// Inputs
rsiLength = input.int(14, "RSI Length", minval=1)
overbought = input.int(70, "Overbought Level")
oversold = input.int(30, "Oversold Level")

// Calculate RSI
rsiValue = ta.rsi(close, rsiLength)

// Entry conditions
longCondition = ta.crossover(rsiValue, oversold)
shortCondition = ta.crossunder(rsiValue, overbought)

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

// Plot
plot(rsiValue, "RSI", color.purple)
hline(overbought, "Overbought", color.red)
hline(oversold, "Oversold", color.green)
'''

    def _get_ema_crossover_template(self, script_type: str) -> str:
        return '''
//@version=5
strategy("EMA Crossover Strategy", overlay=true)

// Inputs
fastLength = input.int(9, "Fast EMA")
slowLength = input.int(21, "Slow EMA")
atrLength = input.int(14, "ATR Length")
atrMultiplier = input.float(2.0, "ATR Multiplier")

// Calculate indicators
fastEMA = ta.ema(close, fastLength)
slowEMA = ta.ema(close, slowLength)
atrValue = ta.atr(atrLength)

// Entry conditions
longCondition = ta.crossover(fastEMA, slowEMA)
shortCondition = ta.crossunder(fastEMA, slowEMA)

// Position management
if longCondition
    stopLoss = close - atrValue * atrMultiplier
    takeProfit = close + atrValue * atrMultiplier * 2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=stopLoss, limit=takeProfit)

if shortCondition
    stopLoss = close + atrValue * atrMultiplier
    takeProfit = close - atrValue * atrMultiplier * 2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=stopLoss, limit=takeProfit)

// Plot
plot(fastEMA, "Fast EMA", color.blue)
plot(slowEMA, "Slow EMA", color.orange)
'''

    def _get_bollinger_template(self) -> str:
        return '''
//@version=5
indicator("Bollinger Bands", overlay=true)

// Inputs
length = input.int(20, "Length")
mult = input.float(2.0, "Multiplier")

// Calculate Bollinger Bands
basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

// Plot
plot(basis, "Basis", color.orange)
p1 = plot(upper, "Upper", color.blue)
p2 = plot(lower, "Lower", color.blue)
fill(p1, p2, color=color.new(color.blue, 90))
'''

    def _get_macd_template(self, script_type: str) -> str:
        return '''
//@version=5
indicator("MACD", overlay=false)

// Inputs
fastLength = input.int(12, "Fast Length")
slowLength = input.int(26, "Slow Length")
signalLength = input.int(9, "Signal Length")

// Calculate MACD
[macdLine, signalLine, histLine] = ta.macd(close, fastLength, slowLength, signalLength)

// Histogram color
histColor = histLine >= 0 ? (histLine > histLine[1] ? color.green : color.lime) : (histLine < histLine[1] ? color.red : color.orange)

// Plot
plot(histLine, "Histogram", color=histColor, style=plot.style_columns)
plot(macdLine, "MACD", color.blue)
plot(signalLine, "Signal", color.orange)
hline(0, "Zero", color.gray)
'''

    def _get_volume_template(self, script_type: str) -> str:
        return '''
//@version=5
strategy("Volume Spike Strategy", overlay=true)

// Inputs
volLength = input.int(20, "Volume MA Length")
volThreshold = input.float(2.0, "Volume Spike Threshold")

// Calculate indicators
avgVolume = ta.sma(volume, volLength)
relativeVolume = volume / avgVolume

// Conditions
volumeSpike = relativeVolume > volThreshold
bullishBar = close > open
bearishBar = close < open

// Entry conditions
longCondition = volumeSpike and bullishBar
shortCondition = volumeSpike and bearishBar

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

// Exit after 5 bars
if strategy.position_size != 0 and bar_index - strategy.opentrades.entry_bar_index(0) >= 5
    strategy.close_all()

// Plot volume spike background
bgcolor(volumeSpike ? color.new(color.blue, 90) : na)
'''

    def _get_generic_template(self, description: str, script_type: str) -> str:
        declaration = "strategy" if script_type == "strategy" else "indicator"
        overlay = "true" if script_type == "strategy" else "false"
        title = description[:50] if len(description) > 50 else description

        if script_type == "strategy":
            trade_logic = '''
// Execute trades
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)
'''
        else:
            trade_logic = '''
// Plot signals
plotshape(longCondition, style=shape.triangleup, location=location.belowbar, color=color.green)
plotshape(shortCondition, style=shape.triangledown, location=location.abovebar, color=color.red)
'''

        return f'''
//@version=5
{declaration}("{title}", overlay={overlay})

// Generated by OpenQuant
// Description: {description}

// Inputs
length = input.int(14, "Period", minval=1)
threshold = input.float(50.0, "Threshold")

// Calculate indicator
value = ta.sma(close, length)

// Conditions
longCondition = ta.crossover(close, value)
shortCondition = ta.crossunder(close, value)

{trade_logic}
// Plot
plot(value, "Signal", color.purple)
'''
