"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2, Rocket, DollarSign, Target, AlertTriangle, TrendingUp } from "lucide-react";

const PROP_FIRMS = [
  { id: "ftmo", name: "FTMO", cost: 540, accountSize: 100000, profitSplit: 80 },
  { id: "the5ers", name: "The5%ers", cost: 235, accountSize: 100000, profitSplit: 80 },
  { id: "apex", name: "Apex Trader", cost: 167, accountSize: 100000, profitSplit: 90 },
  { id: "e8", name: "E8 Markets", cost: 228, accountSize: 100000, profitSplit: 80 },
];

interface SimulationResult {
  prop_firm: string;
  combined_pass_rate: number;
  phase1: {
    pass_rate: number;
    fail_reasons: {
      daily_drawdown: number;
      total_drawdown: number;
      time_expired: number;
    };
    avg_days_to_pass: number;
  };
  expected_value: {
    expected_value: number;
    roi: number;
    break_even_pass_rate: number;
    recommendation: {
      verdict: string;
      color: string;
      description: string;
    };
  };
  funded_simulation: {
    survival_rate: number;
    expected_monthly_profit: number;
  };
}

export default function DeployPage() {
  const [selectedFirm, setSelectedFirm] = useState("ftmo");
  const [isSimulating, setIsSimulating] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);

  const handleSimulate = async () => {
    setIsSimulating(true);
    await new Promise((resolve) => setTimeout(resolve, 2500));

    const firm = PROP_FIRMS.find((f) => f.id === selectedFirm)!;

    setResult({
      prop_firm: firm.name,
      combined_pass_rate: 0.34,
      phase1: {
        pass_rate: 0.42,
        fail_reasons: {
          daily_drawdown: 0.28,
          total_drawdown: 0.22,
          time_expired: 0.08,
        },
        avg_days_to_pass: 18,
      },
      expected_value: {
        expected_value: 2450,
        roi: 4.5,
        break_even_pass_rate: 0.12,
        recommendation: {
          verdict: "RECOMMENDED",
          color: "green",
          description: "Positive expected value. Worth attempting with proper risk management.",
        },
      },
      funded_simulation: {
        survival_rate: 0.72,
        expected_monthly_profit: 3200,
      },
    });

    setIsSimulating(false);
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
        title="Prop Firm Simulator"
        subtitle="Simulate your odds of passing major prop firm challenges"
      />
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="space-y-6">
          {/* Prop Firm Selection */}
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-accent-primary" />
                Select Prop Firm
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs value={selectedFirm} onValueChange={setSelectedFirm}>
                <TabsList className="grid grid-cols-4 w-full">
                  {PROP_FIRMS.map((firm) => (
                    <TabsTrigger key={firm.id} value={firm.id}>
                      {firm.name}
                    </TabsTrigger>
                  ))}
                </TabsList>
                {PROP_FIRMS.map((firm) => (
                  <TabsContent key={firm.id} value={firm.id}>
                    <div className="grid grid-cols-3 gap-4 mt-4">
                      <div className="p-4 bg-background-tertiary rounded-lg">
                        <div className="text-sm text-text-muted">Challenge Cost</div>
                        <div className="text-xl font-bold text-text-primary">
                          ${firm.cost}
                        </div>
                      </div>
                      <div className="p-4 bg-background-tertiary rounded-lg">
                        <div className="text-sm text-text-muted">Account Size</div>
                        <div className="text-xl font-bold text-text-primary">
                          ${firm.accountSize.toLocaleString()}
                        </div>
                      </div>
                      <div className="p-4 bg-background-tertiary rounded-lg">
                        <div className="text-sm text-text-muted">Profit Split</div>
                        <div className="text-xl font-bold text-text-primary">
                          {firm.profitSplit}%
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                ))}
              </Tabs>

              <div className="flex justify-end mt-6">
                <Button
                  onClick={handleSimulate}
                  disabled={isSimulating}
                  className="bg-accent-gradient"
                >
                  {isSimulating ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : (
                    <Rocket className="h-4 w-4 mr-2" />
                  )}
                  Run Simulation
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <>
              {/* Recommendation Card */}
              <Card className={`border ${getVerdictColor(result.expected_value.recommendation.color)}`}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-2xl font-bold">
                        {result.expected_value.recommendation.verdict}
                      </h3>
                      <p className="text-text-secondary mt-1">
                        {result.expected_value.recommendation.description}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-text-muted">Expected Value</div>
                      <div className="text-3xl font-bold text-success">
                        ${result.expected_value.expected_value.toLocaleString()}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Pass Rate Analysis */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-background-card border-border-primary">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-accent-primary" />
                      Pass Rate Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="text-text-secondary">Combined Pass Rate</span>
                        <span className="text-2xl font-bold text-text-primary">
                          {(result.combined_pass_rate * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-text-secondary">Phase 1 Pass Rate</span>
                        <span className="text-xl font-bold text-text-primary">
                          {(result.phase1.pass_rate * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-text-secondary">Avg Days to Pass</span>
                        <span className="text-xl font-bold text-text-primary">
                          {result.phase1.avg_days_to_pass}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-text-secondary">Break-Even Pass Rate</span>
                        <span className="text-xl font-bold text-accent-primary">
                          {(result.expected_value.break_even_pass_rate * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-background-card border-border-primary">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5 text-warning" />
                      Failure Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-text-muted">Daily Drawdown Breach</span>
                          <span className="text-error">
                            {(result.phase1.fail_reasons.daily_drawdown * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                          <div
                            className="h-full bg-error"
                            style={{
                              width: `${result.phase1.fail_reasons.daily_drawdown * 100}%`,
                            }}
                          />
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-text-muted">Total Drawdown Breach</span>
                          <span className="text-warning">
                            {(result.phase1.fail_reasons.total_drawdown * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                          <div
                            className="h-full bg-warning"
                            style={{
                              width: `${result.phase1.fail_reasons.total_drawdown * 100}%`,
                            }}
                          />
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-text-muted">Time Expired</span>
                          <span className="text-text-muted">
                            {(result.phase1.fail_reasons.time_expired * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                          <div
                            className="h-full bg-text-muted"
                            style={{
                              width: `${result.phase1.fail_reasons.time_expired * 100}%`,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Funded Account Projection */}
              <Card className="bg-background-card border-border-primary">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-success" />
                    Funded Account Projection (12 months)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <div className="text-sm text-text-muted mb-2">Survival Rate</div>
                      <div className="text-2xl font-bold text-text-primary">
                        {(result.funded_simulation.survival_rate * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-text-muted">
                        Probability of staying funded for 12 months
                      </div>
                    </div>
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <div className="text-sm text-text-muted mb-2">Expected Monthly Profit</div>
                      <div className="text-2xl font-bold text-success">
                        ${result.funded_simulation.expected_monthly_profit.toLocaleString()}
                      </div>
                      <div className="text-sm text-text-muted">
                        Average monthly payout if funded
                      </div>
                    </div>
                    <div className="p-4 bg-background-tertiary rounded-lg">
                      <div className="text-sm text-text-muted mb-2">ROI</div>
                      <div className="text-2xl font-bold text-accent-primary">
                        {(result.expected_value.roi * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-text-muted">
                        Return on challenge investment
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
