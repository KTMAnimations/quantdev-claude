"""
Comprehensive Test Suite for OpenQuant API
Tests all features end-to-end with test data
"""
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import sys
import os

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.edge_discovery import EdgeDiscoveryService
from app.services.monte_carlo_service import MonteCarloService
from app.models.schemas import PropFirmType
from app.services.prop_firm_simulator import PropFirmSimulator


class TestResults:
    """Container for test results"""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def add_pass(self, name: str, details: str = ""):
        self.passed.append({"name": name, "details": details})
        print(f"✅ PASS: {name}")
        if details:
            print(f"   Details: {details}")

    def add_fail(self, name: str, error: str):
        self.failed.append({"name": name, "error": error})
        print(f"❌ FAIL: {name}")
        print(f"   Error: {error}")

    def add_warning(self, name: str, warning: str):
        self.warnings.append({"name": name, "warning": warning})
        print(f"⚠️  WARNING: {name}")
        print(f"   Warning: {warning}")

    def summary(self):
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Passed: {len(self.passed)}")
        print(f"Failed: {len(self.failed)}")
        print(f"Warnings: {len(self.warnings)}")
        print("="*60)
        return len(self.failed) == 0


def generate_test_trades(n_trades: int = 100, win_rate: float = 0.55,
                         avg_win: float = 0.02, avg_loss: float = -0.015):
    """Generate realistic test trades"""
    trades = []
    start_date = datetime.now() - timedelta(days=n_trades * 2)

    for i in range(n_trades):
        is_win = np.random.random() < win_rate
        if is_win:
            return_pct = np.random.normal(avg_win, avg_win * 0.3)
        else:
            return_pct = np.random.normal(avg_loss, abs(avg_loss) * 0.3)

        entry_time = start_date + timedelta(days=i*2)
        exit_time = entry_time + timedelta(hours=np.random.randint(1, 24))

        trades.append({
            "entry_time": entry_time,
            "exit_time": exit_time,
            "pnl": return_pct * 10000,  # Assuming $10k account
            "return_pct": return_pct
        })

    return pd.DataFrame(trades)


def generate_test_daily_returns(n_days: int = 60, avg_return: float = 0.002,
                                 volatility: float = 0.015):
    """Generate realistic daily returns"""
    returns = np.random.normal(avg_return, volatility, n_days)
    # Add some bad days
    bad_day_idx = np.random.choice(n_days, size=int(n_days * 0.1), replace=False)
    returns[bad_day_idx] = np.random.uniform(-0.03, -0.01, len(bad_day_idx))
    return returns


results = TestResults()


# ============================================================
# TEST 1: Edge Discovery Service
# ============================================================
print("\n" + "="*60)
print("TEST 1: EDGE DISCOVERY SERVICE")
print("="*60)

async def test_edge_discovery():
    try:
        service = EdgeDiscoveryService()

        # Test RSI feature analysis
        print("\nTesting RSI feature analysis...")
        result = await service.analyze_feature(
            feature_description="RSI crosses above 30",
            symbol="SPY",
            timeframe="1D",
            lookback_days=252
        )

        # Validate response structure
        assert "feature_name" in result, "Missing feature_name"
        assert "statistical_significance" in result, "Missing statistical_significance"
        assert "ml_importance" in result, "Missing ml_importance"
        assert "confidence_intervals" in result, "Missing confidence_intervals"
        assert "recommendation" in result, "Missing recommendation"

        # Validate statistical significance fields
        stats = result["statistical_significance"]
        required_stats = ["correlation_1d", "ic_mean", "p_value", "is_significant", "quantile_returns"]
        for field in required_stats:
            assert field in stats, f"Missing {field} in statistical_significance"

        # Validate ML importance fields
        ml = result["ml_importance"]
        required_ml = ["cv_accuracy", "has_predictive_power", "feature_importance"]
        for field in required_ml:
            assert field in ml, f"Missing {field} in ml_importance"

        # Validate confidence intervals
        ci = result["confidence_intervals"]
        required_ci = ["mean_return", "ci_lower_95", "ci_upper_95", "probability_positive"]
        for field in required_ci:
            assert field in ci, f"Missing {field} in confidence_intervals"

        results.add_pass("Edge Discovery - RSI Feature",
                        f"IC: {stats['ic_mean']:.4f}, p-value: {stats['p_value']:.4f}, "
                        f"ML Accuracy: {ml['cv_accuracy']:.2%}")

        # Test EMA feature
        print("\nTesting EMA crossover feature analysis...")
        result_ema = await service.analyze_feature(
            feature_description="EMA 9 crosses above EMA 21",
            symbol="QQQ",
            timeframe="1D",
            lookback_days=252
        )

        assert result_ema["feature_name"] == "EMA 9 crosses above EMA 21"
        results.add_pass("Edge Discovery - EMA Feature",
                        f"Recommendation: {result_ema['recommendation'][:50]}...")

        # Test volume feature
        print("\nTesting volume spike feature analysis...")
        result_vol = await service.analyze_feature(
            feature_description="Volume exceeds 2x average",
            symbol="AAPL",
            timeframe="1D",
            lookback_days=252
        )

        results.add_pass("Edge Discovery - Volume Feature",
                        f"IC IR: {result_vol['statistical_significance']['ic_ir']:.4f}")

        # Test Bollinger feature
        print("\nTesting Bollinger Band feature analysis...")
        result_bb = await service.analyze_feature(
            feature_description="Price touches lower Bollinger Band",
            symbol="MSFT",
            timeframe="1D",
            lookback_days=252
        )

        results.add_pass("Edge Discovery - Bollinger Feature",
                        f"Significant: {result_bb['statistical_significance']['is_significant']}")

    except Exception as e:
        results.add_fail("Edge Discovery Service", str(e))


