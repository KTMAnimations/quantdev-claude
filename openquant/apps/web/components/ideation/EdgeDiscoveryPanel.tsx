"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2, TrendingUp, BarChart3, Zap } from "lucide-react";

interface EdgeResult {
  feature_name: string;
  statistical_significance: {
    correlation_1d: number;
    ic_mean: number;
    ic_ir: number;
    p_value: number;
    is_significant: boolean;
    quantile_returns: Record<string, any>;
  };
  ml_importance: {
    cv_accuracy: number;
    has_predictive_power: boolean;
    feature_importance: Record<string, number>;
  };
  confidence_intervals: {
    mean_return: number;
    ci_lower_95: number;
    ci_upper_95: number;
    probability_positive: number;
  };
  recommendation: string;
}

function StatItem({
  label,
  value,
  isPositive,
}: {
  label: string;
  value: string;
  isPositive: boolean;
}) {
  return (
    <div className="p-3 bg-background-tertiary rounded-lg">
      <div className="text-xs text-text-muted mb-1">{label}</div>
      <div
        className={`font-mono font-semibold ${
          isPositive ? "text-success" : "text-text-primary"
        }`}
      >
        {value}
      </div>
    </div>
  );
}

export function EdgeDiscoveryPanel() {
  const [featureDescription, setFeatureDescription] = useState("");
  const [symbol, setSymbol] = useState("SPY");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<EdgeResult | null>(null);

  const handleAnalyze = async () => {
    if (!featureDescription.trim()) return;

    setIsAnalyzing(true);
    // Simulate API call - in production this would call the backend
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Mock result for demo
    setResult({
      feature_name: featureDescription,
      statistical_significance: {
        correlation_1d: 0.0234,
        ic_mean: 0.0156,
        ic_ir: 0.42,
        p_value: 0.032,
        is_significant: true,
        quantile_returns: {
          Q1: { mean_return: -0.0012, sharpe: -0.32, count: 50 },
          Q2: { mean_return: 0.0003, sharpe: 0.12, count: 50 },
          Q3: { mean_return: 0.0008, sharpe: 0.28, count: 50 },
          Q4: { mean_return: 0.0015, sharpe: 0.45, count: 50 },
          Q5: { mean_return: 0.0028, sharpe: 0.68, count: 50 },
          long_short_spread: 0.004,
        },
      },
      ml_importance: {
        cv_accuracy: 0.543,
        has_predictive_power: true,
        feature_importance: { feature: 0.35, lag_1: 0.25, lag_2: 0.2, volume: 0.2 },
      },
      confidence_intervals: {
        mean_return: 0.0023,
        ci_lower_95: 0.0008,
        ci_upper_95: 0.0038,
        probability_positive: 0.87,
      },
      recommendation: "MODERATE EDGE - Strategy shows promise but needs further validation.",
    });

    setIsAnalyzing(false);
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card className="bg-background-card border-border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-accent-primary" />
            Discover Your Edge
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm text-text-secondary mb-2 block">
              Describe your trading feature in plain English
            </label>
            <Input
              placeholder="e.g., RSI crosses above 70 after being below 30 for 3+ days"
              value={featureDescription}
              onChange={(e) => setFeatureDescription(e.target.value)}
              className="bg-background-tertiary border-border-primary"
            />
          </div>

          <div className="flex gap-4">
            <Input
              placeholder="Symbol"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              className="w-32 bg-background-tertiary border-border-primary"
            />
            <Button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !featureDescription.trim()}
              className="bg-accent-gradient"
            >
              {isAnalyzing ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <TrendingUp className="h-4 w-4 mr-2" />
              )}
              Analyze Edge
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Results Section */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Statistical Significance Card */}
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-accent-primary" />
                Statistical Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <StatItem
                  label="Information Coefficient"
                  value={result.statistical_significance.ic_mean.toFixed(4)}
                  isPositive={result.statistical_significance.ic_mean > 0}
                />
                <StatItem
                  label="IC IR"
                  value={result.statistical_significance.ic_ir.toFixed(2)}
                  isPositive={result.statistical_significance.ic_ir > 0.5}
                />
                <StatItem
                  label="P-Value"
                  value={result.statistical_significance.p_value.toFixed(4)}
                  isPositive={result.statistical_significance.p_value < 0.05}
                />
                <StatItem
                  label="Statistically Significant"
                  value={
                    result.statistical_significance.is_significant ? "Yes" : "No"
                  }
                  isPositive={result.statistical_significance.is_significant}
                />
              </div>
            </CardContent>
          </Card>

          {/* ML Analysis Card */}
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="text-lg">ML Pattern Detection</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-text-secondary">CV Accuracy</span>
                  <span
                    className={`font-mono ${
                      result.ml_importance.cv_accuracy > 0.52
                        ? "text-success"
                        : "text-text-primary"
                    }`}
                  >
                    {(result.ml_importance.cv_accuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-text-secondary">Predictive Power</span>
                  <span
                    className={
                      result.ml_importance.has_predictive_power
                        ? "text-success"
                        : "text-error"
                    }
                  >
                    {result.ml_importance.has_predictive_power
                      ? "Detected"
                      : "Weak"}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Confidence Intervals Card */}
          <Card className="bg-background-card border-border-primary lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Bootstrap Confidence Intervals</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <StatItem
                  label="Mean Return"
                  value={`${(result.confidence_intervals.mean_return * 100).toFixed(2)}%`}
                  isPositive={result.confidence_intervals.mean_return > 0}
                />
                <StatItem
                  label="95% CI Lower"
                  value={`${(result.confidence_intervals.ci_lower_95 * 100).toFixed(2)}%`}
                  isPositive={result.confidence_intervals.ci_lower_95 > 0}
                />
                <StatItem
                  label="95% CI Upper"
                  value={`${(result.confidence_intervals.ci_upper_95 * 100).toFixed(2)}%`}
                  isPositive={result.confidence_intervals.ci_upper_95 > 0}
                />
                <StatItem
                  label="P(Positive)"
                  value={`${(result.confidence_intervals.probability_positive * 100).toFixed(1)}%`}
                  isPositive={result.confidence_intervals.probability_positive > 0.5}
                />
              </div>
            </CardContent>
          </Card>

          {/* Recommendation Card */}
          <Card className="bg-background-card border-border-primary lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Recommendation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-accent-primary/10 rounded-lg border border-accent-primary/30">
                <p className="text-text-primary font-medium">
                  {result.recommendation}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
