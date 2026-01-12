"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  ComposedChart,
} from "recharts";

interface EquityCurveProps {
  data: { date: string; equity: number; drawdown?: number }[];
  showDrawdown?: boolean;
}

export function EquityCurve({ data, showDrawdown = false }: EquityCurveProps) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
        <XAxis
          dataKey="date"
          stroke="#64748b"
          tick={{ fill: "#64748b", fontSize: 12 }}
        />
        <YAxis
          yAxisId="equity"
          stroke="#64748b"
          tick={{ fill: "#64748b", fontSize: 12 }}
          tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
        />
        {showDrawdown && (
          <YAxis
            yAxisId="drawdown"
            orientation="right"
            stroke="#64748b"
            tick={{ fill: "#64748b", fontSize: 12 }}
            tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
          />
        )}
        <Tooltip
          contentStyle={{
            backgroundColor: "#16161e",
            border: "1px solid #27272a",
            borderRadius: "8px",
          }}
          labelStyle={{ color: "#f8fafc" }}
          itemStyle={{ color: "#94a3b8" }}
        />
        {showDrawdown && (
          <Area
            yAxisId="drawdown"
            type="monotone"
            dataKey="drawdown"
            fill="rgba(239, 68, 68, 0.2)"
            stroke="#ef4444"
            strokeWidth={1}
            name="Drawdown"
          />
        )}
        <Line
          yAxisId="equity"
          type="monotone"
          dataKey="equity"
          stroke="#8b5cf6"
          strokeWidth={2}
          dot={false}
          name="Equity"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
