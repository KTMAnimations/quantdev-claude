"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Star, Download, ThumbsUp, Code2 } from "lucide-react";

const STRATEGIES = [
  {
    id: "1",
    name: "RSI Divergence Strategy",
    author: "QuantTrader",
    description: "Identifies bullish and bearish divergences using RSI and price action",
    category: "momentum",
    votes: 342,
    downloads: 1245,
  },
  {
    id: "2",
    name: "EMA Cross with ATR Stop",
    author: "AlgoMaster",
    description: "Classic EMA crossover strategy with dynamic ATR-based stop losses",
    category: "trend",
    votes: 287,
    downloads: 982,
  },
  {
    id: "3",
    name: "Bollinger Band Mean Reversion",
    author: "StatArb",
    description: "Mean reversion strategy using Bollinger Bands with volatility filter",
    category: "mean_reversion",
    votes: 256,
    downloads: 876,
  },
  {
    id: "4",
    name: "VWAP Scalping Strategy",
    author: "DayTrader Pro",
    description: "Intraday scalping strategy based on VWAP deviations",
    category: "scalping",
    votes: 198,
    downloads: 654,
  },
  {
    id: "5",
    name: "Multi-Timeframe Trend",
    author: "SwingTrader",
    description: "Aligns trades with higher timeframe trend direction",
    category: "trend",
    votes: 176,
    downloads: 543,
  },
  {
    id: "6",
    name: "Volume Profile Strategy",
    author: "VolumeWizard",
    description: "Uses volume profile levels for entries and exits",
    category: "volume",
    votes: 154,
    downloads: 432,
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
                    <Button size="sm" variant="outline">
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