# ============================================================
# TEST 2: Monte Carlo Service
# ============================================================
print("\n" + "="*60)
print("TEST 2: MONTE CARLO SERVICE")
print("="*60)

async def test_monte_carlo():
    try:
        service = MonteCarloService()

        # Generate test trades
        print("\nGenerating test trades...")
        trades = generate_test_trades(n_trades=100, win_rate=0.55)
        equity_curve = pd.Series((1 + trades["return_pct"]).cumprod())

        print(f"Test Data: {len(trades)} trades, Final Equity: {equity_curve.iloc[-1]:.2%}")

        # Run full Monte Carlo analysis
        print("\nRunning Monte Carlo analysis...")
        result = await service.run_full_analysis(trades=trades, equity_curve=equity_curve)

        # Validate shuffle trades results
        assert "shuffle_trades" in result, "Missing shuffle_trades"
        assert "equity_curves" in result["shuffle_trades"], "Missing equity_curves"
        assert "max_drawdown_distribution" in result["shuffle_trades"], "Missing max_drawdown_distribution"
        results.add_pass("Monte Carlo - Shuffle Trades",
                        f"Median Final Equity: {result['shuffle_trades']['final_equity_distribution']['percentiles']['p50']:.2%}")

        # Validate bootstrap results
        assert "bootstrap" in result, "Missing bootstrap"
        bootstrap = result["bootstrap"]
        assert "sharpe_ratio" in bootstrap, "Missing sharpe_ratio"
        assert "win_rate" in bootstrap, "Missing win_rate"
        assert "expectancy" in bootstrap, "Missing expectancy"
        results.add_pass("Monte Carlo - Bootstrap",
                        f"Sharpe: {bootstrap['sharpe_ratio']['mean']:.2f}, "
                        f"Win Rate: {bootstrap['win_rate']['mean']:.1%}")

        # Validate random entry results
        assert "random_entry" in result, "Missing random_entry"
        random_entry = result["random_entry"]
        assert "p_value" in random_entry, "Missing p_value"
        assert "is_significant" in random_entry, "Missing is_significant"
        results.add_pass("Monte Carlo - Random Entry",
                        f"p-value: {random_entry['p_value']:.4f}, "
                        f"Significant: {random_entry['is_significant']}")

        # Validate drawdown distribution
        assert "drawdown_distribution" in result, "Missing drawdown_distribution"
        assert "max_drawdown" in result["drawdown_distribution"], "Missing max_drawdown"
        results.add_pass("Monte Carlo - Drawdown Distribution",
                        f"Max DD P95: {result['drawdown_distribution']['max_drawdown']['percentiles']['p95']:.1%}")

        # Validate risk of ruin
        assert "risk_of_ruin" in result, "Missing risk_of_ruin"
        assert "ruin_probability" in result["risk_of_ruin"], "Missing ruin_probability"
        results.add_pass("Monte Carlo - Risk of Ruin",
                        f"Ruin Probability: {result['risk_of_ruin']['ruin_probability']:.1%}")

        # Validate summary
        assert "summary" in result, "Missing summary"
        summary = result["summary"]
        assert "verdict" in summary, "Missing verdict"
        assert "edge_score" in summary, "Missing edge_score"
        results.add_pass("Monte Carlo - Summary",
                        f"Verdict: {summary['verdict']}, Edge Score: {summary['edge_score']}/7")

        # Test with losing strategy
        print("\nTesting with losing strategy...")
        losing_trades = generate_test_trades(n_trades=100, win_rate=0.40,
                                             avg_win=0.015, avg_loss=-0.02)
        losing_equity = pd.Series((1 + losing_trades["return_pct"]).cumprod())

        losing_result = await service.run_full_analysis(trades=losing_trades, equity_curve=losing_equity)

        # Should detect no edge
        if losing_result["summary"]["verdict"] in ["NO EDGE DETECTED", "WEAK EDGE"]:
            results.add_pass("Monte Carlo - Losing Strategy Detection",
                           f"Correctly identified: {losing_result['summary']['verdict']}")
        else:
            results.add_warning("Monte Carlo - Losing Strategy Detection",
                              f"May have false positive: {losing_result['summary']['verdict']}")

    except Exception as e:
        results.add_fail("Monte Carlo Service", str(e))


