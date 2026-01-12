"""
Pydantic models for API request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Edge Discovery Schemas
class EdgeAnalysisRequest(BaseModel):
    description: str = Field(..., description="Natural language description of the trading feature")
    symbol: str = Field(default="SPY", description="Trading symbol to analyze")
    timeframe: str = Field(default="1D", description="Timeframe for analysis")
    lookback_days: int = Field(default=252, description="Number of days to look back")


class StatisticalSignificance(BaseModel):
    correlation_1d: float
    correlation_5d: float
    ic_mean: float
    ic_std: float
    ic_ir: float
    t_statistic: float
    p_value: float
    is_significant: bool
    quantile_returns: Dict[str, Any]


class MLImportance(BaseModel):
    cv_accuracy: float
    cv_std: float
    feature_importance: Dict[str, float]
    has_predictive_power: bool
    shap_summary: Optional[Dict[str, Any]] = None


class ConfidenceIntervals(BaseModel):
    mean_return: float
    ci_lower_95: float
    ci_upper_95: float
    ci_lower_99: float
    ci_upper_99: float
    probability_positive: float


class ParsedFeatureLogic(BaseModel):
    type: str
    confidence: float
    source: str  # "llm" or "pattern"
    # Additional parameters are dynamic based on feature type


class EdgeAnalysisResponse(BaseModel):
    feature_name: str
    parsed_logic: Optional[Dict[str, Any]] = None
    statistical_significance: StatisticalSignificance
    ml_importance: MLImportance
    confidence_intervals: ConfidenceIntervals
    recommendation: str


# Monte Carlo Schemas
class TradeData(BaseModel):
    entry_time: datetime
    exit_time: datetime
    pnl: float
    return_pct: float


class MonteCarloRequest(BaseModel):
    trades: List[TradeData]
    n_simulations: int = Field(default=10000, description="Number of simulations")


class PercentileData(BaseModel):
    p5: float
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float
    p95: float
    p99: float


class BootstrapResult(BaseModel):
    sharpe_ratio: Dict[str, Any]
    profit_factor: Dict[str, Any]
    win_rate: Dict[str, Any]
    expectancy: Dict[str, Any]


class MonteCarloSummary(BaseModel):
    verdict: str
    verdict_color: str
    description: str
    edge_score: int
    key_metrics: Dict[str, Any]


class MonteCarloResponse(BaseModel):
    shuffle_trades: Dict[str, Any]
    bootstrap: BootstrapResult
    random_entry: Dict[str, Any]
    drawdown_distribution: Dict[str, Any]
    risk_of_ruin: Dict[str, Any]
    expectancy_ci: Dict[str, Any]
    summary: MonteCarloSummary


# Pine Script Schemas
class PineScriptRequest(BaseModel):
    description: str = Field(..., description="Natural language description of the strategy")
    script_type: str = Field(default="strategy", description="'strategy' or 'indicator'")


class PineScriptResponse(BaseModel):
    code: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class PineScriptFixRequest(BaseModel):
    code: str
    error_message: str


# Prop Firm Schemas
class PropFirmType(str, Enum):
    FTMO = "ftmo"
    THE5ERS = "the5ers"
    APEX = "apex"
    TOPSTEP = "topstep"
    MFF = "mff"
    E8 = "e8"


class PropFirmRequest(BaseModel):
    daily_returns: List[float]
    prop_firm: PropFirmType
    n_simulations: int = Field(default=10000)


class PropFirmPhaseResult(BaseModel):
    pass_rate: float
    fail_rate: float
    fail_reasons: Dict[str, float]
    avg_days_to_pass: Optional[float]
    days_to_pass_distribution: Dict[str, Optional[float]]


class PropFirmExpectedValue(BaseModel):
    expected_value: float
    roi: float
    break_even_pass_rate: float
    current_pass_rate: float
    edge_over_break_even: float
    recommendation: Dict[str, str]


class PropFirmResponse(BaseModel):
    prop_firm: str
    account_size: float
    challenge_cost: float
    phase1: PropFirmPhaseResult
    phase2: Optional[PropFirmPhaseResult]
    combined_pass_rate: float
    funded_simulation: Dict[str, Any]
    expected_value: PropFirmExpectedValue


# Backtest Schemas
class BacktestRequest(BaseModel):
    strategy_code: str
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = Field(default=10000)


class BacktestResponse(BaseModel):
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    trades: List[TradeData]
    equity_curve: List[Dict[str, Any]]
