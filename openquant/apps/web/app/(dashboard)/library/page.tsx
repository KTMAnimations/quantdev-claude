"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Star, Download, ThumbsUp, Code2 } from "lucide-react";
import { useStrategyStore } from "@/lib/strategyStore";
import { toast } from "sonner";

const STRATEGIES = [
  {
    id: "1",
    name: "RSI Divergence Strategy",
    author: "QuantTrader",
    description: "Identifies bullish and bearish divergences using RSI and price action",
    category: "momentum",
    votes: 342,
    downloads: 1245,
    pineCode: `//@version=5
strategy("RSI Divergence Strategy", overlay=false)

rsiLength = input.int(14, "RSI Length", minval=1)
overbought = input.int(70, "Overbought Level")
oversold = input.int(30, "Oversold Level")

rsiValue = ta.rsi(close, rsiLength)
longCondition = ta.crossover(rsiValue, oversold)
shortCondition = ta.crossunder(rsiValue, overbought)

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

plot(rsiValue, "RSI", color.purple)
hline(overbought, "Overbought", color.red)
hline(oversold, "Oversold", color.green)
`,
  },
  {
    id: "2",
    name: "EMA Cross with ATR Stop",
    author: "AlgoMaster",
    description: "Classic EMA crossover strategy with dynamic ATR-based stop losses",
    category: "trend",
    votes: 287,
    downloads: 982,
    pineCode: `//@version=5
strategy("EMA Cross with ATR Stop", overlay=true)

fastLength = input.int(9, "Fast EMA")
slowLength = input.int(21, "Slow EMA")
atrLength = input.int(14, "ATR Length")
atrMultiplier = input.float(2.0, "ATR Multiplier")

fastEMA = ta.ema(close, fastLength)
slowEMA = ta.ema(close, slowLength)
atrValue = ta.atr(atrLength)

longCondition = ta.crossover(fastEMA, slowEMA)
shortCondition = ta.crossunder(fastEMA, slowEMA)

if longCondition
    stopLoss = close - atrValue * atrMultiplier
    takeProfit = close + atrValue * atrMultiplier * 2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=stopLoss, limit=takeProfit)

if shortCondition
    stopLoss = close + atrValue * atrMultiplier
    takeProfit = close - atrValue * atrMultiplier * 2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=stopLoss, limit=takeProfit)

plot(fastEMA, "Fast EMA", color.blue)
plot(slowEMA, "Slow EMA", color.orange)
`,
  },
  {
    id: "3",
    name: "Bollinger Band Mean Reversion",
    author: "StatArb",
    description: "Mean reversion strategy using Bollinger Bands with volatility filter",
    category: "mean_reversion",
    votes: 256,
    downloads: 876,
    pineCode: `//@version=5
strategy("Bollinger Mean Reversion", overlay=true)

length = input.int(20, "Length")
mult = input.float(2.0, "Multiplier")

basis = ta.sma(close, length)
dev = mult * ta.stdev(close, length)
upper = basis + dev
lower = basis - dev

longCondition = ta.crossover(close, lower)
shortCondition = ta.crossunder(close, upper)

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

plot(basis, "Basis", color.orange)
p1 = plot(upper, "Upper", color.blue)
p2 = plot(lower, "Lower", color.blue)
fill(p1, p2, color=color.new(color.blue, 90))
`,
  },
  {
    id: "4",
    name: "VWAP Scalping Strategy",
    author: "DayTrader Pro",
    description: "Intraday scalping strategy based on VWAP deviations",
    category: "scalping",
    votes: 198,
    downloads: 654,
    pineCode: `//@version=5
strategy("VWAP Scalping", overlay=true)

vwapValue = ta.vwap(hlc3)
longCondition = ta.crossover(close, vwapValue)
shortCondition = ta.crossunder(close, vwapValue)

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

plot(vwapValue, "VWAP", color.purple)
`,
  },
  {
    id: "5",
    name: "Multi-Timeframe Trend",
    author: "SwingTrader",
    description: "Aligns trades with higher timeframe trend direction",
    category: "trend",
    votes: 176,
    downloads: 543,
    pineCode: `//@version=5
strategy("Multi-Timeframe Trend", overlay=true)

fast = input.int(20, "Fast SMA")
slow = input.int(50, "Slow SMA")

fastSma = ta.sma(close, fast)
slowSma = ta.sma(close, slow)

trendUp = fastSma > slowSma
longCondition = ta.crossover(close, fastSma) and trendUp
shortCondition = ta.crossunder(close, fastSma) and not trendUp

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

plot(fastSma, "Fast SMA", color.blue)
plot(slowSma, "Slow SMA", color.orange)
`,
  },
  {
    id: "6",
    name: "Volume Profile Strategy",
    author: "VolumeWizard",
    description: "Uses volume profile levels for entries and exits",
    category: "volume",
    votes: 154,
    downloads: 432,
    pineCode: `//@version=5
strategy("Volume Profile Strategy (Template)", overlay=true)

// Note: full volume profile requires additional logic/data.
maLength = input.int(50, "MA Length")
ma = ta.sma(close, maLength)

longCondition = ta.crossover(close, ma)
shortCondition = ta.crossunder(close, ma)

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

plot(ma, "MA", color.purple)
`,
  },
];

const CATEGORIES = [
  { id: "all", name: "All" },
  { id: "trend", name: "Trend Following" },
  { id: "momentum", name: "Momentum" },
  { id: "mean_reversion", name: "Mean Reversion" },
  { id: "scalping", name: "Scalping" },
  { id: "volume", name: "Volume" },
];

export default function LibraryPage() {
  const router = useRouter();
  const setPineCode = useStrategyStore((s) => s.setPineCode);

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");

  const filteredStrategies = STRATEGIES.filter((strategy) => {
    const matchesSearch =
      strategy.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      strategy.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory =
      selectedCategory === "all" || strategy.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Strategy Library"
        subtitle="Browse and download community strategies"
      />
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="space-y-6">
          {/* Search and Filters */}
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
              <Input
                placeholder="Search strategies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 bg-background-tertiary border-border-primary"
              />
            </div>
          </div>

          {/* Category Tabs */}
          <Tabs value={selectedCategory} onValueChange={setSelectedCategory}>
            <TabsList>
              {CATEGORIES.map((category) => (
                <TabsTrigger key={category.id} value={category.id}>
                  {category.name}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>

          {/* Strategy Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredStrategies.map((strategy) => (
              <Card
                key={strategy.id}
                className="bg-background-card border-border-primary hover:border-accent-primary/50 transition-all duration-300"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{strategy.name}</CardTitle>
                      <p className="text-sm text-text-muted mt-1">by {strategy.author}</p>
                    </div>
                    <Button variant="ghost" size="icon">
                      <Star className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-text-secondary text-sm mb-4">
                    {strategy.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-sm text-text-muted">
                      <span className="flex items-center gap-1">
                        <ThumbsUp className="h-3 w-3" />
                        {strategy.votes}
                      </span>
                      <span className="flex items-center gap-1">
                        <Download className="h-3 w-3" />
                        {strategy.downloads}
                      </span>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setPineCode(strategy.pineCode);
                        toast.success("Opened in Code editor");
                        router.push("/code");
                      }}
                    >
                      <Code2 className="h-4 w-4 mr-2" />
                      View Code
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