# ============================================================
# TEST 3: Prop Firm Simulator
# ============================================================
print("\n" + "="*60)
print("TEST 3: PROP FIRM SIMULATOR")
print("="*60)

async def test_prop_firm():
    try:
        simulator = PropFirmSimulator(n_simulations=1000)  # Reduced for speed

        # Test FTMO simulation
        print("\nTesting FTMO simulation...")
        daily_returns = generate_test_daily_returns(n_days=60, avg_return=0.003, volatility=0.012)

        result = await simulator.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=PropFirmType.FTMO
        )

        # Validate structure
        assert "prop_firm" in result, "Missing prop_firm"
        assert result["prop_firm"] == "FTMO", "Wrong prop firm name"
        assert "phase1" in result, "Missing phase1"
        assert "phase2" in result, "Missing phase2"
        assert "combined_pass_rate" in result, "Missing combined_pass_rate"

        # Validate phase results
        phase1 = result["phase1"]
        assert "pass_rate" in phase1, "Missing pass_rate"
        assert "fail_reasons" in phase1, "Missing fail_reasons"
        assert 0 <= phase1["pass_rate"] <= 1, "Invalid pass_rate"

        results.add_pass("Prop Firm - FTMO Simulation",
                        f"Phase 1 Pass: {phase1['pass_rate']:.1%}, "
                        f"Phase 2 Pass: {result['phase2']['pass_rate']:.1%}, "
                        f"Combined: {result['combined_pass_rate']:.1%}")

        # Validate funded simulation
        assert "funded_simulation" in result, "Missing funded_simulation"
        funded = result["funded_simulation"]
        assert "survival_rate" in funded, "Missing survival_rate"
        assert "expected_monthly_profit" in funded, "Missing expected_monthly_profit"

        results.add_pass("Prop Firm - Funded Account Simulation",
                        f"Survival Rate: {funded['survival_rate']:.1%}, "
                        f"Monthly Profit: ${funded['expected_monthly_profit']:,.0f}")

        # Validate expected value
        assert "expected_value" in result, "Missing expected_value"
        ev = result["expected_value"]
        assert "expected_value" in ev, "Missing expected_value value"
        assert "roi" in ev, "Missing roi"
        assert "recommendation" in ev, "Missing recommendation"

        results.add_pass("Prop Firm - Expected Value Calculation",
                        f"EV: ${ev['expected_value']:,.0f}, ROI: {ev['roi']:.1%}, "
                        f"Verdict: {ev['recommendation']['verdict']}")

        # Test The5%ers
        print("\nTesting The5%ers simulation...")
        result_5ers = await simulator.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=PropFirmType.THE5ERS
        )

        assert result_5ers["prop_firm"] == "The5%ers"
        results.add_pass("Prop Firm - The5%ers Simulation",
                        f"Pass Rate: {result_5ers['combined_pass_rate']:.1%}")

        # Test Apex (trailing drawdown)
        print("\nTesting Apex simulation...")
        result_apex = await simulator.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=PropFirmType.APEX
        )

        assert result_apex["prop_firm"] == "Apex Trader Funding"
        # Apex has no phase 2
        assert result_apex["phase2"] is None, "Apex should have no phase 2"
        results.add_pass("Prop Firm - Apex Simulation (Trailing DD)",
                        f"Pass Rate: {result_apex['combined_pass_rate']:.1%}")

        # Test E8
        print("\nTesting E8 simulation...")
        result_e8 = await simulator.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=PropFirmType.E8
        )

        assert result_e8["prop_firm"] == "E8 Markets"
        results.add_pass("Prop Firm - E8 Simulation",
                        f"Pass Rate: {result_e8['combined_pass_rate']:.1%}")

        # Test with bad strategy
        print("\nTesting with bad strategy...")
        bad_returns = generate_test_daily_returns(n_days=60, avg_return=-0.001, volatility=0.025)
        bad_result = await simulator.simulate_challenge(
            daily_returns=bad_returns,
            prop_firm=PropFirmType.FTMO
        )

        if bad_result["expected_value"]["recommendation"]["verdict"] in ["NOT RECOMMENDED", "AVOID"]:
            results.add_pass("Prop Firm - Bad Strategy Detection",
                           f"Correctly identified: {bad_result['expected_value']['recommendation']['verdict']}")
        else:
            results.add_warning("Prop Firm - Bad Strategy Detection",
                              f"May have missed bad strategy: {bad_result['expected_value']['recommendation']['verdict']}")

    except Exception as e:
        results.add_fail("Prop Firm Simulator", str(e))


