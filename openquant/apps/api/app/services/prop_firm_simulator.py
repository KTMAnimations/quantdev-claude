"""
Prop Firm Challenge Simulator - Monte Carlo simulation of prop firm pass rates
"""
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class PropFirmType(Enum):
    FTMO = "ftmo"
    THE5ERS = "the5ers"
    APEX = "apex"
    TOPSTEP = "topstep"
    MFF = "mff"
    E8 = "e8"


@dataclass
class PropFirmRules:
    name: str
    account_size: float
    challenge_cost: float
    profit_target_phase1: float
    profit_target_phase2: float
    max_daily_drawdown: float
    max_total_drawdown: float
    min_trading_days: int
    max_trading_days: Optional[int]
    profit_split: float
    trailing_drawdown: bool = False
    consistency_rule: Optional[float] = None


PROP_FIRM_CONFIGS = {
    PropFirmType.FTMO: PropFirmRules(
        name="FTMO",
        account_size=100000,
        challenge_cost=540,
        profit_target_phase1=0.10,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.10,
        min_trading_days=4,
        max_trading_days=None,
        profit_split=0.80
    ),
    PropFirmType.THE5ERS: PropFirmRules(
        name="The5%ers",
        account_size=100000,
        challenge_cost=235,
        profit_target_phase1=0.08,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.10,
        min_trading_days=3,
        max_trading_days=None,
        profit_split=0.80
    ),
    PropFirmType.APEX: PropFirmRules(
        name="Apex Trader Funding",
        account_size=100000,
        challenge_cost=167,
        profit_target_phase1=0.06,
        profit_target_phase2=0.0,
        max_daily_drawdown=0.0,
        max_total_drawdown=0.03,
        min_trading_days=7,
        max_trading_days=None,
        profit_split=0.90,
        trailing_drawdown=True
    ),
    PropFirmType.E8: PropFirmRules(
        name="E8 Markets",
        account_size=100000,
        challenge_cost=228,
        profit_target_phase1=0.08,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.08,
        min_trading_days=0,
        max_trading_days=None,
        profit_split=0.80
    )
}


