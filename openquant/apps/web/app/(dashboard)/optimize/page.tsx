"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Settings2, TrendingUp, BarChart3 } from "lucide-react";

export default function OptimizePage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsAnalyzing(false);
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

              <div className="flex justify-end">
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

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-background-card border-border-primary">
              <CardHeader>
                <CardTitle className="text-lg">Top Positive Factors</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {["RSI Momentum", "Volume Spike", "Trend Alignment", "Volatility Expansion"].map(
                    (factor, i) => (
                      <div
                        key={factor}
                        className="flex items-center justify-between p-3 bg-background-tertiary rounded-lg"
                      >
                        <span className="text-text-primary">{factor}</span>
                        <span className="text-success font-mono">
                          +{(0.15 - i * 0.03).toFixed(2)}
                        </span>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="bg-background-card border-border-primary">
              <CardHeader>
                <CardTitle className="text-lg">Top Negative Factors</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {["News Events", "Low Liquidity", "Counter-Trend", "High Correlation"].map(
                    (factor, i) => (
                      <div
                        key={factor}
                        className="flex items-center justify-between p-3 bg-background-tertiary rounded-lg"
                      >
                        <span className="text-text-primary">{factor}</span>
                        <span className="text-error font-mono">
                          -{(0.12 - i * 0.02).toFixed(2)}
                        </span>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
