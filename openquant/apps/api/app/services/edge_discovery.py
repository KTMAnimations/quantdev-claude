"""
Edge Discovery Service - Replicates QuantPad's edge discovery using Alphalens + ML
Enhanced with LLM-powered feature parsing
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from typing import Dict, Optional
import yfinance as yf
import logging
import json

from app.core.llm_service import LLMService


class EdgeDiscoveryService:
    """
    Replicates QuantPad's edge discovery using Alphalens + custom ML.
    Enhanced with LLM for natural language feature parsing.
    """

    FEATURE_PARSE_PROMPT = """Parse this trading feature description into structured logic.

Description: {description}

Return a JSON object with:
{{
    "type": "rsi" | "ema" | "macd" | "bollinger" | "volume_spike" | "momentum" | "atr" | "stochastic" | "custom",
    "parameters": {{
        // indicator-specific parameters like period, threshold, etc.
    }},
    "conditions": {{
        "entry_long": "condition description (optional)",
        "entry_short": "condition description (optional)",
        "exit": "condition description (optional)"
    }},
    "confidence": 0.0-1.0  // how confident you are in parsing this
}}

Examples:
- "RSI below 30" -> {{"type": "rsi", "parameters": {{"period": 14}}, "conditions": {{"entry_long": "rsi < 30"}}, "confidence": 0.95}}
- "20 EMA crosses above 50 EMA" -> {{"type": "ema", "parameters": {{"fast": 20, "slow": 50}}, "conditions": {{"entry_long": "crossover(ema_fast, ema_slow)"}}, "confidence": 0.9}}
- "Volume 2x above average with price breakout" -> {{"type": "volume_spike", "parameters": {{"threshold": 2.0, "lookback": 20}}, "conditions": {{"entry_long": "volume > 2 * avg_volume and close > high[1]"}}, "confidence": 0.85}}

