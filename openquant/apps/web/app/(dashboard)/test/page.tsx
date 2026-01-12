"use client";

import { useRef, useState, type ChangeEvent } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Upload, FlaskConical, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";
import { EquityCurve } from "@/components/charts/EquityCurve";
import { DistributionChart } from "@/components/charts/DistributionChart";
import { toast } from "sonner";
import { useStrategyStore, type Trade } from "@/lib/strategyStore";
import {
  buildEquityCurve,
  buildReturnHistogram,
  generateSampleTrades,
  parseTradesCsv,
} from "@/lib/trades";

interface MonteCarloResult {
  summary: {
    verdict: string;
    verdict_color: string;
    description: string;
    edge_score: number;
    key_metrics: {
      probability_positive_expectancy: number;
      timing_p_value: number;
      risk_of_ruin: number;
      sharpe_95_ci: [number, number];
    };
  };
  bootstrap: {
    sharpe_ratio: { mean: number; std: number };
    win_rate: { mean: number; std: number };
    expectancy: { mean: number; probability_positive: number };
  };
}

export default function TestPage() {
  const storedTrades = useStrategyStore((s) => s.trades);
  const setStoredTrades = useStrategyStore((s) => s.setTrades);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<MonteCarloResult | null>(null);
  const [trades, setTrades] = useState<Trade[]>(
    storedTrades.length > 0 ? storedTrades : generateSampleTrades()
  );
  const [nSimulations, setNSimulations] = useState(2000);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const equityData = buildEquityCurve(trades, 10_000);
  const distributionData = buildReturnHistogram(trades, 20);

  const handleChooseFile = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const parsed = parseTradesCsv(text);
      if (parsed.length === 0) {
        throw new Error(
          "No trades found. Expected CSV columns: entry_time, exit_time, pnl, return_pct"
        );
      }

      setTrades(parsed);
      setStoredTrades(parsed);
      setFileName(file.name);
      setResult(null);
      toast.success(`Loaded ${parsed.length} trades`);
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Failed to parse CSV");
    } finally {
      e.target.value = "";
    }
  };

  const handleAnalyze = async () => {
    if (trades.length === 0) {
      toast.error("Load trades first");
      return;
    }

    setIsAnalyzing(true);
    try {
      const resp = await fetch("/api/monte-carlo/analyze", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ trades, n_simulations: nSimulations }),
      });

      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data?.error || data?.detail || "Monte Carlo analysis failed");
      }

      setResult(data as MonteCarloResult);
      toast.success("Monte Carlo analysis complete");
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Monte Carlo analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getVerdictColor = (color: string) => {
    switch (color) {
      case "green":
        return "text-success bg-success/10 border-success/30";
      case "yellow":
        return "text-warning bg-warning/10 border-warning/30";
      case "orange":
        return "text-orange-500 bg-orange-500/10 border-orange-500/30";
      case "red":
        return "text-error bg-error/10 border-error/30";
      default:
        return "text-text-primary bg-background-tertiary border-border-primary";
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Monte Carlo Testing"
        subtitle="Validate your strategy with institutional-grade simulations"
      />
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="space-y-6">
          {/* Upload Section */}
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5 text-accent-primary" />
                Upload Backtest Results
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-border-secondary rounded-lg p-8 text-center">
                <Upload className="h-12 w-12 mx-auto mb-4 text-text-muted" />
                <p className="text-text-secondary mb-2">
                  Drop your backtest CSV or paste trade data
                </p>
                <p className="text-text-muted text-sm">
                  Supported formats: CSV with columns (entry_time, exit_time, pnl, return_pct)
                </p>
                <div className="mt-4 flex items-center justify-center gap-3">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv,text/csv"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                  <Button variant="outline" onClick={handleChooseFile}>
                    Choose File
                  </Button>
                  <Button
                    variant="ghost"
                    onClick={() => {
                      const sample = generateSampleTrades();
                      setTrades(sample);
                      setStoredTrades(sample);
                      setFileName(null);
                      setResult(null);
                      toast.success("Loaded sample trades");
                    }}
                  >
                    Use Sample Data
                  </Button>
                </div>
                <div className="mt-3 text-sm text-text-muted">
                  {fileName ? (
                    <span>
                      Loaded <span className="text-text-primary">{fileName}</span> (
                      {trades.length} trades)
                    </span>
                  ) : (
                    <span>Using sample trades ({trades.length} trades)</span>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <span className="text-sm text-text-muted">Simulations</span>
                  <Input
                    type="number"
                    min={100}
                    max={50000}
                    value={nSimulations}
                    onChange={(e) => setNSimulations(Number(e.target.value) || 0)}
                    className="w-32 bg-background-tertiary border-border-primary"
                  />
                </div>
                <div className="flex justify-end">
                  <Button
                    onClick={handleAnalyze}
                    disabled={isAnalyzing || trades.length === 0 || nSimulations <= 0}
                    className="bg-accent-gradient"
                  >
                    {isAnalyzing ? (
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    ) : (
                      <FlaskConical className="h-4 w-4 mr-2" />
                    )}
                    Run Monte Carlo Analysis
                  </Button>
                </div>
              </div>

              <div className="flex justify-end">
                <div className="text-sm text-text-muted">
                  Tip: run fewer simulations for faster iteration, then increase for final
                  validation.
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <>
              {/* Verdict Card */}
              <Card className={`border ${getVerdictColor(result.summary.verdict_color)}`}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-2xl font-bold">{result.summary.verdict}</h3>
                      <p className="text-text-secondary mt-1">
                        {result.summary.description}
                      </p>
                    </div>
                    <div className="text-5xl font-bold opacity-50">
                      {result.summary.edge_score}/7
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp className="h-4 w-4 text-accent-primary" />
                      <span className="text-sm text-text-muted">P(Positive Expectancy)</span>
                    </div>
                    <div className="text-2xl font-bold text-text-primary">
                      {(result.summary.key_metrics.probability_positive_expectancy * 100).toFixed(1)}%
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="h-4 w-4 text-success" />
                      <span className="text-sm text-text-muted">Timing P-Value</span>
                    </div>
                    <div className="text-2xl font-bold text-text-primary">
                      {result.summary.key_metrics.timing_p_value.toFixed(4)}
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <AlertTriangle className="h-4 w-4 text-warning" />
                      <span className="text-sm text-text-muted">Risk of Ruin</span>
                    </div>
                    <div className="text-2xl font-bold text-text-primary">
                      {(result.summary.key_metrics.risk_of_ruin * 100).toFixed(1)}%
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp className="h-4 w-4 text-accent-primary" />
                      <span className="text-sm text-text-muted">Sharpe 95% CI</span>
                    </div>
                    <div className="text-2xl font-bold text-text-primary">
                      [{result.summary.key_metrics.sharpe_95_ci[0].toFixed(2)}, {result.summary.key_metrics.sharpe_95_ci[1].toFixed(2)}]
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-background-card border-border-primary">
                  <CardHeader>
                    <CardTitle className="text-lg">Equity Curve with Drawdown</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <EquityCurve data={equityData} showDrawdown />
                  </CardContent>
                </Card>

                <Card className="bg-background-card border-border-primary">
                  <CardHeader>
                    <CardTitle className="text-lg">Return Distribution</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <DistributionChart data={distributionData} />
                  </CardContent>
                </Card>
              </div>

              {/* Bootstrap Statistics */}
              <Card className="bg-background-card border-border-primary">
                <CardHeader>
                  <CardTitle className="text-lg">Bootstrap Statistics (10,000 iterations)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <h4 className="text-sm text-text-muted mb-2">Sharpe Ratio</h4>
                      <div className="text-2xl font-bold text-text-primary">
                        {result.bootstrap.sharpe_ratio.mean.toFixed(2)}
                      </div>
                      <div className="text-sm text-text-muted">
                        \u00B1 {result.bootstrap.sharpe_ratio.std.toFixed(2)} std
                      </div>
                    </div>
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <h4 className="text-sm text-text-muted mb-2">Win Rate</h4>
                      <div className="text-2xl font-bold text-text-primary">
                        {(result.bootstrap.win_rate.mean * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-text-muted">
                        \u00B1 {(result.bootstrap.win_rate.std * 100).toFixed(1)}% std
                      </div>
                    </div>
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <h4 className="text-sm text-text-muted mb-2">Expectancy</h4>
                      <div className="text-2xl font-bold text-text-primary">
                        {(result.bootstrap.expectancy.mean * 100).toFixed(2)}%
                      </div>
                      <div className="text-sm text-text-muted">
                        {(result.bootstrap.expectancy.probability_positive * 100).toFixed(1)}% P(Positive)
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
