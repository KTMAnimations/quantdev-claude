"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";

interface MonteCarloChartProps {
  equityCurves: number[][];
  originalCurve: number[];
  percentiles: {
    p5: number[];
    p50: number[];
    p95: number[];
  };
  width?: number;
  height?: number;
}

export function MonteCarloChart({
  equityCurves,
  originalCurve,
  percentiles,
  width = 800,
  height = 400
}: MonteCarloChartProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear()
      .domain([0, originalCurve.length - 1])
      .range([0, innerWidth]);

    const allValues = equityCurves.flat().concat(originalCurve);
    const yScale = d3.scaleLinear()
      .domain([d3.min(allValues)! * 0.95, d3.max(allValues)! * 1.05])
      .range([innerHeight, 0]);

    // Draw confidence bands
    const areaGenerator = d3.area<number>()
      .x((_, i) => xScale(i))
      .y0((_, i) => yScale(percentiles.p5[i]))
      .y1((_, i) => yScale(percentiles.p95[i]));

    g.append("path")
      .datum(percentiles.p50)
      .attr("fill", "rgba(139, 92, 246, 0.15)")
      .attr("d", areaGenerator);

    // Draw simulated equity curves (sample)
    const lineGenerator = d3.line<number>()
      .x((_, i) => xScale(i))
      .y(d => yScale(d));

    // Draw sample of simulations
    const sampleCurves = equityCurves.slice(0, 50);
    sampleCurves.forEach(curve => {
      g.append("path")
        .datum(curve)
        .attr("fill", "none")
        .attr("stroke", "rgba(139, 92, 246, 0.1)")
        .attr("stroke-width", 1)
        .attr("d", lineGenerator);
    });

    // Draw median line
    g.append("path")
      .datum(percentiles.p50)
      .attr("fill", "none")
      .attr("stroke", "#8b5cf6")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", "4,4")
      .attr("d", lineGenerator);

    // Draw original equity curve
    g.append("path")
      .datum(originalCurve)
      .attr("fill", "none")
      .attr("stroke", "#22c55e")
      .attr("stroke-width", 2.5)
      .attr("d", lineGenerator);

    // Axes
    const xAxis = d3.axisBottom(xScale)
      .ticks(10)
      .tickFormat(d => `${d}`);

    const yAxis = d3.axisLeft(yScale)
      .ticks(8)
      .tickFormat(d => `${(d as number).toFixed(2)}`);

    g.append("g")
      .attr("transform", `translate(0,${innerHeight})`)
      .call(xAxis)
      .attr("color", "#64748b");

    g.append("g")
      .call(yAxis)
      .attr("color", "#64748b");

    // Labels
    g.append("text")
      .attr("x", innerWidth / 2)
      .attr("y", innerHeight + 35)
      .attr("text-anchor", "middle")
      .attr("fill", "#94a3b8")
      .attr("font-size", "12px")
      .text("Trade Number");

    g.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -innerHeight / 2)
      .attr("y", -45)
      .attr("text-anchor", "middle")
      .attr("fill", "#94a3b8")
      .attr("font-size", "12px")
      .text("Equity Multiple");

    // Legend
    const legend = g.append("g")
      .attr("transform", `translate(${innerWidth - 150}, 10)`);

    legend.append("line")
      .attr("x1", 0).attr("x2", 20)
      .attr("y1", 0).attr("y2", 0)
      .attr("stroke", "#22c55e")
      .attr("stroke-width", 2.5);
    legend.append("text")
      .attr("x", 25).attr("y", 4)
      .attr("fill", "#94a3b8")
      .attr("font-size", "11px")
      .text("Original");

    legend.append("line")
      .attr("x1", 0).attr("x2", 20)
      .attr("y1", 20).attr("y2", 20)
      .attr("stroke", "#8b5cf6")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", "4,4");
    legend.append("text")
      .attr("x", 25).attr("y", 24)
      .attr("fill", "#94a3b8")
      .attr("font-size", "11px")
      .text("Median (50th)");

    legend.append("rect")
      .attr("x", 0).attr("y", 35)
      .attr("width", 20).attr("height", 10)
      .attr("fill", "rgba(139, 92, 246, 0.15)");
    legend.append("text")
      .attr("x", 25).attr("y", 44)
      .attr("fill", "#94a3b8")
      .attr("font-size", "11px")
      .text("90% CI");

  }, [equityCurves, originalCurve, percentiles, width, height]);

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      className="bg-background-card rounded-lg"
    />
  );
}
