"""
Test Pine Script Generator and Regression Analysis Services
"""
import asyncio
import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.pine_generator import PineScriptGenerator
from app.services.regression_service import RegressionService


async def test_pine_generator():
    print("\n" + "="*60)
    print("PINE SCRIPT GENERATOR TESTS")
    print("="*60)

    service = PineScriptGenerator()
    passed = 0
    failed = 0

    # Test 1: RSI Strategy Generation
    print("\nTest 1: RSI Strategy Generation...")
    result = await service.generate_pine_script(
        description="RSI overbought oversold strategy",
        script_type="strategy"
    )

    if result["is_valid"] and "//@version=5" in result["code"] and "strategy(" in result["code"]:
        print("✅ PASS: RSI strategy generated correctly")
        print(f"   Code length: {len(result['code'])} chars")
        passed += 1
    else:
        print(f"❌ FAIL: RSI strategy generation failed: {result.get('errors', [])}")
        failed += 1

    # Test 2: EMA Crossover Generation
    print("\nTest 2: EMA Crossover Generation...")
    result = await service.generate_pine_script(
        description="EMA 9 21 crossover with ATR stops",
        script_type="strategy"
    )

    if result["is_valid"] and "ema" in result["code"].lower():
        print("✅ PASS: EMA crossover strategy generated")
        passed += 1
    else:
        print(f"❌ FAIL: EMA strategy generation failed")
        failed += 1

    # Test 3: Bollinger Bands Indicator
    print("\nTest 3: Bollinger Bands Indicator...")
    result = await service.generate_pine_script(
        description="Bollinger Bands indicator",
        script_type="indicator"
    )

    if result["is_valid"] and "indicator(" in result["code"]:
        print("✅ PASS: Bollinger Bands indicator generated")
        passed += 1
    else:
        print(f"❌ FAIL: Bollinger Bands generation failed")
        failed += 1

    # Test 4: Custom Strategy Generation
    print("\nTest 4: Custom Strategy Generation...")
    result = await service.generate_pine_script(
        description="Custom momentum breakout system",
        script_type="strategy"
    )

    if result["is_valid"]:
        print("✅ PASS: Custom strategy generated")
        passed += 1
    else:
        print(f"❌ FAIL: Custom strategy failed: {result.get('errors', [])}")
        failed += 1

    # Test 5: Syntax Validation - Valid Code
    print("\nTest 5: Syntax Validation (Valid Code)...")
    valid_code = '''
//@version=5
strategy("Test", overlay=true)
plot(close, "Close", color.blue)
'''
    validation = service._validate_pine_syntax(valid_code)
    if validation["is_valid"]:
        print("✅ PASS: Valid code recognized")
        passed += 1
    else:
        print(f"❌ FAIL: Valid code rejected: {validation['errors']}")
        failed += 1

    # Test 6: Syntax Validation - Invalid Code (no version)
    print("\nTest 6: Syntax Validation (Missing Version)...")
    invalid_code = '''
strategy("Test", overlay=true)
plot(close, "Close", color.blue)
'''
    validation = service._validate_pine_syntax(invalid_code)
    if not validation["is_valid"] and any("version" in e.lower() for e in validation["errors"]):
        print("✅ PASS: Missing version detected")
        passed += 1
    else:
        print(f"❌ FAIL: Missing version not detected")
        failed += 1

    # Test 7: Syntax Validation - Mismatched Parentheses
    print("\nTest 7: Syntax Validation (Mismatched Parentheses)...")
    bad_code = '''
//@version=5
strategy("Test", overlay=true
plot(close)
'''
    validation = service._validate_pine_syntax(bad_code)
    if not validation["is_valid"]:
        print("✅ PASS: Syntax error detected")
        passed += 1
    else:
        print("❌ FAIL: Syntax error not detected")
        failed += 1

    print(f"\nPine Generator Summary: {passed}/{passed+failed} passed")
    return passed, failed


