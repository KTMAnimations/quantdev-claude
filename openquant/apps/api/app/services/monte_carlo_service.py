"""
Monte Carlo Simulation Service - Institutional-grade bootstrapping and randomization
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class MonteCarloConfig:
    n_simulations: int = 10000
    confidence_levels: tuple = (0.80, 0.90, 0.95, 0.99)
    methods: tuple = ("shuffle_returns", "bootstrap", "random_entry")


class MonteCarloService:
    """
    Institutional-grade Monte Carlo simulation engine
    """

    def __init__(self, config: MonteCarloConfig = None):
        self.config = config or MonteCarloConfig()

    async def run_full_analysis(
        self,
        trades: pd.DataFrame,
        equity_curve: pd.Series
    ) -> Dict:
        """
        Run comprehensive Monte Carlo analysis on backtest results
        """
        results = {}

        # 1. Shuffle trades Monte Carlo
        results["shuffle_trades"] = self._shuffle_trades_mc(trades)

        # 2. Bootstrap resampling
        results["bootstrap"] = self._bootstrap_mc(trades)

        # 3. Random entry simulation
        results["random_entry"] = self._random_entry_mc(trades, equity_curve)

        # 4. Drawdown distribution
        results["drawdown_distribution"] = self._drawdown_distribution(trades)

        # 5. Risk of ruin calculation
        results["risk_of_ruin"] = self._calculate_risk_of_ruin(trades)

        # 6. Expectancy confidence intervals
        results["expectancy_ci"] = self._expectancy_confidence_intervals(trades)

        # 7. Summary statistics
        results["summary"] = self._generate_summary(results, trades)

        return self._to_python_types(results)

    @staticmethod
    def _to_python_types(obj):
        """Recursively convert numpy scalars/arrays to JSON-serializable Python types."""
        if isinstance(obj, dict):
            return {k: MonteCarloService._to_python_types(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [MonteCarloService._to_python_types(v) for v in obj]
        if isinstance(obj, np.ndarray):
            return MonteCarloService._to_python_types(obj.tolist())
        if isinstance(obj, (np.floating, np.integer)):
            return obj.item()
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        return obj

    def _shuffle_trades_mc(self, trades: pd.DataFrame) -> Dict:
        """Monte Carlo by shuffling trade order"""
        returns = trades["return_pct"].values
        n_trades = len(returns)

        simulated_max_drawdowns = []
        simulated_final_equity = []
        equity_curves = []

        for _ in range(self.config.n_simulations):
            shuffled = np.random.permutation(returns)
            equity = np.cumprod(1 + shuffled)

            if len(equity_curves) < 100:
                equity_curves.append(equity.tolist())

            running_max = np.maximum.accumulate(equity)
            drawdown = (running_max - equity) / running_max
            simulated_max_drawdowns.append(np.max(drawdown))
            simulated_final_equity.append(equity[-1])

        return {
            "equity_curves": equity_curves,
            "max_drawdown_distribution": {
                "values": simulated_max_drawdowns[:1000],
                "percentiles": self._calculate_percentiles(simulated_max_drawdowns)
            },
            "final_equity_distribution": {
                "values": simulated_final_equity[:1000],
                "percentiles": self._calculate_percentiles(simulated_final_equity)
            }
        }

    def _bootstrap_mc(self, trades: pd.DataFrame) -> Dict:
        """Bootstrap resampling with replacement"""
        returns = trades["return_pct"].values
        n_trades = len(returns)

        bootstrap_sharpe = []
        bootstrap_profit_factor = []
        bootstrap_win_rate = []
        bootstrap_expectancy = []

        for _ in range(self.config.n_simulations):
            sample_idx = np.random.choice(n_trades, size=n_trades, replace=True)
            sample_returns = returns[sample_idx]

            if np.std(sample_returns) > 0:
                sharpe = np.mean(sample_returns) / np.std(sample_returns) * np.sqrt(252)
            else:
                sharpe = 0
            bootstrap_sharpe.append(sharpe)

            wins = sample_returns[sample_returns > 0]
            losses = sample_returns[sample_returns < 0]

            if len(losses) > 0 and np.sum(np.abs(losses)) > 0:
                pf = np.sum(wins) / np.sum(np.abs(losses))
            else:
                pf = np.inf if len(wins) > 0 else 0
            bootstrap_profit_factor.append(pf)

            win_rate = len(wins) / len(sample_returns) if len(sample_returns) > 0 else 0
            bootstrap_win_rate.append(win_rate)

            expectancy = np.mean(sample_returns)
            bootstrap_expectancy.append(expectancy)

        return {
            "sharpe_ratio": {
                "mean": float(np.mean(bootstrap_sharpe)),
                "std": float(np.std(bootstrap_sharpe)),
                "percentiles": self._calculate_percentiles(bootstrap_sharpe)
            },
            "profit_factor": {
                "mean": float(np.nanmean([x for x in bootstrap_profit_factor if x != np.inf])),
                "percentiles": self._calculate_percentiles(
                    [x for x in bootstrap_profit_factor if x != np.inf and x < 100]
                )
            },
            "win_rate": {
                "mean": float(np.mean(bootstrap_win_rate)),
                "std": float(np.std(bootstrap_win_rate)),
                "percentiles": self._calculate_percentiles(bootstrap_win_rate)
            },
            "expectancy": {
                "mean": float(np.mean(bootstrap_expectancy)),
                "std": float(np.std(bootstrap_expectancy)),
                "percentiles": self._calculate_percentiles(bootstrap_expectancy),
                "probability_positive": float(np.mean(np.array(bootstrap_expectancy) > 0))
            }
        }

    def _random_entry_mc(
        self,
        trades: pd.DataFrame,
        equity_curve: pd.Series
    ) -> Dict:
        """Compare strategy to random entry timing"""
        underlying_returns = equity_curve.pct_change().dropna().values
        n_periods = len(underlying_returns)
        n_trades = len(trades)

        avg_trade_duration = 5

        random_strategy_returns = []

        for _ in range(self.config.n_simulations):
            entry_points = np.random.choice(
                max(1, n_periods - avg_trade_duration),
                size=n_trades,
                replace=True
            )

            trade_returns = []
            for entry in entry_points:
                exit_point = min(entry + avg_trade_duration, n_periods - 1)
                period_returns = underlying_returns[entry:exit_point]
                if len(period_returns) > 0:
                    trade_return = np.prod(1 + period_returns) - 1
                    trade_returns.append(trade_return)

            if trade_returns:
                random_strategy_returns.append(np.mean(trade_returns))

        original_expectancy = trades["return_pct"].mean()
        p_value = np.mean(np.array(random_strategy_returns) >= original_expectancy)

        return {
            "original_expectancy": float(original_expectancy),
            "random_expectancy_distribution": {
                "mean": float(np.mean(random_strategy_returns)),
                "std": float(np.std(random_strategy_returns)),
                "percentiles": self._calculate_percentiles(random_strategy_returns)
            },
            "p_value": float(p_value),
            "is_significant": bool(p_value < 0.05),
            "edge_percentile": float(
                stats.percentileofscore(random_strategy_returns, original_expectancy)
            ) if random_strategy_returns else 50.0
        }

    def _drawdown_distribution(self, trades: pd.DataFrame) -> Dict:
        """Calculate drawdown distribution across simulations"""
        returns = trades["return_pct"].values

        max_drawdowns = []
        avg_drawdowns = []
        drawdown_durations = []

        for _ in range(self.config.n_simulations):
            shuffled = np.random.permutation(returns)
            equity = np.cumprod(1 + shuffled)

            running_max = np.maximum.accumulate(equity)
            drawdown = (running_max - equity) / running_max

            max_drawdowns.append(np.max(drawdown))
            avg_drawdowns.append(np.mean(drawdown))

            in_drawdown = drawdown > 0
            durations = []
            current_duration = 0
            for is_dd in in_drawdown:
                if is_dd:
                    current_duration += 1
                elif current_duration > 0:
                    durations.append(current_duration)
                    current_duration = 0
            if current_duration > 0:
                durations.append(current_duration)

            drawdown_durations.append(max(durations) if durations else 0)

        return {
            "max_drawdown": {
                "percentiles": self._calculate_percentiles(max_drawdowns),
                "histogram": np.histogram(max_drawdowns, bins=50)[0].tolist()
            },
            "avg_drawdown": {
                "mean": float(np.mean(avg_drawdowns)),
                "percentiles": self._calculate_percentiles(avg_drawdowns)
            },
            "max_drawdown_duration": {
                "mean": float(np.mean(drawdown_durations)),
                "percentiles": self._calculate_percentiles(drawdown_durations)
            }
        }

    def _calculate_risk_of_ruin(
        self,
        trades: pd.DataFrame,
        ruin_threshold: float = 0.5
    ) -> Dict:
        """Calculate probability of hitting a ruin threshold"""
        returns = trades["return_pct"].values

        ruin_count = 0
        min_equity_distribution = []

        for _ in range(self.config.n_simulations):
            shuffled = np.random.permutation(returns)
            equity = np.cumprod(1 + shuffled)

            min_equity = np.min(equity)
            min_equity_distribution.append(min_equity)

            if min_equity < (1 - ruin_threshold):
                ruin_count += 1

        return {
            "ruin_probability": float(ruin_count / self.config.n_simulations),
            "min_equity_percentiles": self._calculate_percentiles(min_equity_distribution),
            "probability_below_50pct": float(
                np.mean(np.array(min_equity_distribution) < 0.5)
            ),
            "probability_below_25pct": float(
                np.mean(np.array(min_equity_distribution) < 0.25)
            )
        }

    def _expectancy_confidence_intervals(self, trades: pd.DataFrame) -> Dict:
        """Calculate confidence intervals for expectancy"""
        returns = trades["return_pct"].values

        bootstrap_means = []
        for _ in range(self.config.n_simulations):
            sample = np.random.choice(returns, size=len(returns), replace=True)
            bootstrap_means.append(np.mean(sample))

        return {
            "mean": float(np.mean(returns)),
            "confidence_intervals": {
                "80": [
                    float(np.percentile(bootstrap_means, 10)),
                    float(np.percentile(bootstrap_means, 90))
                ],
                "90": [
                    float(np.percentile(bootstrap_means, 5)),
                    float(np.percentile(bootstrap_means, 95))
                ],
                "95": [
                    float(np.percentile(bootstrap_means, 2.5)),
                    float(np.percentile(bootstrap_means, 97.5))
                ],
                "99": [
                    float(np.percentile(bootstrap_means, 0.5)),
                    float(np.percentile(bootstrap_means, 99.5))
                ]
            },
            "probability_positive": float(np.mean(np.array(bootstrap_means) > 0))
        }

    def _calculate_percentiles(self, values: List[float]) -> Dict:
        """Calculate standard percentiles"""
        arr = np.array([x for x in values if not np.isnan(x) and not np.isinf(x)])
        if len(arr) == 0:
            return {f"p{p}": 0.0 for p in [5, 10, 25, 50, 75, 90, 95, 99]}
        return {
            "p5": float(np.percentile(arr, 5)),
            "p10": float(np.percentile(arr, 10)),
            "p25": float(np.percentile(arr, 25)),
            "p50": float(np.percentile(arr, 50)),
            "p75": float(np.percentile(arr, 75)),
            "p90": float(np.percentile(arr, 90)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99))
        }

    def _generate_summary(self, results: Dict, trades: pd.DataFrame) -> Dict:
        """Generate summary verdict"""
        bootstrap = results["bootstrap"]
        random_entry = results["random_entry"]
        risk = results["risk_of_ruin"]

        edge_score = 0

        if bootstrap["expectancy"]["probability_positive"] > 0.95:
            edge_score += 3
        elif bootstrap["expectancy"]["probability_positive"] > 0.80:
            edge_score += 2
        elif bootstrap["expectancy"]["probability_positive"] > 0.65:
            edge_score += 1

        if random_entry["is_significant"]:
            edge_score += 2

        if risk["ruin_probability"] < 0.05:
            edge_score += 2
        elif risk["ruin_probability"] < 0.10:
            edge_score += 1

        if edge_score >= 6:
            verdict = "STRONG EDGE"
            verdict_color = "green"
            description = "Strategy shows statistically significant edge with low risk of ruin."
        elif edge_score >= 4:
            verdict = "MODERATE EDGE"
            verdict_color = "yellow"
            description = "Strategy shows promise but needs further validation."
        elif edge_score >= 2:
            verdict = "WEAK EDGE"
            verdict_color = "orange"
            description = "Limited evidence of edge. Consider refinement."
        else:
            verdict = "NO EDGE DETECTED"
            verdict_color = "red"
            description = "Strategy does not show statistical edge over random."

        return {
            "verdict": verdict,
            "verdict_color": verdict_color,
            "description": description,
            "edge_score": edge_score,
            "key_metrics": {
                "expectancy_95_ci": bootstrap["expectancy"]["percentiles"],
                "probability_positive_expectancy": bootstrap["expectancy"]["probability_positive"],
                "timing_p_value": random_entry["p_value"],
                "risk_of_ruin": risk["ruin_probability"],
                "sharpe_95_ci": [
                    bootstrap["sharpe_ratio"]["percentiles"]["p5"],
                    bootstrap["sharpe_ratio"]["percentiles"]["p95"]
                ]
            }
        }
