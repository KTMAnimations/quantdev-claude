"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Activity, Target } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon: React.ReactNode;
}

function StatCard({ title, value, change, changeType, icon }: StatCardProps) {
  return (
    <Card className="bg-background-card border-border-primary">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-text-secondary">
          {title}
        </CardTitle>
        <div className="h-8 w-8 rounded-lg bg-accent-primary/10 flex items-center justify-center">
          {icon}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-text-primary">{value}</div>
        {change && (
          <p
            className={`text-xs mt-1 ${
              changeType === "positive"
                ? "text-success"
                : changeType === "negative"
                ? "text-error"
                : "text-text-muted"
            }`}
          >
            {changeType === "positive" && "+"}
            {change}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

interface StatsCardsProps {
  stats?: {
    totalStrategies: number;
    totalBacktests: number;
    avgSharpe: number;
    winRate: number;
  };
}

export function StatsCards({ stats }: StatsCardsProps) {
  const defaultStats = {
    totalStrategies: 12,
    totalBacktests: 47,
    avgSharpe: 1.42,
    winRate: 58.3,
  };

  const data = stats || defaultStats;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Total Strategies"
        value={data.totalStrategies.toString()}
        change="2 this week"
        changeType="positive"
        icon={<Activity className="h-4 w-4 text-accent-primary" />}
      />
      <StatCard
        title="Backtests Run"
        value={data.totalBacktests.toString()}
        change="5 this week"
        changeType="positive"
        icon={<Target className="h-4 w-4 text-accent-primary" />}
      />
      <StatCard
        title="Avg Sharpe Ratio"
        value={data.avgSharpe.toFixed(2)}
        change="0.12 vs last month"
        changeType="positive"
        icon={<TrendingUp className="h-4 w-4 text-accent-primary" />}
      />
      <StatCard
        title="Avg Win Rate"
        value={`${data.winRate.toFixed(1)}%`}
        change="2.1% vs last month"
        changeType="negative"
        icon={<TrendingDown className="h-4 w-4 text-accent-primary" />}
      />
    </div>
  );
}