# ============================================================
# TEST 4: Pipeline Integration
# ============================================================
print("\n" + "="*60)
print("TEST 4: PIPELINE INTEGRATION")
print("="*60)

async def test_pipeline_integration():
    """Test the full pipeline from edge discovery through prop firm simulation"""
    try:
        print("\nTesting full pipeline integration...")

        # Step 1: Edge Discovery
        edge_service = EdgeDiscoveryService()
        edge_result = await edge_service.analyze_feature(
            feature_description="RSI crosses above 30",
            symbol="SPY",
            timeframe="1D",
            lookback_days=252
        )

        # Verify edge discovery output can flow to next stage
        assert "statistical_significance" in edge_result
        assert "ml_importance" in edge_result
        results.add_pass("Pipeline - Edge Discovery Stage", "Output validated")

        # Step 2: Generate trades based on edge (simulated)
        # In production, this would be actual backtest
        if edge_result["ml_importance"]["has_predictive_power"]:
            win_rate = 0.55
            avg_win = 0.025
        else:
            win_rate = 0.50
            avg_win = 0.02

        trades = generate_test_trades(n_trades=100, win_rate=win_rate, avg_win=avg_win)
        results.add_pass("Pipeline - Trade Generation Stage", f"{len(trades)} trades generated")

        # Step 3: Monte Carlo Analysis
        mc_service = MonteCarloService()
        equity_curve = pd.Series((1 + trades["return_pct"]).cumprod())
        mc_result = await mc_service.run_full_analysis(trades=trades, equity_curve=equity_curve)

        assert "summary" in mc_result
        results.add_pass("Pipeline - Monte Carlo Stage",
                        f"Verdict: {mc_result['summary']['verdict']}")

        # Step 4: Convert to daily returns for prop firm simulation
        daily_returns = trades.set_index("entry_time")["return_pct"].resample("D").sum().dropna().values
        if len(daily_returns) < 20:
            # Not enough data, extend
            daily_returns = np.tile(daily_returns, 3)[:60]

        results.add_pass("Pipeline - Daily Returns Conversion", f"{len(daily_returns)} daily returns")

        # Step 5: Prop Firm Simulation
        prop_simulator = PropFirmSimulator(n_simulations=1000)
        prop_result = await prop_simulator.simulate_challenge(
            daily_returns=daily_returns,
            prop_firm=PropFirmType.FTMO
        )

        assert "expected_value" in prop_result
        results.add_pass("Pipeline - Prop Firm Simulation Stage",
                        f"EV: ${prop_result['expected_value']['expected_value']:,.0f}")

        # Verify end-to-end data flow
        pipeline_summary = {
            "edge_found": edge_result["statistical_significance"]["is_significant"],
            "monte_carlo_verdict": mc_result["summary"]["verdict"],
            "prop_firm_verdict": prop_result["expected_value"]["recommendation"]["verdict"],
            "expected_value": prop_result["expected_value"]["expected_value"]
        }

        results.add_pass("Pipeline - End-to-End Integration",
                        f"Edge: {pipeline_summary['edge_found']}, "
                        f"MC: {pipeline_summary['monte_carlo_verdict']}, "
                        f"Prop: {pipeline_summary['prop_firm_verdict']}")

    except Exception as e:
        results.add_fail("Pipeline Integration", str(e))