async def test_regression_service():
    print("\n" + "="*60)
    print("REGRESSION ANALYSIS TESTS")
    print("="*60)

    service = RegressionService()
    passed = 0
    failed = 0

    # Generate test trades
    n_trades = 100
    test_trades = []
    for i in range(n_trades):
        test_trades.append({
            "return_pct": np.random.normal(0.002, 0.02),
            "volatility": np.random.uniform(0.1, 0.3),
            "rsi_level": np.random.uniform(20, 80),
            "volume_ratio": np.random.uniform(0.5, 2.0),
        })

    # Test 1: Basic Regression Analysis
    print("\nTest 1: Basic Regression Analysis...")
    result = await service.analyze(trades=test_trades, features=["volatility", "rsi_level"])

    if "r_squared" in result and "factors" in result:
        print("✅ PASS: Regression analysis completed")
        print(f"   R²: {result['r_squared']:.4f}")
        print(f"   Adjusted R²: {result['adjusted_r_squared']:.4f}")
        print(f"   Factors: {len(result['factors'])}")
        passed += 1
    else:
        print(f"❌ FAIL: Missing expected fields")
        failed += 1

    # Test 2: Factor Results Structure
    print("\nTest 2: Factor Results Structure...")
    if result["factors"]:
        factor = result["factors"][0]
        if all(k in factor for k in ["name", "coefficient", "p_value", "significance"]):
            print("✅ PASS: Factor structure correct")
            print(f"   Example: {factor['name']}: coef={factor['coefficient']:.4f}, p={factor['p_value']:.4f}")
            passed += 1
        else:
            print("❌ FAIL: Factor missing required fields")
            failed += 1
    else:
        print("⚠️ WARNING: No factors returned")
        failed += 1

    # Test 3: Durbin-Watson Statistic
    print("\nTest 3: Durbin-Watson Statistic...")
    if "durbin_watson" in result and 0 <= result["durbin_watson"] <= 4:
        print("✅ PASS: Durbin-Watson in valid range")
        print(f"   DW: {result['durbin_watson']:.4f}")
        passed += 1
    else:
        print(f"❌ FAIL: Durbin-Watson invalid: {result.get('durbin_watson')}")
        failed += 1

    # Test 4: Residuals Normality
    print("\nTest 4: Residuals Normality...")
    if "residuals_normality" in result:
        print(f"✅ PASS: Normality test completed: {result['residuals_normality']}")
        passed += 1
    else:
        print("❌ FAIL: Normality test missing")
        failed += 1

    # Test 5: Empty Trades Handling
    print("\nTest 5: Empty Trades Handling...")
    empty_result = await service.analyze(trades=[], features=[])
    if empty_result["r_squared"] == 0.0:
        print("✅ PASS: Empty trades handled gracefully")
        passed += 1
    else:
        print("❌ FAIL: Empty trades not handled")
        failed += 1

    # Test 6: Large Dataset
    print("\nTest 6: Large Dataset (500 trades)...")
    large_trades = [{"return_pct": np.random.normal(0.001, 0.015)} for _ in range(500)]
    large_result = await service.analyze(trades=large_trades, features=[])
    if "r_squared" in large_result:
        print("✅ PASS: Large dataset processed")
        passed += 1
    else:
        print("❌ FAIL: Large dataset failed")
        failed += 1

    print(f"\nRegression Summary: {passed}/{passed+failed} passed")
    return passed, failed


async def main():
    print("="*60)
    print("OPENQUANT PINE SCRIPT & REGRESSION TESTS")
    print("="*60)

    pine_passed, pine_failed = await test_pine_generator()
    reg_passed, reg_failed = await test_regression_service()

    total_passed = pine_passed + reg_passed
    total_failed = pine_failed + reg_failed

    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Pine Generator: {pine_passed}/{pine_passed + pine_failed} passed")
    print(f"Regression:     {reg_passed}/{reg_passed + reg_failed} passed")
    print(f"Total:          {total_passed}/{total_passed + total_failed} passed")
    print("="*60)

    return total_failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
