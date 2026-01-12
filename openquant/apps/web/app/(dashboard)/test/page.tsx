"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Upload, FlaskConical, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";
import { EquityCurve } from "@/components/charts/EquityCurve";
import { DistributionChart } from "@/components/charts/DistributionChart";

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
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<MonteCarloResult | null>(null);

  // Mock data for equity curve
  const equityData = Array.from({ length: 100 }, (_, i) => ({
    date: `Day ${i + 1}`,
    equity: 10000 * Math.pow(1.001 + Math.random() * 0.002, i) + (Math.random() - 0.5) * 500,
    drawdown: Math.random() * 0.1,
  }));

  // Mock data for distribution
  const distributionData = Array.from({ length: 20 }, (_, i) => ({
    bin: `${(i - 10) * 0.5}%`,
    count: Math.floor(Math.random() * 100 + 50 * Math.exp(-Math.pow((i - 10) / 5, 2))),
  }));

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    await new Promise((resolve) => setTimeout(resolve, 3000));

    setResult({
      summary: {
        verdict: "MODERATE EDGE",
        verdict_color: "yellow",
        description: "Strategy shows promise but needs further validation.",
        edge_score: 4,
        key_metrics: {
          probability_positive_expectancy: 0.87,
          timing_p_value: 0.032,
          risk_of_ruin: 0.08,
          sharpe_95_ci: [0.42, 1.85],
        },
      },
      bootstrap: {
        sharpe_ratio: { mean: 1.12, std: 0.35 },
        win_rate: { mean: 0.54, std: 0.05 },
        expectancy: { mean: 0.0023, probability_positive: 0.87 },
      },
    });

    setIsAnalyzing(false);
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
                <Button variant="outline" className="mt-4">
                  Choose File
                </Button>
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
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