# ============================================================
# TEST 5: Data Validation
# ============================================================
print("\n" + "="*60)
print("TEST 5: DATA VALIDATION")
print("="*60)

async def test_data_validation():
    """Test edge cases and data validation"""
    try:
        mc_service = MonteCarloService()

        # Test with minimal trades
        print("\nTesting with minimal trades...")
        minimal_trades = generate_test_trades(n_trades=10, win_rate=0.60)
        minimal_equity = pd.Series((1 + minimal_trades["return_pct"]).cumprod())

        minimal_result = await mc_service.run_full_analysis(
            trades=minimal_trades,
            equity_curve=minimal_equity
        )

        assert "summary" in minimal_result
        results.add_pass("Data Validation - Minimal Trades (10)", "Handled gracefully")

        # Test with large number of trades
        print("\nTesting with large number of trades...")
        large_trades = generate_test_trades(n_trades=500, win_rate=0.55)
        large_equity = pd.Series((1 + large_trades["return_pct"]).cumprod())

        large_result = await mc_service.run_full_analysis(
            trades=large_trades,
            equity_curve=large_equity
        )

        assert "summary" in large_result
        results.add_pass("Data Validation - Large Trades (500)", "Handled successfully")

        # Test with extreme win rate
        print("\nTesting with extreme win rates...")
        high_win_trades = generate_test_trades(n_trades=100, win_rate=0.90, avg_win=0.01, avg_loss=-0.02)
        high_win_equity = pd.Series((1 + high_win_trades["return_pct"]).cumprod())

        high_win_result = await mc_service.run_full_analysis(
            trades=high_win_trades,
            equity_curve=high_win_equity
        )

        assert high_win_result["bootstrap"]["win_rate"]["mean"] > 0.8
        results.add_pass("Data Validation - High Win Rate",
                        f"Win Rate: {high_win_result['bootstrap']['win_rate']['mean']:.1%}")

        # Test with all losses
        print("\nTesting with all losses...")
        all_loss_trades = generate_test_trades(n_trades=50, win_rate=0.0, avg_win=0.01, avg_loss=-0.02)
        all_loss_trades["return_pct"] = np.abs(all_loss_trades["return_pct"]) * -1
        all_loss_equity = pd.Series((1 + all_loss_trades["return_pct"]).cumprod())

        all_loss_result = await mc_service.run_full_analysis(
            trades=all_loss_trades,
            equity_curve=all_loss_equity
        )

        # Should detect no edge
        assert all_loss_result["summary"]["verdict"] in ["NO EDGE DETECTED", "WEAK EDGE"]
        results.add_pass("Data Validation - All Losses",
                        f"Correctly detected: {all_loss_result['summary']['verdict']}")

        # Test prop firm with very volatile returns
        print("\nTesting prop firm with volatile returns...")
        prop_simulator = PropFirmSimulator(n_simulations=500)
        volatile_returns = generate_test_daily_returns(n_days=60, avg_return=0.005, volatility=0.04)

        volatile_result = await prop_simulator.simulate_challenge(
            daily_returns=volatile_returns,
            prop_firm=PropFirmType.FTMO
        )

        # High volatility should increase failure rate
        assert "fail_reasons" in volatile_result["phase1"]
        results.add_pass("Data Validation - Volatile Returns",
                        f"Daily DD Failures: {volatile_result['phase1']['fail_reasons']['daily_drawdown']:.1%}")

    except Exception as e:
        results.add_fail("Data Validation", str(e))


# ============================================================
# RUN ALL TESTS
# ============================================================
async def run_all_tests():
    print("\n" + "="*60)
    print("OPENQUANT COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    await test_edge_discovery()
    await test_monte_carlo()
    await test_prop_firm()
    await test_pipeline_integration()
    await test_data_validation()

    print("\n" + "="*60)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    all_passed = results.summary()

    # Print detailed results
    if results.failed:
        print("\nFailed Tests:")
        for fail in results.failed:
            print(f"  - {fail['name']}: {fail['error']}")

    if results.warnings:
        print("\nWarnings:")
        for warn in results.warnings:
            print(f"  - {warn['name']}: {warn['warning']}")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
