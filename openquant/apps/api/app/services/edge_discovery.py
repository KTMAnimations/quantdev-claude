"""
Edge Discovery Service - Replicates QuantPad's edge discovery using Alphalens + ML
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from typing import Dict, Optional
import yfinance as yf


class EdgeDiscoveryService:
    """
    Replicates QuantPad's edge discovery using Alphalens + custom ML
    """

    def __init__(self):
        self.tscv = TimeSeriesSplit(n_splits=5)

    async def analyze_feature(
        self,
        feature_description: str,
        symbol: str,
        timeframe: str,
        lookback_days: int = 252
    ) -> Dict:
        """
        Main entry point - analyzes a trading feature/signal
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
            "statistical_significance": stats_results,
            "ml_importance": ml_results,
            "confidence_intervals": bootstrap_results,
            "recommendation": self._generate_recommendation(stats_results, ml_results)
        }

    async def _parse_feature_description(self, description: str) -> Dict:
        """Parse natural language to feature logic"""
        # Simplified parsing - in production would use LLM
        description_lower = description.lower()

        if "rsi" in description_lower:
            return {"type": "rsi", "period": 14}
        elif "ema" in description_lower or "moving average" in description_lower:
            return {"type": "ema", "fast": 9, "slow": 21}
        elif "volume" in description_lower:
            return {"type": "volume_spike", "threshold": 2.0}
        elif "bollinger" in description_lower:
            return {"type": "bollinger", "period": 20, "std": 2}
        else:
            return {"type": "momentum", "period": 10}

    async def _fetch_data(self, symbol: str, timeframe: str, lookback_days: int) -> pd.DataFrame:
        """Fetch historical data"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{lookback_days}d")
        data.columns = data.columns.str.lower()
        return data

    def _compute_feature(self, price_data: pd.DataFrame, feature_logic: Dict) -> pd.Series:
        """Compute the feature based on logic"""
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

        elif feature_type == "volume_spike":
            threshold = feature_logic.get("threshold", 2.0)
            avg_volume = price_data['volume'].rolling(20).mean()
            return price_data['volume'] / avg_volume

        elif feature_type == "bollinger":
            period = feature_logic.get("period", 20)
            std_dev = feature_logic.get("std", 2)
            ma = price_data['close'].rolling(period).mean()
            std = price_data['close'].rolling(period).std()
            return (price_data['close'] - ma) / (std * std_dev)

        else:  # momentum
            period = feature_logic.get("period", 10)
            return price_data['close'].pct_change(period)

    def _run_statistical_tests(self, feature: pd.Series, prices: pd.DataFrame) -> Dict:
        """Run comprehensive statistical tests on the feature"""
        # Forward returns
        returns_1d = prices['close'].pct_change(1).shift(-1)
        returns_5d = prices['close'].pct_change(5).shift(-5)

        # Clean data
        mask = ~(feature.isna() | returns_1d.isna())
        feature_clean = feature[mask]
        returns_1d_clean = returns_1d[mask]
        returns_5d_clean = returns_5d[mask & ~returns_5d.isna()]

        # Correlation analysis
        correlation_1d = feature_clean.corr(returns_1d_clean)
        correlation_5d = feature_clean[:len(returns_5d_clean)].corr(returns_5d_clean)

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
        """Use ML to detect non-linear patterns"""
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
        importance = dict(zip(X_clean.columns, model.feature_importances_))

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
        """Bootstrap confidence intervals for expectancy"""
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
        """Calculate Information Coefficient"""
        daily_ic = feature.rolling(20).corr(returns)
        return daily_ic.mean(), daily_ic.std()

    def _quantile_analysis(self, feature: pd.Series, returns: pd.Series, n_quantiles: int = 5) -> Dict:
        """Alphalens-style quantile analysis"""
        try:
            quantiles = pd.qcut(feature, n_quantiles, labels=False, duplicates='drop')
        except ValueError:
            return {"error": "Not enough unique values for quantile analysis"}

        result = {}
        for q in range(n_quantiles):
            q_returns = returns[quantiles == q].dropna()
            if len(q_returns) > 0:
                result[f"Q{q+1}"] = {
                    "mean_return": float(q_returns.mean()),
                    "sharpe": float(q_returns.mean() / q_returns.std() * np.sqrt(252)) if q_returns.std() > 0 else 0,
                    "count": len(q_returns)
                }

        # Long-short spread
        if f"Q{n_quantiles}" in result and "Q1" in result:
            result["long_short_spread"] = result[f"Q{n_quantiles}"]["mean_return"] - result["Q1"]["mean_return"]

        return result

    def _create_feature_matrix(self, feature: pd.Series, prices: pd.DataFrame) -> pd.DataFrame:
        """Create feature matrix with lagged values"""
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
        """Generate recommendation based on analysis"""
        score = 0

        if stats_results["is_significant"]:
            score += 2
        if stats_results["ic_ir"] > 0.5:
            score += 2
        if ml_results["has_predictive_power"]:
            score += 2

        if score >= 5:
            return "STRONG EDGE - Strategy shows statistically significant edge with high predictive power"
        elif score >= 3:
            return "MODERATE EDGE - Strategy shows promise but needs further validation"
        elif score >= 1:
            return "WEAK EDGE - Limited evidence of edge. Consider refinement"
        else:
            return "NO EDGE DETECTED - Strategy does not show statistical edge"
