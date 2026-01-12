"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface DistributionChartProps {
  data: { bin: string; count: number }[];
  mean?: number;
  title?: string;
  color?: string;
}

export function DistributionChart({
  data,
  mean,
  title,
  color = "#8b5cf6",
}: DistributionChartProps) {
  return (
    <div>
      {title && (
        <h4 className="text-sm font-medium text-text-secondary mb-4">{title}</h4>
      )}
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
          <XAxis
            dataKey="bin"
            stroke="#64748b"
            tick={{ fill: "#64748b", fontSize: 10 }}
            angle={-45}
            textAnchor="end"
            height={60}
          />
          <YAxis
            stroke="#64748b"
            tick={{ fill: "#64748b", fontSize: 12 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#16161e",
              border: "1px solid #27272a",
              borderRadius: "8px",
            }}
            labelStyle={{ color: "#f8fafc" }}
            itemStyle={{ color: "#94a3b8" }}
          />
          <Bar dataKey="count" fill={color} radius={[4, 4, 0, 0]} />
          {mean !== undefined && (
            <ReferenceLine
              x={mean.toString()}
              stroke="#22c55e"
              strokeDasharray="5 5"
              label={{
                value: "Mean",
                fill: "#22c55e",
                fontSize: 12,
              }}
            />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