class PropFirmSimulator:
    """Simulate prop firm challenge pass rates using Monte Carlo"""

    def __init__(self, n_simulations: int = 10000):
        self.n_simulations = n_simulations

    async def simulate_challenge(
        self,
        daily_returns: np.ndarray,
        prop_firm: PropFirmType,
        custom_rules: Optional[PropFirmRules] = None
    ) -> Dict:
        """Run Monte Carlo simulation of prop firm challenge"""
        rules = custom_rules or PROP_FIRM_CONFIGS[prop_firm]

        results = {
            "prop_firm": rules.name,
            "account_size": rules.account_size,
            "challenge_cost": rules.challenge_cost,
            "phase1": self._simulate_phase(
                daily_returns,
                rules.profit_target_phase1,
                rules.max_daily_drawdown,
                rules.max_total_drawdown,
                rules.min_trading_days,
                rules.trailing_drawdown,
                rules.consistency_rule
            ),
            "phase2": None,
            "funded_simulation": None
        }

        if rules.profit_target_phase2 > 0:
            results["phase2"] = self._simulate_phase(
                daily_returns,
                rules.profit_target_phase2,
                rules.max_daily_drawdown,
                rules.max_total_drawdown,
                rules.min_trading_days,
                rules.trailing_drawdown,
                rules.consistency_rule
            )

        phase1_pass = results["phase1"]["pass_rate"]
        phase2_pass = results["phase2"]["pass_rate"] if results["phase2"] else 1.0
        combined_pass_rate = phase1_pass * phase2_pass

        results["combined_pass_rate"] = combined_pass_rate

        results["funded_simulation"] = self._simulate_funded_account(
            daily_returns,
            rules
        )

        results["expected_value"] = self._calculate_expected_value(
            results,
            rules
        )

        return results

    def _simulate_phase(
        self,
        daily_returns: np.ndarray,
        profit_target: float,
        max_daily_dd: float,
        max_total_dd: float,
        min_days: int,
        trailing_dd: bool,
        consistency_rule: Optional[float]
    ) -> Dict:
        """Simulate a single challenge phase"""
        n_days = len(daily_returns)
        passed = 0
        failed_daily_dd = 0
        failed_total_dd = 0
        failed_consistency = 0
        days_to_pass = []

        for _ in range(self.n_simulations):
            shuffled_returns = np.random.permutation(daily_returns)

            equity = 1.0
            peak_equity = 1.0
            trailing_floor = 1.0 - max_total_dd
            daily_pnl_history = []
            day = 0
            phase_passed = False
            fail_reason = None

            for daily_return in shuffled_returns:
                day += 1
                daily_pnl = equity * daily_return
                daily_pnl_history.append(daily_pnl)

                if max_daily_dd > 0 and daily_return < -max_daily_dd:
                    fail_reason = "daily_dd"
                    break

                equity *= (1 + daily_return)

                if trailing_dd:
                    if equity > peak_equity:
                        peak_equity = equity
                        trailing_floor = equity - max_total_dd
                    if equity < trailing_floor:
                        fail_reason = "total_dd"
                        break
                else:
                    if equity < (1 - max_total_dd):
                        fail_reason = "total_dd"
                        break

                if consistency_rule and len(daily_pnl_history) > 0:
                    total_profit = sum(daily_pnl_history)
                    if total_profit > 0:
                        max_day_pnl = max(daily_pnl_history)
                        if max_day_pnl / total_profit > consistency_rule:
                            fail_reason = "consistency"
                            break

                if day >= min_days and equity >= (1 + profit_target):
                    phase_passed = True
                    break

            if phase_passed:
                passed += 1
                days_to_pass.append(day)
            elif fail_reason == "daily_dd":
                failed_daily_dd += 1
            elif fail_reason == "total_dd":
                failed_total_dd += 1
            elif fail_reason == "consistency":
                failed_consistency += 1

        pass_rate = passed / self.n_simulations

        return {
            "pass_rate": pass_rate,
            "fail_rate": 1 - pass_rate,
            "fail_reasons": {
                "daily_drawdown": failed_daily_dd / self.n_simulations,
                "total_drawdown": failed_total_dd / self.n_simulations,
                "consistency": failed_consistency / self.n_simulations,
                "time_expired": (self.n_simulations - passed - failed_daily_dd -
                               failed_total_dd - failed_consistency) / self.n_simulations
            },
            "avg_days_to_pass": float(np.mean(days_to_pass)) if days_to_pass else None,
            "days_to_pass_distribution": {
                "p25": float(np.percentile(days_to_pass, 25)) if days_to_pass else None,
                "p50": float(np.percentile(days_to_pass, 50)) if days_to_pass else None,
                "p75": float(np.percentile(days_to_pass, 75)) if days_to_pass else None
            }
        }

    def _simulate_funded_account(
        self,
        daily_returns: np.ndarray,
        rules: PropFirmRules,
        months: int = 12
    ) -> Dict:
        """Simulate performance once funded"""
        trading_days_per_month = 21
        total_days = months * trading_days_per_month

        monthly_profits = []
        violation_count = 0

        for _ in range(self.n_simulations):
            extended_returns = np.tile(
                daily_returns,
                (total_days // len(daily_returns)) + 1
            )[:total_days]
            np.random.shuffle(extended_returns)

            equity = 1.0
            monthly_pnl = []
            violated = False

            for month in range(months):
                if violated:
                    break

                month_start_equity = equity

                for day in range(trading_days_per_month):
                    idx = month * trading_days_per_month + day
                    if idx >= len(extended_returns):
                        break

                    daily_return = extended_returns[idx]

                    if rules.max_daily_drawdown > 0:
                        if daily_return < -rules.max_daily_drawdown:
                            violated = True
                            break

                    equity *= (1 + daily_return)

                    if equity < (1 - rules.max_total_drawdown):
                        violated = True
                        break

                if not violated:
                    month_pnl = equity - month_start_equity
                    monthly_pnl.append(month_pnl * rules.account_size * rules.profit_split)

            if violated:
                violation_count += 1
                monthly_profits.append(sum(monthly_pnl) if monthly_pnl else 0)
            else:
                monthly_profits.append(sum(monthly_pnl))

        return {
            "violation_rate": violation_count / self.n_simulations,
            "survival_rate": 1 - (violation_count / self.n_simulations),
            "expected_monthly_profit": float(np.mean([
                p / months for p in monthly_profits if p > 0
            ])) if any(p > 0 for p in monthly_profits) else 0,
            "total_profit_distribution": {
                "mean": float(np.mean(monthly_profits)),
                "p10": float(np.percentile(monthly_profits, 10)),
                "p25": float(np.percentile(monthly_profits, 25)),
                "p50": float(np.percentile(monthly_profits, 50)),
                "p75": float(np.percentile(monthly_profits, 75)),
                "p90": float(np.percentile(monthly_profits, 90))
            }
        }

    def _calculate_expected_value(
        self,
        results: Dict,
        rules: PropFirmRules
    ) -> Dict:
        """Calculate expected value of taking the challenge"""
        pass_rate = results["combined_pass_rate"]
        funded_sim = results["funded_simulation"]

        challenge_cost = rules.challenge_cost
        expected_funded_profit = funded_sim["total_profit_distribution"]["mean"]

        ev = (pass_rate * expected_funded_profit) - challenge_cost

        if expected_funded_profit > 0:
            break_even_pass_rate = challenge_cost / expected_funded_profit
        else:
            break_even_pass_rate = 1.0

        if challenge_cost > 0:
            roi = ev / challenge_cost
        else:
            roi = 0

        return {
            "expected_value": float(ev),
            "roi": float(roi),
            "break_even_pass_rate": float(break_even_pass_rate),
            "current_pass_rate": float(pass_rate),
            "edge_over_break_even": float(pass_rate - break_even_pass_rate),
            "recommendation": self._generate_recommendation(
                pass_rate, break_even_pass_rate, roi
            )
        }

    def _generate_recommendation(
        self,
        pass_rate: float,
        break_even: float,
        roi: float
    ) -> Dict:
        """Generate recommendation based on analysis"""
        if roi > 2:
            verdict = "HIGHLY RECOMMENDED"
            color = "green"
            description = "Strong positive expected value. Strategy is well-suited for this challenge."
        elif roi > 0.5:
            verdict = "RECOMMENDED"
            color = "green"
            description = "Positive expected value. Worth attempting with proper risk management."
        elif roi > 0:
            verdict = "MARGINAL"
            color = "yellow"
            description = "Slightly positive EV but tight margins. Consider optimizing strategy first."
        elif pass_rate > break_even * 0.8:
            verdict = "NOT RECOMMENDED"
            color = "orange"
            description = "Negative expected value but close to break-even. Minor improvements could help."
        else:
            verdict = "AVOID"
            color = "red"
            description = "Significantly negative expected value. Strategy needs major improvements."

        return {
            "verdict": verdict,
            "color": color,
            "description": description
        }
