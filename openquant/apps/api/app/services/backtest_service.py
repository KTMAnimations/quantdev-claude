"""
Backtest Service - Strategy backtesting engine
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
import yfinance as yf


class BacktestService:
    """Strategy backtesting engine"""

    async def run_backtest(
        self,
        strategy_code: str,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 10000
    ) -> Dict:
        """Run a backtest on a strategy"""
        # Fetch historical data
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date)
        data.columns = data.columns.str.lower()

        # Simple simulation (in production, would parse Pine Script)
        trades = self._simulate_trades(data, initial_capital)
        equity_curve = self._calculate_equity_curve(trades, initial_capital)

        # Calculate metrics
        metrics = self._calculate_metrics(trades, equity_curve, initial_capital)

        return {
            "total_return": metrics["total_return"],
            "sharpe_ratio": metrics["sharpe_ratio"],
            "max_drawdown": metrics["max_drawdown"],
            "win_rate": metrics["win_rate"],
            "profit_factor": metrics["profit_factor"],
            "total_trades": len(trades),
            "trades": trades,
            "equity_curve": equity_curve
        }

    def _simulate_trades(self, data: pd.DataFrame, initial_capital: float) -> List[Dict]:
        """Simulate trades (simplified)"""
        trades = []
        position = None

        # Simple moving average crossover
        data['sma_fast'] = data['close'].rolling(9).mean()
        data['sma_slow'] = data['close'].rolling(21).mean()

        for i in range(21, len(data) - 1):
            if position is None:
                if data['sma_fast'].iloc[i] > data['sma_slow'].iloc[i] and \
                   data['sma_fast'].iloc[i-1] <= data['sma_slow'].iloc[i-1]:
                    position = {
                        "entry_time": data.index[i],
                        "entry_price": data['close'].iloc[i],
                        "direction": "long"
                    }
            else:
                if data['sma_fast'].iloc[i] < data['sma_slow'].iloc[i]:
                    exit_price = data['close'].iloc[i]
                    pnl = exit_price - position["entry_price"]
                    return_pct = pnl / position["entry_price"]

                    trades.append({
                        "entry_time": position["entry_time"].isoformat(),
                        "exit_time": data.index[i].isoformat(),
                        "pnl": float(pnl * (initial_capital / position["entry_price"])),
                        "return_pct": float(return_pct)
                    })
                    position = None

        return trades

    def _calculate_equity_curve(self, trades: List[Dict], initial_capital: float) -> List[Dict]:
        """Calculate equity curve from trades"""
        equity = initial_capital
        curve = [{"date": "Start", "equity": initial_capital}]

        for trade in trades:
            equity += trade["pnl"]
            curve.append({
                "date": trade["exit_time"],
                "equity": equity
            })

        return curve

    def _calculate_metrics(
        self,
        trades: List[Dict],
        equity_curve: List[Dict],
        initial_capital: float
    ) -> Dict:
        """Calculate performance metrics"""
        if not trades:
            return {
                "total_return": 0,
                "sharpe_ratio": 0,
                "max_drawdown": 0,
                "win_rate": 0,
                "profit_factor": 0
            }

        returns = [t["return_pct"] for t in trades]
        pnls = [t["pnl"] for t in trades]

        # Total return
        final_equity = equity_curve[-1]["equity"]
        total_return = (final_equity - initial_capital) / initial_capital

        # Sharpe ratio (annualized)
        if np.std(returns) > 0:
            sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe_ratio = 0

        # Max drawdown
        equities = [e["equity"] for e in equity_curve]
        running_max = np.maximum.accumulate(equities)
        drawdowns = (running_max - equities) / running_max
        max_drawdown = np.max(drawdowns)

        # Win rate
        wins = len([p for p in pnls if p > 0])
        win_rate = wins / len(pnls) if pnls else 0

        # Profit factor
        gross_profit = sum([p for p in pnls if p > 0])
        gross_loss = abs(sum([p for p in pnls if p < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        return {
            "total_return": float(total_return),
            "sharpe_ratio": float(sharpe_ratio),
            "max_drawdown": float(max_drawdown),
            "win_rate": float(win_rate),
            "profit_factor": float(profit_factor)
        }