Return ONLY the JSON object, no additional text."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize Edge Discovery Service.

        Args:
            llm_service: Optional LLM service for feature parsing
        """
        self.llm = llm_service
        self.tscv = TimeSeriesSplit(n_splits=5)
        self.logger = logging.getLogger(__name__)

    async def analyze_feature(
        self,
        feature_description: str,
        symbol: str,
        timeframe: str,
        lookback_days: int = 252
    ) -> Dict:
        """
        Main entry point - analyzes a trading feature/signal.

        Args:
            feature_description: Natural language description of the feature
            symbol: Trading symbol (e.g., "SPY", "AAPL")
            timeframe: Timeframe (e.g., "1d", "1h")
            lookback_days: Number of days of historical data

        Returns:
            Dict with analysis results
        """
        # 1. Parse natural language to feature logic
        feature_logic = await self._parse_feature_description(feature_description)

        # 2. Fetch historical data
        price_data = await self._fetch_data(symbol, timeframe, lookback_days)

        # 3. Compute the feature
        feature_values = self._compute_feature(price_data, feature_logic)

        # 4. Run statistical analysis
        stats_results = self._run_statistical_tests(feature_values, price_data)

        # 5. Run ML analysis for non-linear patterns
        ml_results = self._run_ml_analysis(feature_values, price_data)

        # 6. Compute confidence intervals via bootstrap
        bootstrap_results = self._bootstrap_analysis(feature_values, price_data)

        return {
            "feature_name": feature_description,
            "parsed_logic": feature_logic,
            "statistical_significance": stats_results,
            "ml_importance": ml_results,
            "confidence_intervals": bootstrap_results,
            "recommendation": self._generate_recommendation(stats_results, ml_results)
        }

    async def _parse_feature_description(self, description: str) -> Dict:
        """
        Parse natural language to feature logic.
        Uses LLM if available, falls back to pattern matching.
        """
        # Try LLM parsing first
        if self.llm:
            try:
                messages = [
                    {"role": "system", "content": "You are a quantitative trading expert. Parse feature descriptions into structured JSON logic. Return ONLY valid JSON."},
                    {"role": "user", "content": self.FEATURE_PARSE_PROMPT.format(description=description)}
                ]

                result = await self.llm.complete(messages, temperature=0.1, json_mode=True)

                # Parse JSON response
                parsed = json.loads(result)

                # Validate parsed result has required fields
                if "type" in parsed and "parameters" in parsed:
                    self.logger.info(f"LLM parsed feature: {parsed['type']} with confidence {parsed.get('confidence', 'N/A')}")
                    return {
                        "type": parsed["type"],
                        **parsed.get("parameters", {}),
                        "conditions": parsed.get("conditions", {}),
                        "confidence": parsed.get("confidence", 0.8),
                        "source": "llm"
                    }
            except json.JSONDecodeError as e:
                self.logger.warning(f"LLM returned invalid JSON: {e}")
            except Exception as e:
                self.logger.warning(f"LLM parsing failed: {e}")

        # Fallback to pattern matching
        return self._pattern_match_feature(description)

    def _pattern_match_feature(self, description: str) -> Dict:
        """Fallback pattern matching for feature parsing."""
        description_lower = description.lower()

        if "rsi" in description_lower:
            # Extract period if mentioned
            import re
            period_match = re.search(r'(\d+)\s*(?:period|day|bar)', description_lower)
            period = int(period_match.group(1)) if period_match else 14

            return {
                "type": "rsi",
                "period": period,
                "confidence": 0.6,
                "source": "pattern"
            }

        elif "ema" in description_lower or "moving average" in description_lower:
            # Try to extract periods
            import re
            periods = re.findall(r'(\d+)\s*(?:ema|ma|period|day)', description_lower)
            if len(periods) >= 2:
                fast, slow = sorted([int(p) for p in periods[:2]])
            else:
                fast, slow = 9, 21

            return {
                "type": "ema",
                "fast": fast,
                "slow": slow,
                "confidence": 0.6,
                "source": "pattern"
            }

        elif "macd" in description_lower:
            return {
                "type": "macd",
                "fast": 12,
                "slow": 26,
                "signal": 9,
                "confidence": 0.7,
                "source": "pattern"
            }

        elif "volume" in description_lower:
            # Extract threshold if mentioned
            import re
            threshold_match = re.search(r'(\d+(?:\.\d+)?)\s*[x×]', description_lower)
            threshold = float(threshold_match.group(1)) if threshold_match else 2.0

            return {
                "type": "volume_spike",
                "threshold": threshold,
                "lookback": 20,
                "confidence": 0.6,
                "source": "pattern"
            }

        elif "bollinger" in description_lower:
            return {
                "type": "bollinger",
                "period": 20,
                "std": 2,
                "confidence": 0.7,
                "source": "pattern"
            }

        elif "atr" in description_lower:
            return {
                "type": "atr",
                "period": 14,
                "confidence": 0.6,
                "source": "pattern"
            }

        elif "stochastic" in description_lower or "stoch" in description_lower:
            return {
                "type": "stochastic",
                "k_period": 14,
                "d_period": 3,
                "confidence": 0.6,
                "source": "pattern"
            }

        else:
            return {
                "type": "momentum",
                "period": 10,
                "confidence": 0.3,
                "source": "pattern"
            }

    async def _fetch_data(self, symbol: str, timeframe: str, lookback_days: int) -> pd.DataFrame:
        """Fetch historical data using yfinance."""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=f"{lookback_days}d")
            data.columns = data.columns.str.lower()
            return data
        except Exception as e:
            self.logger.error(f"Failed to fetch data for {symbol}: {e}")
            raise

    def _compute_feature(self, price_data: pd.DataFrame, feature_logic: Dict) -> pd.Series:
        """Compute the feature based on parsed logic."""
        feature_type = feature_logic.get("type", "momentum")

        if feature_type == "rsi":
            period = feature_logic.get("period", 14)
            delta = price_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))

        elif feature_type == "ema":
            fast = feature_logic.get("fast", 9)
            slow = feature_logic.get("slow", 21)
            fast_ema = price_data['close'].ewm(span=fast).mean()
            slow_ema = price_data['close'].ewm(span=slow).mean()
            return fast_ema - slow_ema

        elif feature_type == "macd":
            fast = feature_logic.get("fast", 12)
            slow = feature_logic.get("slow", 26)
            fast_ema = price_data['close'].ewm(span=fast).mean()
            slow_ema = price_data['close'].ewm(span=slow).mean()
            return fast_ema - slow_ema

        elif feature_type == "volume_spike":
            threshold = feature_logic.get("threshold", 2.0)
            lookback = feature_logic.get("lookback", 20)
            avg_volume = price_data['volume'].rolling(lookback).mean()
            return price_data['volume'] / avg_volume

        elif feature_type == "bollinger":
            period = feature_logic.get("period", 20)
            std_dev = feature_logic.get("std", 2)
            ma = price_data['close'].rolling(period).mean()
            std = price_data['close'].rolling(period).std()
            return (price_data['close'] - ma) / (std * std_dev)

        elif feature_type == "atr":
            period = feature_logic.get("period", 14)
            high_low = price_data['high'] - price_data['low']
            high_close = abs(price_data['high'] - price_data['close'].shift())
            low_close = abs(price_data['low'] - price_data['close'].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            return tr.rolling(period).mean()

        elif feature_type == "stochastic":
            k_period = feature_logic.get("k_period", 14)
            lowest_low = price_data['low'].rolling(k_period).min()
            highest_high = price_data['high'].rolling(k_period).max()
            return 100 * (price_data['close'] - lowest_low) / (highest_high - lowest_low)

        else:  # momentum
            period = feature_logic.get("period", 10)
            return price_data['close'].pct_change(period)

    def _run_statistical_tests(self, feature: pd.Series, prices: pd.DataFrame) -> Dict:
        """Run comprehensive statistical tests on the feature."""
        # Forward returns
        returns_1d = prices['close'].pct_change(1).shift(-1)
        returns_5d = prices['close'].pct_change(5).shift(-5)

        # Clean data
        mask = ~(feature.isna() | returns_1d.isna())
        feature_clean = feature[mask]
        returns_1d_clean = returns_1d[mask]
        returns_5d_clean = returns_5d[mask & ~returns_5d.isna()]

        if len(feature_clean) < 30:
            return {
                "error": "Insufficient data for statistical analysis",
                "correlation_1d": 0.0,
                "correlation_5d": 0.0,
                "ic_mean": 0.0,
                "ic_std": 0.0,
                "ic_ir": 0.0,
                "t_statistic": 0.0,
                "p_value": 1.0,
                "is_significant": False,
                "quantile_returns": {}
            }

        # Correlation analysis
        correlation_1d = feature_clean.corr(returns_1d_clean)
        correlation_5d = feature_clean[:len(returns_5d_clean)].corr(returns_5d_clean) if len(returns_5d_clean) > 0 else 0.0

        # Information Coefficient (IC)
        ic_mean, ic_std = self._calculate_ic(feature_clean, returns_1d_clean)

        # T-test for signal vs no-signal periods
        median_feature = feature_clean.median()
        signal_returns = returns_1d_clean[feature_clean > median_feature]
        no_signal_returns = returns_1d_clean[feature_clean <= median_feature]

        if len(signal_returns) > 1 and len(no_signal_returns) > 1:
            t_stat, p_value = stats.ttest_ind(signal_returns.dropna(), no_signal_returns.dropna())
        else:
            t_stat, p_value = 0.0, 1.0

        # Quantile analysis
        quantile_returns = self._quantile_analysis(feature_clean, returns_1d_clean)

        return {
            "correlation_1d": float(correlation_1d) if not np.isnan(correlation_1d) else 0.0,
            "correlation_5d": float(correlation_5d) if not np.isnan(correlation_5d) else 0.0,
            "ic_mean": float(ic_mean),
            "ic_std": float(ic_std),
            "ic_ir": float(ic_mean / ic_std) if ic_std > 0 else 0.0,
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "is_significant": p_value < 0.05,
            "quantile_returns": quantile_returns
        }

    def _run_ml_analysis(self, feature: pd.Series, prices: pd.DataFrame) -> Dict:
        """Use ML to detect non-linear patterns."""
        # Create feature matrix with lagged values
        X = self._create_feature_matrix(feature, prices)
        y = (prices['close'].pct_change(1).shift(-1) > 0).astype(int)

        # Align and clean data
        mask = ~(X.isna().any(axis=1) | y.isna())
        X_clean = X[mask]
        y_clean = y[mask]

        if len(X_clean) < 100:
            return {
                "cv_accuracy": 0.5,
                "cv_std": 0.0,
                "feature_importance": {},
                "has_predictive_power": False,
                "shap_summary": None
            }

        # Train Random Forest with cross-validation
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

        cv_scores = []
        for train_idx, test_idx in self.tscv.split(X_clean):
            model.fit(X_clean.iloc[train_idx], y_clean.iloc[train_idx])
            score = model.score(X_clean.iloc[test_idx], y_clean.iloc[test_idx])
            cv_scores.append(score)

        # Feature importance
        model.fit(X_clean, y_clean)
        importance = dict(zip(X_clean.columns, model.feature_importances_.tolist()))

        return {
            "cv_accuracy": float(np.mean(cv_scores)),
            "cv_std": float(np.std(cv_scores)),
            "feature_importance": importance,
            "has_predictive_power": np.mean(cv_scores) > 0.52,
            "shap_summary": None  # Would compute SHAP in production
        }

    def _bootstrap_analysis(
        self,
        feature: pd.Series,
        prices: pd.DataFrame,
        n_iterations: int = 10000
    ) -> Dict:
        """Bootstrap confidence intervals for expectancy."""
        returns = prices['close'].pct_change(1).shift(-1)

        # Signal-based returns
        signal_mask = feature > feature.median()
        signal_returns = returns[signal_mask].dropna().values

        if len(signal_returns) < 10:
            return {
                "mean_return": 0.0,
                "ci_lower_95": 0.0,
                "ci_upper_95": 0.0,
                "ci_lower_99": 0.0,
                "ci_upper_99": 0.0,
                "probability_positive": 0.5
            }

        # Bootstrap
        bootstrap_means = []
        for _ in range(n_iterations):
            sample = np.random.choice(signal_returns, size=len(signal_returns), replace=True)
            bootstrap_means.append(np.mean(sample))

        bootstrap_means = np.array(bootstrap_means)

        return {
            "mean_return": float(np.mean(bootstrap_means)),
            "ci_lower_95": float(np.percentile(bootstrap_means, 2.5)),
            "ci_upper_95": float(np.percentile(bootstrap_means, 97.5)),
            "ci_lower_99": float(np.percentile(bootstrap_means, 0.5)),
            "ci_upper_99": float(np.percentile(bootstrap_means, 99.5)),
            "probability_positive": float(np.mean(bootstrap_means > 0))
        }

    def _calculate_ic(self, feature: pd.Series, returns: pd.Series) -> tuple:
        """Calculate Information Coefficient."""
        daily_ic = feature.rolling(20).corr(returns)
        ic_mean = daily_ic.mean()
        ic_std = daily_ic.std()
        return (
            float(ic_mean) if not np.isnan(ic_mean) else 0.0,
            float(ic_std) if not np.isnan(ic_std) else 1.0
        )

    def _quantile_analysis(self, feature: pd.Series, returns: pd.Series, n_quantiles: int = 5) -> Dict:
        """Alphalens-style quantile analysis."""
        try:
            quantiles = pd.qcut(feature, n_quantiles, labels=False, duplicates='drop')
        except ValueError:
            return {"error": "Not enough unique values for quantile analysis"}

        result = {}
        for q in range(n_quantiles):
            q_returns = returns[quantiles == q].dropna()
            if len(q_returns) > 0:
                mean_ret = float(q_returns.mean())
                std_ret = float(q_returns.std())
                result[f"Q{q+1}"] = {
                    "mean_return": mean_ret,
                    "sharpe": float(mean_ret / std_ret * np.sqrt(252)) if std_ret > 0 else 0,
                    "count": len(q_returns)
                }

        # Long-short spread
        if f"Q{n_quantiles}" in result and "Q1" in result:
            result["long_short_spread"] = result[f"Q{n_quantiles}"]["mean_return"] - result["Q1"]["mean_return"]

        return result

    def _create_feature_matrix(self, feature: pd.Series, prices: pd.DataFrame) -> pd.DataFrame:
        """Create feature matrix with lagged values."""
        X = pd.DataFrame({
            "feature": feature,
            "feature_lag1": feature.shift(1),
            "feature_lag2": feature.shift(2),
            "returns_1d": prices['close'].pct_change(1),
            "returns_5d": prices['close'].pct_change(5),
            "volatility": prices['close'].pct_change(1).rolling(20).std(),
        })
        return X

    def _generate_recommendation(self, stats_results: Dict, ml_results: Dict) -> str:
        """Generate recommendation based on analysis."""
        if "error" in stats_results:
            return "INSUFFICIENT DATA - Unable to perform statistical analysis"

        score = 0

        if stats_results.get("is_significant", False):
            score += 2
        if stats_results.get("ic_ir", 0) > 0.5:
            score += 2
        if ml_results.get("has_predictive_power", False):
            score += 2

        if score >= 5:
            return "STRONG EDGE - Strategy shows statistically significant edge with high predictive power"
        elif score >= 3:
            return "MODERATE EDGE - Strategy shows promise but needs further validation"
        elif score >= 1:
            return "WEAK EDGE - Limited evidence of edge. Consider refinement"
        else:
            return "NO EDGE DETECTED - Strategy does not show statistical edge"
