"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { PineScriptEditor } from "@/components/editor/PineScriptEditor";
import { validatePineSyntax } from "@/lib/pineValidation";
import { useStrategyStore } from "@/lib/strategyStore";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2, Play } from "lucide-react";

const DEFAULT_CODE = `//@version=5
strategy("My Strategy", overlay=true)

// Inputs
length = input.int(14, "RSI Length", minval=1)
overbought = input.int(70, "Overbought Level")
oversold = input.int(30, "Oversold Level")

// Calculate RSI
rsiValue = ta.rsi(close, length)

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
`;

export default function CodePage() {
  const storedCode = useStrategyStore((s) => s.pineCode);
  const setStoredCode = useStrategyStore((s) => s.setPineCode);
  const setStoredTrades = useStrategyStore((s) => s.setTrades);

  const [code, setCode] = useState(storedCode || DEFAULT_CODE);
  const [isGenerating, setIsGenerating] = useState(false);
  const [validationErrors, setValidationErrors] = useState<string[]>(() => {
    return validatePineSyntax(storedCode || DEFAULT_CODE).errors;
  });
  const [symbol, setSymbol] = useState("SPY");
  const [timeframe, setTimeframe] = useState("1D");
  const [startDate, setStartDate] = useState("2020-01-01");
  const [endDate, setEndDate] = useState("2020-09-01");
  const [initialCapital, setInitialCapital] = useState(10_000);
  const [isBacktesting, setIsBacktesting] = useState(false);
  const [lastBacktestTrades, setLastBacktestTrades] = useState<number | null>(null);

  useEffect(() => {
    setValidationErrors(validatePineSyntax(code).errors);
    setStoredCode(code);
  }, [code, setStoredCode]);

  useEffect(() => {
    if (storedCode && storedCode !== code) setCode(storedCode);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [storedCode]);

  const handleGenerate = async (description: string) => {
    setIsGenerating(true);
    try {
      const resp = await fetch("/api/pine/generate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ description, script_type: "strategy" }),
      });

      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data?.error || data?.detail || "Failed to generate Pine Script");
      }

      if (typeof data.code !== "string") {
        throw new Error("Backend did not return code");
      }

      setCode(data.code);
      setValidationErrors(Array.isArray(data.errors) ? data.errors : []);
      toast.success("Generated Pine Script");
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleBacktest = async () => {
    setIsBacktesting(true);
    try {
      const resp = await fetch("/api/backtest/run", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          strategy_code: code,
          symbol,
          timeframe,
          start_date: `${startDate}T00:00:00`,
          end_date: `${endDate}T00:00:00`,
          initial_capital: initialCapital,
        }),
      });

      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data?.error || data?.detail || "Backtest failed");
      }

      const trades = Array.isArray(data.trades) ? data.trades : [];
      setStoredTrades(trades);
      setLastBacktestTrades(trades.length);
      toast.success(`Backtest complete (${trades.length} trades)`);
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Backtest failed");
    } finally {
      setIsBacktesting(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Pine Script Generator"
        subtitle="Describe your strategy in natural language"
      />
      <div className="flex-1 p-6 flex flex-col gap-6 overflow-hidden">
        <Card className="bg-background-card border-border-primary">
          <CardHeader>
            <CardTitle className="text-lg flex items-center justify-between">
              Backtest (Quick Run)
              {lastBacktestTrades !== null && (
                <span className="text-sm text-text-muted font-normal">
                  Last run: {lastBacktestTrades} trades saved to pipeline
                </span>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3 items-end">
              <div>
                <label className="text-sm text-text-muted">Symbol</label>
                <Input
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  className="w-32 bg-background-tertiary border-border-primary"
                />
              </div>
              <div>
                <label className="text-sm text-text-muted">Timeframe</label>
                <Input
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  className="w-32 bg-background-tertiary border-border-primary"
                />
              </div>
              <div>
                <label className="text-sm text-text-muted">Start</label>
                <Input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-44 bg-background-tertiary border-border-primary"
                />
              </div>
              <div>
                <label className="text-sm text-text-muted">End</label>
                <Input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-44 bg-background-tertiary border-border-primary"
                />
              </div>
              <div>
                <label className="text-sm text-text-muted">Initial Capital</label>
                <Input
                  type="number"
                  value={initialCapital}
                  onChange={(e) => setInitialCapital(Number(e.target.value) || 0)}
                  className="w-44 bg-background-tertiary border-border-primary"
                />
              </div>
              <div className="ml-auto">
                <Button
                  onClick={handleBacktest}
                  disabled={isBacktesting || initialCapital <= 0}
                  className="bg-accent-gradient"
                >
                  {isBacktesting ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : (
                    <Play className="h-4 w-4 mr-2" />
                  )}
                  Run Backtest
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex-1 bg-background-card rounded-lg border border-border-primary overflow-hidden">
          <PineScriptEditor
            value={code}
            onChange={setCode}
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
            validationErrors={validationErrors}
          />
        </div>
      </div>
    </div>
  );
}
