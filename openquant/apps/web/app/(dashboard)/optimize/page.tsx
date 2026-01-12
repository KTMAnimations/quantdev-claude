"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Settings2, TrendingUp, BarChart3 } from "lucide-react";
import { toast } from "sonner";
import { useStrategyStore } from "@/lib/strategyStore";
import { generateSampleTrades } from "@/lib/trades";

interface RegressionResult {
  r_squared: number;
  adjusted_r_squared: number;
  factors: { name: string; coefficient: number; p_value: number; significance: string }[];
  residuals_normality: boolean;
  durbin_watson: number;
}

export default function OptimizePage() {
  const trades = useStrategyStore((s) => s.trades);
  const setTrades = useStrategyStore((s) => s.setTrades);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<RegressionResult | null>(null);

  const handleAnalyze = async () => {
    if (trades.length === 0) {
      toast.error("Load trades first (Test → upload CSV)");
      return;
    }

    setIsAnalyzing(true);
    try {
      const resp = await fetch("/api/regression/analyze", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ trades, features: [] }),
      });

      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data?.error || data?.detail || "Regression analysis failed");
      }

      setResult(data as RegressionResult);
      toast.success("Regression analysis complete");
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Regression analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Regression Analysis"
        subtitle="Uncover the hidden factors affecting your strategy performance"
      />
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="space-y-6">
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings2 className="h-5 w-5 text-accent-primary" />
                Factor Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-text-secondary">
                Upload your backtest results to automatically compute features and run regression
                analysis. We'll identify which factors are truly driving your PnL, drawdown,
                and other KPIs.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-background-tertiary rounded-lg">
                  <BarChart3 className="h-8 w-8 text-accent-primary mb-2" />
                  <h4 className="font-medium text-text-primary">Feature Engineering</h4>
                  <p className="text-sm text-text-muted mt-1">
                    Automatic computation of market features and technical indicators
                  </p>
                </div>
                <div className="p-4 bg-background-tertiary rounded-lg">
                  <TrendingUp className="h-8 w-8 text-success mb-2" />
                  <h4 className="font-medium text-text-primary">Regression Analysis</h4>
                  <p className="text-sm text-text-muted mt-1">
                    Linear and non-linear regression to identify key drivers
                  </p>
                </div>
                <div className="p-4 bg-background-tertiary rounded-lg">
                  <Settings2 className="h-8 w-8 text-warning mb-2" />
                  <h4 className="font-medium text-text-primary">SHAP Explainability</h4>
                  <p className="text-sm text-text-muted mt-1">
                    ML-based feature importance with full interpretability
                  </p>
                </div>
              </div>

              <div className="flex justify-end gap-3">
                <Button
                  variant="outline"
                  onClick={() => {
                    const sample = generateSampleTrades();
                    setTrades(sample);
                    setResult(null);
                    toast.success("Loaded sample trades");
                  }}
                >
                  Use Sample Trades
                </Button>
                <Button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  className="bg-accent-gradient"
                >
                  {isAnalyzing ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : (
                    <Settings2 className="h-4 w-4 mr-2" />
                  )}
                  Run Analysis
                </Button>
              </div>
            </CardContent>
          </Card>

          {result && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="text-sm text-text-muted">R²</div>
                    <div className="text-2xl font-bold text-text-primary">
                      {result.r_squared.toFixed(3)}
                    </div>
                  </CardContent>
                </Card>
                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="text-sm text-text-muted">Adj. R²</div>
                    <div className="text-2xl font-bold text-text-primary">
                      {result.adjusted_r_squared.toFixed(3)}
                    </div>
                  </CardContent>
                </Card>
                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="text-sm text-text-muted">Durbin-Watson</div>
                    <div className="text-2xl font-bold text-text-primary">
                      {result.durbin_watson.toFixed(2)}
                    </div>
                  </CardContent>
                </Card>
                <Card className="bg-background-card border-border-primary">
                  <CardContent className="p-4">
                    <div className="text-sm text-text-muted">Residuals Normal</div>
                    <div className="text-2xl font-bold text-text-primary">
                      {result.residuals_normality ? "Yes" : "No"}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="bg-background-card border-border-primary">
                <CardHeader>
                  <CardTitle className="text-lg">Factor Coefficients</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {result.factors.length === 0 ? (
                      <div className="text-sm text-text-muted">
                        No factors returned (need more trades).
                      </div>
                    ) : (
                      result.factors.map((factor) => (
                        <div
                          key={factor.name}
                          className="flex items-center justify-between p-3 bg-background-tertiary rounded-lg"
                        >
                          <div className="flex items-center gap-2">
                            <span className="text-text-primary">{factor.name}</span>
                            {factor.significance && (
                              <span className="text-xs text-text-muted font-mono">
                                {factor.significance}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-4 font-mono text-sm">
                            <span
                              className={
                                factor.coefficient >= 0 ? "text-success" : "text-error"
                              }
                            >
                              {factor.coefficient >= 0 ? "+" : ""}
                              {factor.coefficient.toFixed(4)}
                            </span>
                            <span className="text-text-muted">
                              p={factor.p_value.toFixed(3)}
                            </span>
                          </div>
                        </div>
                      ))
                    )}
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
