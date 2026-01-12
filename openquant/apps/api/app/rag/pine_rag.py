"""
Pine Script RAG - Retrieval system for Pine Script code generation
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
import logging
import os


class PineScriptRAG:
    """
    RAG system for Pine Script code generation.
    Uses ChromaDB for vector storage and retrieval.
    """

    # Pine Script v5 documentation chunks
    PINE_DOCS = [
        {
            "id": "version_declaration",
            "content": "//@version=5 must be the first line of every Pine Script. Use indicator() for visual indicators, strategy() for backtestable strategies, library() for reusable code.",
            "metadata": {"category": "syntax", "importance": "critical"}
        },
        {
            "id": "strategy_declaration",
            "content": "strategy(title, overlay, initial_capital, default_qty_type, default_qty_value) declares a strategy. overlay=true plots on price chart, false creates separate pane.",
            "metadata": {"category": "strategy", "importance": "high"}
        },
        {
            "id": "indicator_declaration",
            "content": "indicator(title, overlay, format, precision) declares an indicator. format can be format.price, format.volume, format.percent.",
            "metadata": {"category": "indicator", "importance": "high"}
        },
        {
            "id": "strategy_entries",
            "content": "strategy.entry(id, direction, qty, limit, stop, comment) opens a position. direction is strategy.long or strategy.short. strategy.close(id) closes a position. strategy.close_all() closes all positions.",
            "metadata": {"category": "strategy", "importance": "high"}
        },
        {
            "id": "strategy_exits",
            "content": "strategy.exit(id, from_entry, qty, profit, loss, limit, stop, trail_price, trail_offset) sets exit conditions. profit/loss are in ticks, limit/stop are prices.",
            "metadata": {"category": "strategy", "importance": "high"}
        },
        {
            "id": "ta_indicators",
            "content": "ta.rsi(source, length) calculates RSI. ta.ema(source, length) calculates EMA. ta.sma(source, length) calculates SMA. ta.atr(length) calculates ATR. ta.macd(source, fast, slow, signal) returns [macdLine, signalLine, histogram].",
            "metadata": {"category": "indicators", "importance": "high"}
        },
        {
            "id": "ta_crossovers",
            "content": "ta.crossover(a, b) returns true when a crosses above b. ta.crossunder(a, b) returns true when a crosses below b. ta.cross(a, b) returns true on any cross.",
            "metadata": {"category": "indicators", "importance": "high"}
        },
        {
            "id": "ta_bands",
            "content": "ta.bb(source, length, mult) returns [middle, upper, lower] Bollinger Bands. ta.kc(source, length, mult) returns Keltner Channels.",
            "metadata": {"category": "indicators", "importance": "medium"}
        },
        {
            "id": "input_functions",
            "content": "input.int(defval, title, minval, maxval, step) for integers. input.float() for decimals. input.bool() for true/false. input.string() for text. input.source() for price source selection.",
            "metadata": {"category": "inputs", "importance": "high"}
        },
        {
            "id": "plotting",
            "content": "plot(value, title, color, linewidth, style) draws a line. plotshape(condition, style, location, color, text) draws shapes. hline(price, title, color) draws horizontal line.",
            "metadata": {"category": "plotting", "importance": "medium"}
        },
        {
            "id": "var_keyword",
            "content": "var declares a variable that persists across bars. Without var, variables reset each bar. varip persists even on real-time bar updates.",
            "metadata": {"category": "syntax", "importance": "medium"}
        },
        {
            "id": "na_handling",
            "content": "na is Pine Script's null value. na(x) checks if x is na. nz(x, y) returns y if x is na. fixnan(x) replaces na with last non-na value.",
            "metadata": {"category": "syntax", "importance": "medium"}
        },
        {
            "id": "arrays",
            "content": "array.new_float(size, initial_value) creates array. array.push(id, value) adds to end. array.get(id, index) retrieves value. array.set(id, index, value) sets value.",
            "metadata": {"category": "arrays", "importance": "medium"}
        },
        {
            "id": "conditionals",
            "content": "if condition ... else if ... else ... endif. Ternary: condition ? value_if_true : value_if_false. switch value case1 => result1 case2 => result2.",
            "metadata": {"category": "syntax", "importance": "high"}
        },
        {
            "id": "position_info",
            "content": "strategy.position_size returns current position size (positive=long, negative=short, 0=flat). strategy.position_avg_price returns average entry price.",
            "metadata": {"category": "strategy", "importance": "medium"}
        }
    ]

    # Example Pine Script strategies and indicators
    EXAMPLE_SCRIPTS = {
        "rsi_strategy": {
            "description": "RSI overbought/oversold strategy with crossover entries",
            "code": '''
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
        },
        "ema_crossover_atr": {
            "description": "EMA crossover strategy with ATR-based stop loss and take profit",
            "code": '''
//@version=5
strategy("EMA Cross with ATR Stop", overlay=true)

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
        },
        "bollinger_bands_indicator": {
            "description": "Bollinger Bands indicator with squeeze detection",
            "code": '''
//@version=5
indicator("Bollinger Bands with Squeeze", overlay=true)

// Inputs
length = input.int(20, "Length")
mult = input.float(2.0, "Multiplier")
kcLength = input.int(20, "KC Length")
kcMult = input.float(1.5, "KC Multiplier")

// Calculate Bollinger Bands
basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

// Calculate Keltner Channels for squeeze detection
kcBasis = ta.ema(close, kcLength)
kcRange = ta.atr(kcLength) * kcMult
kcUpper = kcBasis + kcRange
kcLower = kcBasis - kcRange

// Squeeze detection
sqzOn = lower > kcLower and upper < kcUpper
sqzOff = lower < kcLower and upper > kcUpper

// Plot
plot(basis, "Basis", color.orange)
p1 = plot(upper, "Upper", color.blue)
p2 = plot(lower, "Lower", color.blue)
fill(p1, p2, color=color.new(color.blue, 90))

// Squeeze indicator
bgcolor(sqzOn ? color.new(color.red, 90) : na)
'''
        },
        "macd_divergence": {
            "description": "MACD with histogram coloring and signal line crossovers",
            "code": '''
//@version=5
indicator("MACD Divergence", overlay=false)

// Inputs
fastLength = input.int(12, "Fast Length")
slowLength = input.int(26, "Slow Length")
signalLength = input.int(9, "Signal Length")
src = input.source(close, "Source")

// Calculate MACD
[macdLine, signalLine, histLine] = ta.macd(src, fastLength, slowLength, signalLength)

// Histogram color
histColor = histLine >= 0 ? (histLine > histLine[1] ? color.green : color.lime) : (histLine < histLine[1] ? color.red : color.orange)

// Plot
plot(histLine, "Histogram", color=histColor, style=plot.style_columns)
plot(macdLine, "MACD", color.blue)
plot(signalLine, "Signal", color.orange)
hline(0, "Zero", color.gray)

// Alerts
alertcondition(ta.crossover(macdLine, signalLine), "Bullish Cross", "MACD crossed above signal")
alertcondition(ta.crossunder(macdLine, signalLine), "Bearish Cross", "MACD crossed below signal")
'''
        },
        "volume_profile_strategy": {
            "description": "Volume spike detection strategy with relative volume",
            "code": '''
//@version=5
strategy("Volume Spike Strategy", overlay=true)

// Inputs
volLength = input.int(20, "Volume MA Length")
volThreshold = input.float(2.0, "Volume Spike Threshold")
priceLength = input.int(10, "Price MA Length")

// Calculate indicators
avgVolume = ta.sma(volume, volLength)
relativeVolume = volume / avgVolume
priceMA = ta.sma(close, priceLength)

// Conditions
volumeSpike = relativeVolume > volThreshold
priceAboveMA = close > priceMA
priceBelowMA = close < priceMA

// Entry conditions
longCondition = volumeSpike and priceAboveMA and close > open
shortCondition = volumeSpike and priceBelowMA and close < open

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

// Exit after 5 bars
if strategy.position_size != 0 and bar_index - strategy.opentrades.entry_bar_index(0) >= 5
    strategy.close_all()

// Plot
plot(priceMA, "Price MA", color.yellow)
bgcolor(volumeSpike ? color.new(color.blue, 90) : na)
'''
        },
        "support_resistance_breakout": {
            "description": "Support and resistance breakout strategy using pivot points",
            "code": '''
//@version=5
strategy("S/R Breakout Strategy", overlay=true)

// Inputs
leftBars = input.int(10, "Left Bars for Pivot")
rightBars = input.int(10, "Right Bars for Pivot")
atrPeriod = input.int(14, "ATR Period")
atrMult = input.float(1.0, "ATR Filter Multiplier")

// Calculate pivots
pivotHigh = ta.pivothigh(high, leftBars, rightBars)
pivotLow = ta.pivotlow(low, leftBars, rightBars)

// Store last pivot levels
var float resistanceLevel = na
var float supportLevel = na

if not na(pivotHigh)
    resistanceLevel := pivotHigh
if not na(pivotLow)
    supportLevel := pivotLow

// ATR filter
atrValue = ta.atr(atrPeriod)
minMove = atrValue * atrMult

// Breakout conditions
longBreakout = close > resistanceLevel + minMove and not na(resistanceLevel)
shortBreakout = close < supportLevel - minMove and not na(supportLevel)

// Execute trades
if longBreakout
    strategy.entry("Long", strategy.long)
    resistanceLevel := na  // Reset after breakout

if shortBreakout
    strategy.entry("Short", strategy.short)
    supportLevel := na  // Reset after breakout

// Plot levels
plot(resistanceLevel, "Resistance", color.red, style=plot.style_circles)
plot(supportLevel, "Support", color.green, style=plot.style_circles)
'''
        }
    }

    def __init__(self, persist_directory: str, collection_name: str):
        """
        Initialize Pine Script RAG system.

        Args:
            persist_directory: Directory for ChromaDB persistence
            collection_name: Name of the collection
        """
        self.logger = logging.getLogger(__name__)

        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        self.logger.info(f"PineScriptRAG initialized at {persist_directory}")

        # Seed collection if empty
        self._seed_collection()

    def _seed_collection(self):
        """Seed collection with Pine Script documentation and examples."""
        if self.collection.count() == 0:
            self.logger.info("Seeding Pine Script RAG collection...")

            # Add documentation chunks
            for doc in self.PINE_DOCS:
                self.collection.add(
                    ids=[doc["id"]],
                    documents=[doc["content"]],
                    metadatas=[doc["metadata"]]
                )

            # Add example scripts
            for name, data in self.EXAMPLE_SCRIPTS.items():
                self.collection.add(
                    ids=[f"example_{name}"],
                    documents=[f"{data['description']}\n\n{data['code']}"],
                    metadatas={"category": "example", "name": name}
                )

            self.logger.info(f"Seeded {self.collection.count()} documents")
        else:
            self.logger.info(f"Collection already has {self.collection.count()} documents")

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Retrieve relevant Pine Script context for a query.

        Args:
            query: Natural language query or description
            n_results: Number of results to return

        Returns:
            List of retrieved documents with content and metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        retrieved = []
        if results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                retrieved.append({
                    "content": doc,
                    "metadata": meta
                })

        return retrieved

    def add_example(self, name: str, description: str, code: str, metadata: Dict = None):
        """
        Add a new example to the collection.

        Args:
            name: Unique name for the example
            description: Description of what the script does
            code: Pine Script code
            metadata: Additional metadata
        """
        doc_id = f"user_example_{name}"
        content = f"{description}\n\n{code}"

        meta = {"category": "user_example", "name": name}
        if metadata:
            meta.update(metadata)

        # Check if exists
        existing = self.collection.get(ids=[doc_id])
        if existing["ids"]:
            # Update existing
            self.collection.update(
                ids=[doc_id],
                documents=[content],
                metadatas=[meta]
            )
        else:
            # Add new
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[meta]
            )

        self.logger.info(f"Added/updated example: {name}")

    def get_example_code(self, name: str) -> str:
        """
        Get example code by name.

        Args:
            name: Name of the example

        Returns:
            Pine Script code or empty string if not found
        """
        if name in self.EXAMPLE_SCRIPTS:
            return self.EXAMPLE_SCRIPTS[name]["code"]

        # Try to retrieve from collection
        results = self.collection.get(ids=[f"example_{name}", f"user_example_{name}"])
        if results["documents"]:
            # Extract code from document
            doc = results["documents"][0]
            if "\n\n" in doc:
                return doc.split("\n\n", 1)[1]
            return doc

        return ""
