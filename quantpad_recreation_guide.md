# QuantPad Recreation Guide: Complete AI Agent Prompt

## MISSION STATEMENT

You are tasked with building **OpenQuant** - a 1:1 open-source recreation of QuantPad.ai using free and open-source tools. This document provides everything needed to build a production-ready quant trading platform with the same features, UI/UX, and functionality.

---

## PART 1: DESIGN SYSTEM & VISUAL IDENTITY

### 1.1 Color Palette (Extract from QuantPad)

```css
:root {
  /* Primary Dark Theme - QuantPad uses deep dark backgrounds */
  --background-primary: #0a0a0f;
  --background-secondary: #111118;
  --background-tertiary: #1a1a24;
  --background-card: #16161e;
  --background-elevated: #1e1e2a;
  
  /* Accent Colors - Purple/Blue gradient accent */
  --accent-primary: #8b5cf6;      /* Violet-500 */
  --accent-secondary: #a78bfa;    /* Violet-400 */
  --accent-tertiary: #6366f1;     /* Indigo-500 */
  --accent-gradient: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  
  /* Text Colors */
  --text-primary: #f8fafc;        /* Slate-50 */
  --text-secondary: #94a3b8;      /* Slate-400 */
  --text-muted: #64748b;          /* Slate-500 */
  --text-disabled: #475569;       /* Slate-600 */
  
  /* Status Colors */
  --success: #22c55e;             /* Green-500 */
  --success-muted: #16a34a;
  --warning: #eab308;             /* Yellow-500 */
  --error: #ef4444;               /* Red-500 */
  --info: #3b82f6;                /* Blue-500 */
  
  /* Chart Colors (Monte Carlo simulations, equity curves) */
  --chart-positive: #22c55e;
  --chart-negative: #ef4444;
  --chart-neutral: #8b5cf6;
  --chart-line-1: #8b5cf6;
  --chart-line-2: #06b6d4;
  --chart-line-3: #f59e0b;
  --chart-area-fill: rgba(139, 92, 246, 0.1);
  --chart-confidence-band: rgba(139, 92, 246, 0.15);
  
  /* Border & Dividers */
  --border-primary: #27272a;
  --border-secondary: #3f3f46;
  --border-accent: rgba(139, 92, 246, 0.3);
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 20px rgba(139, 92, 246, 0.3);
  
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}
```

### 1.2 Typography System

```css
/* QuantPad uses Inter font family */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  
  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}

/* Heading Styles */
h1 { font-size: var(--text-4xl); font-weight: 700; letter-spacing: var(--tracking-tight); }
h2 { font-size: var(--text-3xl); font-weight: 600; }
h3 { font-size: var(--text-2xl); font-weight: 600; }
h4 { font-size: var(--text-xl); font-weight: 500; }

/* Code/Pine Script Editor */
.code-editor {
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
}
```

### 1.3 Component Styling Patterns

```css
/* Card Component - Used extensively in QuantPad */
.card {
  background: var(--background-card);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all 0.2s ease;
}

.card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
}

/* Button Styles */
.btn-primary {
  background: var(--accent-gradient);
  color: white;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-secondary);
  padding: 10px 20px;
  border-radius: var(--radius-md);
}

/* Input Fields */
.input {
  background: var(--background-tertiary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.input:focus {
  border-color: var(--accent-primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

/* Floating Math Formulas (Landing Page Animation) */
.floating-formula {
  font-family: var(--font-mono);
  color: var(--text-muted);
  opacity: 0.4;
  font-size: var(--text-sm);
  position: absolute;
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.2; }
  50% { transform: translateY(-20px) rotate(5deg); opacity: 0.5; }
}
```

---

## PART 2: TECH STACK SPECIFICATION

### 2.1 Frontend Stack

```json
{
  "framework": "Next.js 14+ (App Router)",
  "language": "TypeScript",
  "styling": "Tailwind CSS v4 + shadcn/ui",
  "state": "Zustand + React Query (TanStack Query)",
  "forms": "React Hook Form + Zod",
  "charts": {
    "trading": "TradingView Lightweight Charts",
    "statistics": "Recharts / Plotly.js",
    "monte_carlo": "D3.js + custom canvas"
  },
  "code_editor": "@monaco-editor/react",
  "animations": "Framer Motion",
  "icons": "Lucide React",
  "tables": "TanStack Table"
}
```

### 2.2 Backend Stack

```json
{
  "runtime": "Node.js 20+ / Python FastAPI",
  "api": "tRPC or REST API",
  "database": "PostgreSQL + Prisma ORM",
  "cache": "Redis",
  "queue": "BullMQ (for async ML jobs)",
  "auth": "NextAuth.js / Clerk",
  "file_storage": "S3-compatible (MinIO for self-host)",
  "ml_runtime": "Python with FastAPI microservice"
}
```

### 2.3 ML/Quant Stack (Python Microservice)

```python
# requirements.txt
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
scikit-learn>=1.3.0
statsmodels>=0.14.0
alphalens-reloaded>=0.4.3
pyfolio-reloaded>=0.9.5
vectorbt>=0.25.0
backtesting>=0.3.3
ta-lib>=0.4.28
yfinance>=0.2.28
arch>=6.0.0
shap>=0.43.0
```

---

## PART 3: PROJECT STRUCTURE

```
openquant/
├── apps/
│   ├── web/                          # Next.js frontend
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── sign-in/
│   │   │   │   └── sign-up/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── ideation/         # Edge Discovery
│   │   │   │   ├── code/             # Pine Script Generator
│   │   │   │   ├── test/             # Monte Carlo Testing
│   │   │   │   ├── optimize/         # Regression Analysis
│   │   │   │   ├── deploy/           # Prop Firm Simulator
│   │   │   │   ├── library/          # Strategy Library
│   │   │   │   └── copilot/          # AI Chat Interface
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx              # Landing page
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn components
│   │   │   ├── charts/
│   │   │   │   ├── TradingChart.tsx
│   │   │   │   ├── MonteCarloChart.tsx
│   │   │   │   ├── EquityCurve.tsx
│   │   │   │   ├── ConfidenceIntervals.tsx
│   │   │   │   └── DistributionChart.tsx
│   │   │   ├── editor/
│   │   │   │   ├── PineScriptEditor.tsx
│   │   │   │   └── pine-syntax.ts    # Custom syntax highlighting
│   │   │   ├── dashboard/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── StatsCards.tsx
│   │   │   └── landing/
│   │   │       ├── Hero.tsx
│   │   │       ├── WorkflowSteps.tsx
│   │   │       ├── Features.tsx
│   │   │       └── FloatingFormulas.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── utils.ts
│   │   │   └── pine-compiler.ts
│   │   └── styles/
│   │       └── globals.css
│   │
│   └── api/                          # Python FastAPI backend
│       ├── app/
│       │   ├── main.py
│       │   ├── routers/
│       │   │   ├── ideation.py       # Edge discovery endpoints
│       │   │   ├── backtest.py       # Backtesting endpoints
│       │   │   ├── monte_carlo.py    # MC simulation endpoints
│       │   │   ├── regression.py     # Factor analysis endpoints
│       │   │   ├── pine_gen.py       # Pine Script generation
│       │   │   └── prop_firm.py      # Prop firm simulation
│       │   ├── services/
│       │   │   ├── edge_discovery.py
│       │   │   ├── monte_carlo_service.py
│       │   │   ├── backtest_service.py
│       │   │   ├── regression_service.py
│       │   │   ├── pine_generator.py
│       │   │   └── prop_firm_simulator.py
│       │   ├── models/
│       │   │   └── schemas.py
│       │   └── utils/
│       │       ├── statistics.py
│       │       └── data_fetcher.py
│       └── requirements.txt
│
├── packages/
│   ├── pine-parser/                  # Pine Script parser/validator
│   ├── trading-indicators/           # TA library wrapper
│   └── shared-types/                 # TypeScript types
│
├── docker-compose.yml
├── package.json
└── turbo.json
```

---

## PART 4: FEATURE IMPLEMENTATION GUIDE

### 4.1 FEATURE: Edge Discovery (Ideation)

**QuantPad Description:** "Describe any feature in plain English, and QuantPad instantly tests whether it predicts market movement."

#### Backend Implementation (Python)

```python
# api/app/services/edge_discovery.py
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
import shap

class EdgeDiscoveryService:
    """
    Replicates QuantPad's edge discovery using Alphalens + custom ML
    """
    
    def __init__(self):
        self.tscv = TimeSeriesSplit(n_splits=5)
    
    async def analyze_feature(
        self,
        feature_description: str,
        symbol: str,
        timeframe: str,
        lookback_days: int = 252
    ) -> dict:
        """
        Main entry point - analyzes a trading feature/signal
        """
        # 1. Parse natural language to feature logic
        feature_logic = await self._parse_feature_description(feature_description)
        
        # 2. Fetch historical data
        price_data = await self._fetch_data(symbol, timeframe, lookback_days)
        
        # 3. Compute the feature
        feature_values = self._compute_feature(price_data, feature_logic)
        
        # 4. Run statistical analysis
        stats_results = self._run_statistical_tests(feature_values, price_data)
        
        # 5. Run ML analysis for non-linear patterns
        ml_results = self._run_ml_analysis(feature_values, price_data)
        
        # 6. Compute confidence intervals via bootstrap
        bootstrap_results = self._bootstrap_analysis(feature_values, price_data)
        
        return {
            "feature_name": feature_description,
            "statistical_significance": stats_results,
            "ml_importance": ml_results,
            "confidence_intervals": bootstrap_results,
            "recommendation": self._generate_recommendation(stats_results, ml_results)
        }
    
    def _run_statistical_tests(self, feature: pd.Series, prices: pd.DataFrame) -> dict:
        """
        Run comprehensive statistical tests on the feature
        """
        # Forward returns
        returns_1d = prices['close'].pct_change(1).shift(-1)
        returns_5d = prices['close'].pct_change(5).shift(-5)
        
        # Correlation analysis
        correlation_1d = feature.corr(returns_1d)
        correlation_5d = feature.corr(returns_5d)
        
        # Information Coefficient (IC)
        ic_mean, ic_std = self._calculate_ic(feature, returns_1d)
        
        # T-test for signal vs no-signal periods
        signal_returns = returns_1d[feature > feature.median()]
        no_signal_returns = returns_1d[feature <= feature.median()]
        t_stat, p_value = stats.ttest_ind(signal_returns.dropna(), no_signal_returns.dropna())
        
        # Quantile analysis (Alphalens style)
        quantile_returns = self._quantile_analysis(feature, returns_1d)
        
        return {
            "correlation_1d": float(correlation_1d),
            "correlation_5d": float(correlation_5d),
            "ic_mean": float(ic_mean),
            "ic_std": float(ic_std),
            "ic_ir": float(ic_mean / ic_std) if ic_std > 0 else 0,
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "is_significant": p_value < 0.05,
            "quantile_returns": quantile_returns
        }
    
    def _run_ml_analysis(self, feature: pd.Series, prices: pd.DataFrame) -> dict:
        """
        Use ML to detect non-linear patterns and feature interactions
        """
        # Create feature matrix with lagged values
        X = self._create_feature_matrix(feature, prices)
        y = (prices['close'].pct_change(1).shift(-1) > 0).astype(int)
        
        # Align and clean data
        mask = ~(X.isna().any(axis=1) | y.isna())
        X_clean = X[mask]
        y_clean = y[mask]
        
        # Train Random Forest with cross-validation
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        
        cv_scores = []
        for train_idx, test_idx in self.tscv.split(X_clean):
            model.fit(X_clean.iloc[train_idx], y_clean.iloc[train_idx])
            score = model.score(X_clean.iloc[test_idx], y_clean.iloc[test_idx])
            cv_scores.append(score)
        
        # Feature importance
        model.fit(X_clean, y_clean)
        importance = dict(zip(X_clean.columns, model.feature_importances_))
        
        # SHAP values for explainability
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_clean.iloc[-100:])
        
        return {
            "cv_accuracy": float(np.mean(cv_scores)),
            "cv_std": float(np.std(cv_scores)),
            "feature_importance": importance,
            "has_predictive_power": np.mean(cv_scores) > 0.52,
            "shap_summary": self._summarize_shap(shap_values, X_clean.columns)
        }
    
    def _bootstrap_analysis(
        self,
        feature: pd.Series,
        prices: pd.DataFrame,
        n_iterations: int = 10000
    ) -> dict:
        """
        Bootstrap confidence intervals for expectancy
        """
        returns = prices['close'].pct_change(1).shift(-1)
        
        # Signal-based returns
        signal_mask = feature > feature.median()
        signal_returns = returns[signal_mask].dropna().values
        
        # Bootstrap
        bootstrap_means = []
        for _ in range(n_iterations):
            sample = np.random.choice(signal_returns, size=len(signal_returns), replace=True)
            bootstrap_means.append(np.mean(sample))
        
        bootstrap_means = np.array(bootstrap_means)
        
        return {
            "mean_return": float(np.mean(bootstrap_means)),
            "ci_lower_95": float(np.percentile(bootstrap_means, 2.5)),
            "ci_upper_95": float(np.percentile(bootstrap_means, 97.5)),
            "ci_lower_99": float(np.percentile(bootstrap_means, 0.5)),
            "ci_upper_99": float(np.percentile(bootstrap_means, 99.5)),
            "probability_positive": float(np.mean(bootstrap_means > 0))
        }
    
    def _calculate_ic(self, feature: pd.Series, returns: pd.Series) -> tuple:
        """Calculate Information Coefficient (Alphalens style)"""
        # Daily IC
        daily_ic = feature.rolling(20).corr(returns)
        return daily_ic.mean(), daily_ic.std()
    
    def _quantile_analysis(self, feature: pd.Series, returns: pd.Series, n_quantiles: int = 5) -> dict:
        """Alphalens-style quantile analysis"""
        quantiles = pd.qcut(feature, n_quantiles, labels=False, duplicates='drop')
        
        result = {}
        for q in range(n_quantiles):
            q_returns = returns[quantiles == q].dropna()
            result[f"Q{q+1}"] = {
                "mean_return": float(q_returns.mean()),
                "sharpe": float(q_returns.mean() / q_returns.std() * np.sqrt(252)) if q_returns.std() > 0 else 0,
                "count": len(q_returns)
            }
        
        # Long-short spread (Q5 - Q1)
        q5_returns = returns[quantiles == n_quantiles - 1].dropna()
        q1_returns = returns[quantiles == 0].dropna()
        result["long_short_spread"] = float(q5_returns.mean() - q1_returns.mean())
        
        return result
```

#### Frontend Implementation (React)

```typescript
// components/ideation/EdgeDiscoveryPanel.tsx
"use client";

import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2, TrendingUp, BarChart3, Zap } from "lucide-react";
import { ConfidenceIntervalChart } from "@/components/charts/ConfidenceIntervalChart";
import { QuantileReturnsChart } from "@/components/charts/QuantileReturnsChart";

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

export function EdgeDiscoveryPanel() {
  const [featureDescription, setFeatureDescription] = useState("");
  const [symbol, setSymbol] = useState("SPY");
  
  const analyzeFeature = useMutation({
    mutationFn: async (data: { description: string; symbol: string }) => {
      const response = await fetch("/api/ideation/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      return response.json() as Promise<EdgeResult>;
    },
  });
  
  const handleAnalyze = () => {
    analyzeFeature.mutate({
      description: featureDescription,
      symbol,
    });
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
              disabled={analyzeFeature.isPending}
              className="bg-accent-gradient"
            >
              {analyzeFeature.isPending ? (
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
      {analyzeFeature.data && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Statistical Significance Card */}
          <Card className="bg-background-card border-border-primary">
            <CardHeader>
              <CardTitle className="text-lg">Statistical Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <StatItem
                  label="Information Coefficient"
                  value={analyzeFeature.data.statistical_significance.ic_mean.toFixed(4)}
                  isPositive={analyzeFeature.data.statistical_significance.ic_mean > 0}
                />
                <StatItem
                  label="IC IR"
                  value={analyzeFeature.data.statistical_significance.ic_ir.toFixed(2)}
                  isPositive={analyzeFeature.data.statistical_significance.ic_ir > 0.5}
                />
                <StatItem
                  label="P-Value"
                  value={analyzeFeature.data.statistical_significance.p_value.toFixed(4)}
                  isPositive={analyzeFeature.data.statistical_significance.p_value < 0.05}
                />
                <StatItem
                  label="Statistically Significant"
                  value={analyzeFeature.data.statistical_significance.is_significant ? "Yes" : "No"}
                  isPositive={analyzeFeature.data.statistical_significance.is_significant}
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
                  <span className={`font-mono ${
                    analyzeFeature.data.ml_importance.cv_accuracy > 0.52 
                      ? "text-success" 
                      : "text-text-primary"
                  }`}>
                    {(analyzeFeature.data.ml_importance.cv_accuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-text-secondary">Predictive Power</span>
                  <span className={
                    analyzeFeature.data.ml_importance.has_predictive_power 
                      ? "text-success" 
                      : "text-error"
                  }>
                    {analyzeFeature.data.ml_importance.has_predictive_power ? "Detected" : "Weak"}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Confidence Intervals Chart */}
          <Card className="bg-background-card border-border-primary lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Bootstrap Confidence Intervals</CardTitle>
            </CardHeader>
            <CardContent>
              <ConfidenceIntervalChart data={analyzeFeature.data.confidence_intervals} />
            </CardContent>
          </Card>
          
          {/* Quantile Returns Chart */}
          <Card className="bg-background-card border-border-primary lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg">Quantile Returns Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <QuantileReturnsChart 
                data={analyzeFeature.data.statistical_significance.quantile_returns} 
              />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

function StatItem({ 
  label, 
  value, 
  isPositive 
}: { 
  label: string; 
  value: string; 
  isPositive: boolean;
}) {
  return (
    <div className="p-3 bg-background-tertiary rounded-lg">
      <div className="text-xs text-text-muted mb-1">{label}</div>
      <div className={`font-mono font-semibold ${isPositive ? "text-success" : "text-text-primary"}`}>
        {value}
      </div>
    </div>
  );
}
```

---

### 4.2 FEATURE: Pine Script Code Generator

**QuantPad Description:** "Describe your strategy in natural language. QuantPad converts it into TradingView Pine, ready to test and iterate."

#### Pine Script RAG System

```python
# api/app/services/pine_generator.py
import os
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

class PineScriptGenerator:
    """
    RAG-based Pine Script generator with TradingView documentation
    """
    
    SYSTEM_PROMPT = """You are an expert Pine Script v5 developer. You generate clean, 
    production-ready TradingView Pine Script code based on user descriptions.
    
    Rules:
    1. Always use Pine Script v5 syntax (//@version=5)
    2. Include proper indicator() or strategy() declaration
    3. Add helpful comments explaining the logic
    4. Use meaningful variable names
    5. Handle edge cases (na values, array bounds)
    6. Follow TradingView best practices
    7. Generate complete, compilable code
    
    When generating strategies:
    - Include proper entry/exit logic
    - Add position sizing if relevant
    - Include stop-loss and take-profit when appropriate
    - Use strategy.entry() and strategy.exit() correctly
    """
    
    PINE_EXAMPLES = [
        {
            "description": "RSI crossover strategy with overbought/oversold levels",
            "code": '''
//@version=5
strategy("RSI Crossover Strategy", overlay=false)

// Inputs
rsiLength = input.int(14, "RSI Length", minval=1)
overbought = input.int(70, "Overbought Level")
oversold = input.int(30, "Oversold Level")

// Calculate RSI
rsiValue = ta.rsi(close, rsiLength)

// Entry conditions
longCondition = ta.crossover(rsiValue, oversold)
shortCondition = ta.crossunder(rsiValue, overbought)

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

// Plot
plot(rsiValue, "RSI", color.purple)
hline(overbought, "Overbought", color.red)
hline(oversold, "Oversold", color.green)
'''
        },
        {
            "description": "EMA crossover with ATR-based stop loss",
            "code": '''
//@version=5
strategy("EMA Cross with ATR Stop", overlay=true)

// Inputs
fastLength = input.int(9, "Fast EMA")
slowLength = input.int(21, "Slow EMA")
atrLength = input.int(14, "ATR Length")
atrMultiplier = input.float(2.0, "ATR Multiplier")

// Calculate indicators
fastEMA = ta.ema(close, fastLength)
slowEMA = ta.ema(close, slowLength)
atrValue = ta.atr(atrLength)

// Entry conditions
longCondition = ta.crossover(fastEMA, slowEMA)
shortCondition = ta.crossunder(fastEMA, slowEMA)

// Position management
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

// Plot
plot(fastEMA, "Fast EMA", color.blue)
plot(slowEMA, "Slow EMA", color.orange)
'''
        }
    ]
    
    def __init__(self):
        self.client = OpenAI()
        self.chroma = chromadb.Client()
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize ChromaDB with Pine Script documentation and examples"""
        self.collection = self.chroma.get_or_create_collection(
            name="pine_docs",
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )
        )
        
        # Add examples if collection is empty
        if self.collection.count() == 0:
            for i, example in enumerate(self.PINE_EXAMPLES):
                self.collection.add(
                    documents=[example["description"]],
                    metadatas=[{"code": example["code"]}],
                    ids=[f"example_{i}"]
                )
    
    async def generate_pine_script(
        self,
        description: str,
        script_type: str = "strategy"  # "strategy" or "indicator"
    ) -> Dict:
        """Generate Pine Script from natural language description"""
        
        # 1. Retrieve similar examples from vector store
        results = self.collection.query(
            query_texts=[description],
            n_results=3
        )
        
        # 2. Build context from retrieved examples
        context = "Here are some relevant Pine Script examples:\n\n"
        for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
            context += f"Description: {doc}\nCode:\n{metadata['code']}\n\n---\n\n"
        
        # 3. Generate with LLM
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"""
Context (similar examples):
{context}

User Request:
Generate a TradingView Pine Script {script_type} for the following:
{description}

Requirements:
- Use Pine Script v5
- Include all necessary inputs
- Add proper documentation comments
- Make it production-ready
"""}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        generated_code = response.choices[0].message.content
        
        # 4. Extract code block if wrapped in markdown
        if "```" in generated_code:
            import re
            code_match = re.search(r"```(?:pine|pinescript)?\n(.*?)```", generated_code, re.DOTALL)
            if code_match:
                generated_code = code_match.group(1)
        
        # 5. Validate syntax (basic check)
        validation = self._validate_pine_syntax(generated_code)
        
        return {
            "code": generated_code.strip(),
            "is_valid": validation["is_valid"],
            "errors": validation["errors"],
            "warnings": validation["warnings"]
        }
    
    def _validate_pine_syntax(self, code: str) -> Dict:
        """Basic Pine Script syntax validation"""
        errors = []
        warnings = []
        
        # Check version declaration
        if "//@version=5" not in code and "//@version=4" not in code:
            errors.append("Missing version declaration (//@version=5)")
        
        # Check for indicator or strategy declaration
        if "indicator(" not in code and "strategy(" not in code:
            errors.append("Missing indicator() or strategy() declaration")
        
        # Check for common issues
        if "var " in code and "=" not in code.split("var ")[1][:50]:
            warnings.append("'var' keyword may be incorrectly used")
        
        # Check matching parentheses
        if code.count("(") != code.count(")"):
            errors.append("Mismatched parentheses")
        
        if code.count("[") != code.count("]"):
            errors.append("Mismatched brackets")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    async def fix_compile_errors(self, code: str, error_message: str) -> Dict:
        """Iteratively fix Pine Script compile errors"""
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"""
The following Pine Script has a compile error. Fix it.

Original Code:
```pine
{code}
```

Error Message:
{error_message}

Provide the corrected code only, no explanations.
"""}
            ],
            temperature=0.1
        )
        
        fixed_code = response.choices[0].message.content
        
        # Extract code block
        if "```" in fixed_code:
            import re
            code_match = re.search(r"```(?:pine|pinescript)?\n(.*?)```", fixed_code, re.DOTALL)
            if code_match:
                fixed_code = code_match.group(1)
        
        return {
            "code": fixed_code.strip(),
            "changes_made": True
        }
```

#### Frontend Code Editor Component

```typescript
// components/editor/PineScriptEditor.tsx
"use client";

import { useRef, useState } from "react";
import Editor, { Monaco, OnMount } from "@monaco-editor/react";
import { editor } from "monaco-editor";
import { Button } from "@/components/ui/button";
import { Copy, Download, Play, Wand2, AlertCircle, CheckCircle } from "lucide-react";
import { toast } from "sonner";

// Pine Script syntax definition
const PINE_LANGUAGE_DEF = {
  keywords: [
    "if", "else", "for", "to", "while", "switch", "case", "default",
    "break", "continue", "return", "import", "export", "type", "enum",
    "var", "varip", "const", "input", "series", "simple",
    "true", "false", "na", "bar_index", "last_bar_index",
    "strategy", "indicator", "library"
  ],
  typeKeywords: [
    "int", "float", "bool", "string", "color", "line", "label", "box",
    "table", "array", "matrix", "map"
  ],
  builtins: [
    "ta", "math", "str", "color", "array", "matrix", "map", "chart",
    "request", "ticker", "syminfo", "timeframe", "session", "strategy"
  ],
  operators: [
    "=", ">", "<", "!", "~", "?", ":", "==", "<=", ">=", "!=",
    "and", "or", "not", "+", "-", "*", "/", "%", "+=", "-=", "*=", "/="
  ]
};

interface PineScriptEditorProps {
  value: string;
  onChange: (value: string) => void;
  onGenerate?: (description: string) => Promise<void>;
  isGenerating?: boolean;
  validationErrors?: string[];
}

export function PineScriptEditor({
  value,
  onChange,
  onGenerate,
  isGenerating,
  validationErrors = []
}: PineScriptEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const [description, setDescription] = useState("");
  
  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    
    // Register Pine Script language
    monaco.languages.register({ id: "pinescript" });
    
    // Set tokenizer
    monaco.languages.setMonarchTokensProvider("pinescript", {
      keywords: PINE_LANGUAGE_DEF.keywords,
      typeKeywords: PINE_LANGUAGE_DEF.typeKeywords,
      operators: PINE_LANGUAGE_DEF.operators,
      
      tokenizer: {
        root: [
          [/\/\/.*$/, "comment"],
          [/\/\*/, "comment", "@comment"],
          [/"([^"\\]|\\.)*$/, "string.invalid"],
          [/"/, "string", "@string"],
          [/'[^']*'/, "string"],
          [/\d+\.?\d*/, "number"],
          [/#[0-9a-fA-F]{6,8}/, "color"],
          [
            /[a-zA-Z_]\w*/,
            {
              cases: {
                "@keywords": "keyword",
                "@typeKeywords": "type",
                "@builtins": "builtin",
                "@default": "identifier"
              }
            }
          ],
          [/[{}()\[\]]/, "@brackets"],
          [/[<>](?!@operators)/, "@brackets"],
          [
            /@operators/,
            {
              cases: {
                "@operators": "operator",
                "@default": ""
              }
            }
          ]
        ],
        comment: [
          [/[^\/*]+/, "comment"],
          [/\*\//, "comment", "@pop"],
          [/[\/*]/, "comment"]
        ],
        string: [
          [/[^\\"]+/, "string"],
          [/\\./, "string.escape"],
          [/"/, "string", "@pop"]
        ]
      }
    });
    
    // Define dark theme for Pine Script
    monaco.editor.defineTheme("pine-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "comment", foreground: "6A9955" },
        { token: "keyword", foreground: "C586C0" },
        { token: "type", foreground: "4EC9B0" },
        { token: "builtin", foreground: "DCDCAA" },
        { token: "string", foreground: "CE9178" },
        { token: "number", foreground: "B5CEA8" },
        { token: "operator", foreground: "D4D4D4" },
        { token: "color", foreground: "9CDCFE" },
        { token: "identifier", foreground: "9CDCFE" }
      ],
      colors: {
        "editor.background": "#111118",
        "editor.foreground": "#D4D4D4",
        "editor.lineHighlightBackground": "#1e1e2a",
        "editorCursor.foreground": "#8b5cf6",
        "editor.selectionBackground": "#264f78",
        "editorLineNumber.foreground": "#5A5A5A"
      }
    });
    
    monaco.editor.setTheme("pine-dark");
  };
  
  const copyToClipboard = () => {
    navigator.clipboard.writeText(value);
    toast.success("Copied to clipboard!");
  };
  
  const downloadFile = () => {
    const blob = new Blob([value], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "strategy.pine";
    a.click();
    URL.revokeObjectURL(url);
  };
  
  return (
    <div className="flex flex-col h-full">
      {/* AI Generation Bar */}
      {onGenerate && (
        <div className="p-4 bg-background-tertiary border-b border-border-primary">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Describe your strategy in plain English..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="flex-1 bg-background-secondary border border-border-primary rounded-lg px-4 py-2 text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-primary"
            />
            <Button
              onClick={() => onGenerate(description)}
              disabled={isGenerating || !description.trim()}
              className="bg-accent-gradient"
            >
              <Wand2 className="h-4 w-4 mr-2" />
              {isGenerating ? "Generating..." : "Generate"}
            </Button>
          </div>
        </div>
      )}
      
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-background-secondary border-b border-border-primary">
        <div className="flex items-center gap-2">
          <span className="text-sm text-text-muted font-mono">Pine Script v5</span>
          {validationErrors.length === 0 ? (
            <span className="flex items-center gap-1 text-success text-sm">
              <CheckCircle className="h-3 w-3" /> Valid
            </span>
          ) : (
            <span className="flex items-center gap-1 text-error text-sm">
              <AlertCircle className="h-3 w-3" /> {validationErrors.length} errors
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={copyToClipboard}>
            <Copy className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={downloadFile}>
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>
      
      {/* Editor */}
      <div className="flex-1">
        <Editor
          height="100%"
          language="pinescript"
          value={value}
          onChange={(val) => onChange(val || "")}
          onMount={handleEditorDidMount}
          options={{
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            lineNumbers: "on",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: "on",
            padding: { top: 16, bottom: 16 }
          }}
        />
      </div>
      
      {/* Error Panel */}
      {validationErrors.length > 0 && (
        <div className="p-3 bg-error/10 border-t border-error/30">
          {validationErrors.map((error, i) => (
            <div key={i} className="flex items-center gap-2 text-sm text-error">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

### 4.3 FEATURE: Monte Carlo Testing

**QuantPad Description:** "Upload a backtest. QuantPad runs institutional-grade bootstrapping and Monte Carlo simulations to reveal whether your performance is real or just luck."

#### Backend Monte Carlo Service

```python
# api/app/services/monte_carlo_service.py
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Optional
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

@dataclass
class MonteCarloConfig:
    n_simulations: int = 10000
    confidence_levels: List[float] = (0.80, 0.90, 0.95, 0.99)
    methods: List[str] = ("shuffle_returns", "bootstrap", "random_entry")

class MonteCarloService:
    """
    Institutional-grade Monte Carlo simulation engine
    """
    
    def __init__(self, config: MonteCarloConfig = None):
        self.config = config or MonteCarloConfig()
        self.n_cores = max(1, multiprocessing.cpu_count() - 1)
    
    async def run_full_analysis(
        self,
        trades: pd.DataFrame,
        equity_curve: pd.Series
    ) -> Dict:
        """
        Run comprehensive Monte Carlo analysis on backtest results
        
        Args:
            trades: DataFrame with columns [entry_time, exit_time, pnl, return_pct]
            equity_curve: Series of cumulative equity values
        """
        results = {}
        
        # 1. Shuffle trades Monte Carlo
        results["shuffle_trades"] = self._shuffle_trades_mc(trades)
        
        # 2. Bootstrap resampling
        results["bootstrap"] = self._bootstrap_mc(trades)
        
        # 3. Random entry simulation
        results["random_entry"] = self._random_entry_mc(trades, equity_curve)
        
        # 4. Drawdown distribution
        results["drawdown_distribution"] = self._drawdown_distribution(trades)
        
        # 5. Risk of ruin calculation
        results["risk_of_ruin"] = self._calculate_risk_of_ruin(trades)
        
        # 6. Expectancy confidence intervals
        results["expectancy_ci"] = self._expectancy_confidence_intervals(trades)
        
        # 7. Summary statistics
        results["summary"] = self._generate_summary(results, trades)
        
        return results
    
    def _shuffle_trades_mc(self, trades: pd.DataFrame) -> Dict:
        """
        Monte Carlo by shuffling trade order
        Tests: "What if trades occurred in different order?"
        """
        returns = trades["return_pct"].values
        n_trades = len(returns)
        
        simulated_equity_curves = []
        simulated_max_drawdowns = []
        simulated_final_equity = []
        
        for _ in range(self.config.n_simulations):
            # Shuffle trade order
            shuffled = np.random.permutation(returns)
            
            # Calculate equity curve
            equity = np.cumprod(1 + shuffled)
            simulated_equity_curves.append(equity)
            
            # Calculate max drawdown
            running_max = np.maximum.accumulate(equity)
            drawdown = (running_max - equity) / running_max
            simulated_max_drawdowns.append(np.max(drawdown))
            
            simulated_final_equity.append(equity[-1])
        
        return {
            "equity_curves": self._sample_curves(simulated_equity_curves, 100),
            "max_drawdown_distribution": {
                "values": simulated_max_drawdowns,
                "percentiles": self._calculate_percentiles(simulated_max_drawdowns)
            },
            "final_equity_distribution": {
                "values": simulated_final_equity,
                "percentiles": self._calculate_percentiles(simulated_final_equity)
            }
        }
    
    def _bootstrap_mc(self, trades: pd.DataFrame) -> Dict:
        """
        Bootstrap resampling with replacement
        Tests: "How stable are our metrics?"
        """
        returns = trades["return_pct"].values
        n_trades = len(returns)
        
        bootstrap_sharpe = []
        bootstrap_profit_factor = []
        bootstrap_win_rate = []
        bootstrap_expectancy = []
        
        for _ in range(self.config.n_simulations):
            # Resample with replacement
            sample_idx = np.random.choice(n_trades, size=n_trades, replace=True)
            sample_returns = returns[sample_idx]
            
            # Calculate metrics
            if np.std(sample_returns) > 0:
                sharpe = np.mean(sample_returns) / np.std(sample_returns) * np.sqrt(252)
            else:
                sharpe = 0
            bootstrap_sharpe.append(sharpe)
            
            wins = sample_returns[sample_returns > 0]
            losses = sample_returns[sample_returns < 0]
            
            if len(losses) > 0 and np.sum(np.abs(losses)) > 0:
                pf = np.sum(wins) / np.sum(np.abs(losses))
            else:
                pf = np.inf if len(wins) > 0 else 0
            bootstrap_profit_factor.append(pf)
            
            win_rate = len(wins) / len(sample_returns) if len(sample_returns) > 0 else 0
            bootstrap_win_rate.append(win_rate)
            
            expectancy = np.mean(sample_returns)
            bootstrap_expectancy.append(expectancy)
        
        return {
            "sharpe_ratio": {
                "mean": float(np.mean(bootstrap_sharpe)),
                "std": float(np.std(bootstrap_sharpe)),
                "percentiles": self._calculate_percentiles(bootstrap_sharpe)
            },
            "profit_factor": {
                "mean": float(np.nanmean([x for x in bootstrap_profit_factor if x != np.inf])),
                "percentiles": self._calculate_percentiles(
                    [x for x in bootstrap_profit_factor if x != np.inf and x < 100]
                )
            },
            "win_rate": {
                "mean": float(np.mean(bootstrap_win_rate)),
                "std": float(np.std(bootstrap_win_rate)),
                "percentiles": self._calculate_percentiles(bootstrap_win_rate)
            },
            "expectancy": {
                "mean": float(np.mean(bootstrap_expectancy)),
                "std": float(np.std(bootstrap_expectancy)),
                "percentiles": self._calculate_percentiles(bootstrap_expectancy),
                "probability_positive": float(np.mean(np.array(bootstrap_expectancy) > 0))
            }
        }
    
    def _random_entry_mc(
        self,
        trades: pd.DataFrame,
        equity_curve: pd.Series
    ) -> Dict:
        """
        Compare strategy to random entry timing
        Tests: "Is timing actually adding value?"
        """
        # Get underlying returns
        underlying_returns = equity_curve.pct_change().dropna().values
        n_periods = len(underlying_returns)
        n_trades = len(trades)
        
        avg_trade_duration = 5  # Assume average trade is 5 periods
        
        random_strategy_returns = []
        
        for _ in range(self.config.n_simulations):
            # Generate random entry points
            entry_points = np.random.choice(
                n_periods - avg_trade_duration,
                size=n_trades,
                replace=True
            )
            
            # Calculate returns for random entries
            trade_returns = []
            for entry in entry_points:
                exit_point = min(entry + avg_trade_duration, n_periods - 1)
                period_returns = underlying_returns[entry:exit_point]
                trade_return = np.prod(1 + period_returns) - 1
                trade_returns.append(trade_return)
            
            random_strategy_returns.append(np.mean(trade_returns))
        
        # Original strategy expectancy
        original_expectancy = trades["return_pct"].mean()
        
        # Calculate p-value: probability that random does as well
        p_value = np.mean(np.array(random_strategy_returns) >= original_expectancy)
        
        return {
            "original_expectancy": float(original_expectancy),
            "random_expectancy_distribution": {
                "mean": float(np.mean(random_strategy_returns)),
                "std": float(np.std(random_strategy_returns)),
                "percentiles": self._calculate_percentiles(random_strategy_returns)
            },
            "p_value": float(p_value),
            "is_significant": p_value < 0.05,
            "edge_percentile": float(
                stats.percentileofscore(random_strategy_returns, original_expectancy)
            )
        }
    
    def _drawdown_distribution(self, trades: pd.DataFrame) -> Dict:
        """Calculate drawdown distribution across simulations"""
        returns = trades["return_pct"].values
        
        max_drawdowns = []
        avg_drawdowns = []
        drawdown_durations = []
        
        for _ in range(self.config.n_simulations):
            shuffled = np.random.permutation(returns)
            equity = np.cumprod(1 + shuffled)
            
            running_max = np.maximum.accumulate(equity)
            drawdown = (running_max - equity) / running_max
            
            max_drawdowns.append(np.max(drawdown))
            avg_drawdowns.append(np.mean(drawdown))
            
            # Calculate drawdown duration
            in_drawdown = drawdown > 0
            durations = []
            current_duration = 0
            for is_dd in in_drawdown:
                if is_dd:
                    current_duration += 1
                elif current_duration > 0:
                    durations.append(current_duration)
                    current_duration = 0
            if current_duration > 0:
                durations.append(current_duration)
            
            drawdown_durations.append(max(durations) if durations else 0)
        
        return {
            "max_drawdown": {
                "percentiles": self._calculate_percentiles(max_drawdowns),
                "histogram": np.histogram(max_drawdowns, bins=50)[0].tolist()
            },
            "avg_drawdown": {
                "mean": float(np.mean(avg_drawdowns)),
                "percentiles": self._calculate_percentiles(avg_drawdowns)
            },
            "max_drawdown_duration": {
                "mean": float(np.mean(drawdown_durations)),
                "percentiles": self._calculate_percentiles(drawdown_durations)
            }
        }
    
    def _calculate_risk_of_ruin(
        self,
        trades: pd.DataFrame,
        ruin_threshold: float = 0.5
    ) -> Dict:
        """
        Calculate probability of hitting a ruin threshold
        """
        returns = trades["return_pct"].values
        
        ruin_count = 0
        min_equity_distribution = []
        
        for _ in range(self.config.n_simulations):
            shuffled = np.random.permutation(returns)
            equity = np.cumprod(1 + shuffled)
            
            min_equity = np.min(equity)
            min_equity_distribution.append(min_equity)
            
            if min_equity < (1 - ruin_threshold):
                ruin_count += 1
        
        return {
            "ruin_probability": float(ruin_count / self.config.n_simulations),
            "min_equity_percentiles": self._calculate_percentiles(min_equity_distribution),
            "probability_below_50pct": float(
                np.mean(np.array(min_equity_distribution) < 0.5)
            ),
            "probability_below_25pct": float(
                np.mean(np.array(min_equity_distribution) < 0.25)
            )
        }
    
    def _expectancy_confidence_intervals(self, trades: pd.DataFrame) -> Dict:
        """Calculate confidence intervals for expectancy"""
        returns = trades["return_pct"].values
        
        bootstrap_means = []
        for _ in range(self.config.n_simulations):
            sample = np.random.choice(returns, size=len(returns), replace=True)
            bootstrap_means.append(np.mean(sample))
        
        return {
            "mean": float(np.mean(returns)),
            "confidence_intervals": {
                "80": [
                    float(np.percentile(bootstrap_means, 10)),
                    float(np.percentile(bootstrap_means, 90))
                ],
                "90": [
                    float(np.percentile(bootstrap_means, 5)),
                    float(np.percentile(bootstrap_means, 95))
                ],
                "95": [
                    float(np.percentile(bootstrap_means, 2.5)),
                    float(np.percentile(bootstrap_means, 97.5))
                ],
                "99": [
                    float(np.percentile(bootstrap_means, 0.5)),
                    float(np.percentile(bootstrap_means, 99.5))
                ]
            },
            "probability_positive": float(np.mean(np.array(bootstrap_means) > 0))
        }
    
    def _calculate_percentiles(self, values: List[float]) -> Dict:
        """Calculate standard percentiles"""
        arr = np.array([x for x in values if not np.isnan(x) and not np.isinf(x)])
        return {
            "p5": float(np.percentile(arr, 5)),
            "p10": float(np.percentile(arr, 10)),
            "p25": float(np.percentile(arr, 25)),
            "p50": float(np.percentile(arr, 50)),
            "p75": float(np.percentile(arr, 75)),
            "p90": float(np.percentile(arr, 90)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99))
        }
    
    def _sample_curves(self, curves: List[np.ndarray], n_samples: int) -> List:
        """Sample curves for visualization"""
        indices = np.random.choice(len(curves), min(n_samples, len(curves)), replace=False)
        return [curves[i].tolist() for i in indices]
    
    def _generate_summary(self, results: Dict, trades: pd.DataFrame) -> Dict:
        """Generate summary verdict"""
        bootstrap = results["bootstrap"]
        random_entry = results["random_entry"]
        risk = results["risk_of_ruin"]
        
        # Determine edge quality
        edge_score = 0
        
        if bootstrap["expectancy"]["probability_positive"] > 0.95:
            edge_score += 3
        elif bootstrap["expectancy"]["probability_positive"] > 0.80:
            edge_score += 2
        elif bootstrap["expectancy"]["probability_positive"] > 0.65:
            edge_score += 1
        
        if random_entry["is_significant"]:
            edge_score += 2
        
        if risk["ruin_probability"] < 0.05:
            edge_score += 2
        elif risk["ruin_probability"] < 0.10:
            edge_score += 1
        
        # Generate verdict
        if edge_score >= 6:
            verdict = "STRONG EDGE"
            verdict_color = "green"
            description = "Strategy shows statistically significant edge with low risk of ruin."
        elif edge_score >= 4:
            verdict = "MODERATE EDGE"
            verdict_color = "yellow"
            description = "Strategy shows promise but needs further validation."
        elif edge_score >= 2:
            verdict = "WEAK EDGE"
            verdict_color = "orange"
            description = "Limited evidence of edge. Consider refinement."
        else:
            verdict = "NO EDGE DETECTED"
            verdict_color = "red"
            description = "Strategy does not show statistical edge over random."
        
        return {
            "verdict": verdict,
            "verdict_color": verdict_color,
            "description": description,
            "edge_score": edge_score,
            "key_metrics": {
                "expectancy_95_ci": bootstrap["expectancy"]["percentiles"],
                "probability_positive_expectancy": bootstrap["expectancy"]["probability_positive"],
                "timing_p_value": random_entry["p_value"],
                "risk_of_ruin": risk["ruin_probability"],
                "sharpe_95_ci": [
                    bootstrap["sharpe_ratio"]["percentiles"]["p5"],
                    bootstrap["sharpe_ratio"]["percentiles"]["p95"]
                ]
            }
        }
```

#### Frontend Monte Carlo Visualization

```typescript
// components/charts/MonteCarloChart.tsx
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
```

---

### 4.4 FEATURE: Prop Firm Challenge Simulator

**QuantPad Description:** "Use the Prop Firm Assistant to simulate your odds of passing major prop firm challenges. We model your strategy's edge under real rules, fees, resets, and payout structures."

#### Backend Prop Firm Simulator

```python
# api/app/services/prop_firm_simulator.py
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class PropFirmType(Enum):
    FTMO = "ftmo"
    THE5ERS = "the5ers"
    APEX = "apex"
    TOPSTEP = "topstep"
    MFF = "mff"
    E8 = "e8"

@dataclass
class PropFirmRules:
    name: str
    account_size: float
    challenge_cost: float
    profit_target_phase1: float  # As decimal (0.08 = 8%)
    profit_target_phase2: float
    max_daily_drawdown: float
    max_total_drawdown: float
    min_trading_days: int
    max_trading_days: Optional[int]
    profit_split: float
    trailing_drawdown: bool = False
    consistency_rule: Optional[float] = None  # Max % from single day

# Pre-configured prop firm rules
PROP_FIRM_CONFIGS = {
    PropFirmType.FTMO: PropFirmRules(
        name="FTMO",
        account_size=100000,
        challenge_cost=540,
        profit_target_phase1=0.10,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.10,
        min_trading_days=4,
        max_trading_days=None,
        profit_split=0.80
    ),
    PropFirmType.THE5ERS: PropFirmRules(
        name="The5%ers",
        account_size=100000,
        challenge_cost=235,
        profit_target_phase1=0.08,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.10,
        min_trading_days=3,
        max_trading_days=None,
        profit_split=0.80
    ),
    PropFirmType.APEX: PropFirmRules(
        name="Apex Trader Funding",
        account_size=100000,
        challenge_cost=167,
        profit_target_phase1=0.06,
        profit_target_phase2=0.0,  # No phase 2
        max_daily_drawdown=0.0,  # No daily limit
        max_total_drawdown=0.03,  # Trailing
        min_trading_days=7,
        max_trading_days=None,
        profit_split=0.90,
        trailing_drawdown=True
    ),
    PropFirmType.E8: PropFirmRules(
        name="E8 Markets",
        account_size=100000,
        challenge_cost=228,
        profit_target_phase1=0.08,
        profit_target_phase2=0.05,
        max_daily_drawdown=0.05,
        max_total_drawdown=0.08,
        min_trading_days=0,
        max_trading_days=None,
        profit_split=0.80
    )
}

class PropFirmSimulator:
    """
    Simulate prop firm challenge pass rates using Monte Carlo
    """
    
    def __init__(self, n_simulations: int = 10000):
        self.n_simulations = n_simulations
    
    async def simulate_challenge(
        self,
        daily_returns: np.ndarray,
        prop_firm: PropFirmType,
        custom_rules: Optional[PropFirmRules] = None
    ) -> Dict:
        """
        Run Monte Carlo simulation of prop firm challenge
        """
        rules = custom_rules or PROP_FIRM_CONFIGS[prop_firm]
        
        results = {
            "prop_firm": rules.name,
            "account_size": rules.account_size,
            "challenge_cost": rules.challenge_cost,
            "phase1": self._simulate_phase(
                daily_returns,
                rules.profit_target_phase1,
                rules.max_daily_drawdown,
                rules.max_total_drawdown,
                rules.min_trading_days,
                rules.trailing_drawdown,
                rules.consistency_rule
            ),
            "phase2": None,
            "funded_simulation": None
        }
        
        # Phase 2 simulation (if applicable)
        if rules.profit_target_phase2 > 0:
            results["phase2"] = self._simulate_phase(
                daily_returns,
                rules.profit_target_phase2,
                rules.max_daily_drawdown,
                rules.max_total_drawdown,
                rules.min_trading_days,
                rules.trailing_drawdown,
                rules.consistency_rule
            )
        
        # Combined pass rate
        phase1_pass = results["phase1"]["pass_rate"]
        phase2_pass = results["phase2"]["pass_rate"] if results["phase2"] else 1.0
        combined_pass_rate = phase1_pass * phase2_pass
        
        results["combined_pass_rate"] = combined_pass_rate
        
        # Funded account simulation (12 months)
        results["funded_simulation"] = self._simulate_funded_account(
            daily_returns,
            rules
        )
        
        # Expected value calculation
        results["expected_value"] = self._calculate_expected_value(
            results,
            rules
        )
        
        return results
    
    def _simulate_phase(
        self,
        daily_returns: np.ndarray,
        profit_target: float,
        max_daily_dd: float,
        max_total_dd: float,
        min_days: int,
        trailing_dd: bool,
        consistency_rule: Optional[float]
    ) -> Dict:
        """Simulate a single challenge phase"""
        
        n_days = len(daily_returns)
        passed = 0
        failed_daily_dd = 0
        failed_total_dd = 0
        failed_consistency = 0
        days_to_pass = []
        
        for sim in range(self.n_simulations):
            # Shuffle daily returns
            shuffled_returns = np.random.permutation(daily_returns)
            
            equity = 1.0
            peak_equity = 1.0
            trailing_floor = 1.0 - max_total_dd
            daily_pnl_history = []
            day = 0
            phase_passed = False
            fail_reason = None
            
            for daily_return in shuffled_returns:
                day += 1
                daily_pnl = equity * daily_return
                daily_pnl_history.append(daily_pnl)
                
                # Check daily drawdown
                if max_daily_dd > 0 and daily_return < -max_daily_dd:
                    fail_reason = "daily_dd"
                    break
                
                # Update equity
                equity *= (1 + daily_return)
                
                # Check trailing drawdown
                if trailing_dd:
                    if equity > peak_equity:
                        peak_equity = equity
                        trailing_floor = equity - max_total_dd
                    if equity < trailing_floor:
                        fail_reason = "total_dd"
                        break
                else:
                    # Fixed drawdown from starting equity
                    if equity < (1 - max_total_dd):
                        fail_reason = "total_dd"
                        break
                
                # Check consistency rule
                if consistency_rule and len(daily_pnl_history) > 0:
                    total_profit = sum(daily_pnl_history)
                    if total_profit > 0:
                        max_day_pnl = max(daily_pnl_history)
                        if max_day_pnl / total_profit > consistency_rule:
                            fail_reason = "consistency"
                            break
                
                # Check if passed
                if day >= min_days and equity >= (1 + profit_target):
                    phase_passed = True
                    break
            
            if phase_passed:
                passed += 1
                days_to_pass.append(day)
            elif fail_reason == "daily_dd":
                failed_daily_dd += 1
            elif fail_reason == "total_dd":
                failed_total_dd += 1
            elif fail_reason == "consistency":
                failed_consistency += 1
        
        pass_rate = passed / self.n_simulations
        
        return {
            "pass_rate": pass_rate,
            "fail_rate": 1 - pass_rate,
            "fail_reasons": {
                "daily_drawdown": failed_daily_dd / self.n_simulations,
                "total_drawdown": failed_total_dd / self.n_simulations,
                "consistency": failed_consistency / self.n_simulations,
                "time_expired": (self.n_simulations - passed - failed_daily_dd - 
                               failed_total_dd - failed_consistency) / self.n_simulations
            },
            "avg_days_to_pass": float(np.mean(days_to_pass)) if days_to_pass else None,
            "days_to_pass_distribution": {
                "p25": float(np.percentile(days_to_pass, 25)) if days_to_pass else None,
                "p50": float(np.percentile(days_to_pass, 50)) if days_to_pass else None,
                "p75": float(np.percentile(days_to_pass, 75)) if days_to_pass else None
            }
        }
    
    def _simulate_funded_account(
        self,
        daily_returns: np.ndarray,
        rules: PropFirmRules,
        months: int = 12
    ) -> Dict:
        """Simulate performance once funded"""
        
        trading_days_per_month = 21
        total_days = months * trading_days_per_month
        
        monthly_profits = []
        violation_count = 0
        
        for sim in range(self.n_simulations):
            # Extend returns if needed
            extended_returns = np.tile(
                daily_returns,
                (total_days // len(daily_returns)) + 1
            )[:total_days]
            np.random.shuffle(extended_returns)
            
            equity = 1.0
            monthly_pnl = []
            violated = False
            
            for month in range(months):
                if violated:
                    break
                    
                month_start_equity = equity
                
                for day in range(trading_days_per_month):
                    idx = month * trading_days_per_month + day
                    if idx >= len(extended_returns):
                        break
                    
                    daily_return = extended_returns[idx]
                    
                    # Check daily drawdown
                    if rules.max_daily_drawdown > 0:
                        if daily_return < -rules.max_daily_drawdown:
                            violated = True
                            break
                    
                    equity *= (1 + daily_return)
                    
                    # Check total drawdown
                    if equity < (1 - rules.max_total_drawdown):
                        violated = True
                        break
                
                if not violated:
                    month_pnl = equity - month_start_equity
                    monthly_pnl.append(month_pnl * rules.account_size * rules.profit_split)
            
            if violated:
                violation_count += 1
                monthly_profits.append(sum(monthly_pnl) if monthly_pnl else 0)
            else:
                monthly_profits.append(sum(monthly_pnl))
        
        return {
            "violation_rate": violation_count / self.n_simulations,
            "survival_rate": 1 - (violation_count / self.n_simulations),
            "expected_monthly_profit": float(np.mean([
                p / months for p in monthly_profits if p > 0
            ])) if any(p > 0 for p in monthly_profits) else 0,
            "total_profit_distribution": {
                "mean": float(np.mean(monthly_profits)),
                "p10": float(np.percentile(monthly_profits, 10)),
                "p25": float(np.percentile(monthly_profits, 25)),
                "p50": float(np.percentile(monthly_profits, 50)),
                "p75": float(np.percentile(monthly_profits, 75)),
                "p90": float(np.percentile(monthly_profits, 90))
            }
        }
    
    def _calculate_expected_value(
        self,
        results: Dict,
        rules: PropFirmRules
    ) -> Dict:
        """Calculate expected value of taking the challenge"""
        
        pass_rate = results["combined_pass_rate"]
        funded_sim = results["funded_simulation"]
        
        # Cost of challenge
        challenge_cost = rules.challenge_cost
        
        # Expected profit if funded (12 months)
        expected_funded_profit = funded_sim["total_profit_distribution"]["mean"]
        
        # Expected value
        ev = (pass_rate * expected_funded_profit) - challenge_cost
        
        # Break-even pass rate
        if expected_funded_profit > 0:
            break_even_pass_rate = challenge_cost / expected_funded_profit
        else:
            break_even_pass_rate = 1.0
        
        # ROI
        if challenge_cost > 0:
            roi = ev / challenge_cost
        else:
            roi = 0
        
        return {
            "expected_value": float(ev),
            "roi": float(roi),
            "break_even_pass_rate": float(break_even_pass_rate),
            "current_pass_rate": float(pass_rate),
            "edge_over_break_even": float(pass_rate - break_even_pass_rate),
            "recommendation": self._generate_recommendation(
                pass_rate, break_even_pass_rate, roi
            )
        }
    
    def _generate_recommendation(
        self,
        pass_rate: float,
        break_even: float,
        roi: float
    ) -> Dict:
        """Generate recommendation based on analysis"""
        
        if roi > 2:
            verdict = "HIGHLY RECOMMENDED"
            color = "green"
            description = "Strong positive expected value. Strategy is well-suited for this challenge."
        elif roi > 0.5:
            verdict = "RECOMMENDED"
            color = "green"
            description = "Positive expected value. Worth attempting with proper risk management."
        elif roi > 0:
            verdict = "MARGINAL"
            color = "yellow"
            description = "Slightly positive EV but tight margins. Consider optimizing strategy first."
        elif pass_rate > break_even * 0.8:
            verdict = "NOT RECOMMENDED"
            color = "orange"
            description = "Negative expected value but close to break-even. Minor improvements could help."
        else:
            verdict = "AVOID"
            color = "red"
            description = "Significantly negative expected value. Strategy needs major improvements."
        
        return {
            "verdict": verdict,
            "color": color,
            "description": description
        }
```

---

## PART 5: LANDING PAGE RECREATION

### 5.1 Floating Formulas Animation

```typescript
// components/landing/FloatingFormulas.tsx
"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const FORMULAS = [
  "S = (Rp - Rf) / σp",         // Sharpe Ratio
  "σ = √(Σ(xi - μ)² / N)",      // Standard Deviation
  "E[X] = Σ xi · P(xi)",        // Expected Value
  "f* = (bp - q) / b",          // Kelly Criterion
  "MDD = (Peak - Trough) / Peak", // Max Drawdown
  "Sortino = (R - T) / DR",     // Sortino Ratio
  "β = Cov(ri, rm) / Var(rm)",  // Beta
  "α = Ri - [Rf + β(Rm - Rf)]", // Alpha
  "VaR = μ - zσ",               // Value at Risk
  "PF = ΣWins / Σ|Losses|",     // Profit Factor
  "CAGR = (Vf/Vi)^(1/t) - 1",   // CAGR
  "R² = 1 - (SSres/SStot)",     // R-Squared
  "ρ = Cov(X,Y) / σxσy",        // Correlation
  "IR = (Rp - Rb) / σ(Rp - Rb)", // Information Ratio
];

export function FloatingFormulas() {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) return null;
  
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {FORMULAS.map((formula, i) => (
        <motion.div
          key={i}
          className="absolute font-mono text-sm text-text-muted/30 whitespace-nowrap"
          initial={{
            x: Math.random() * 100 + "%",
            y: Math.random() * 100 + "%",
            opacity: 0,
          }}
          animate={{
            x: [
              `${Math.random() * 100}%`,
              `${Math.random() * 100}%`,
              `${Math.random() * 100}%`,
            ],
            y: [
              `${Math.random() * 100}%`,
              `${Math.random() * 100}%`,
              `${Math.random() * 100}%`,
            ],
            opacity: [0.1, 0.3, 0.1],
            rotate: [0, Math.random() * 10 - 5, 0],
          }}
          transition={{
            duration: 20 + Math.random() * 20,
            repeat: Infinity,
            delay: i * 0.5,
            ease: "linear",
          }}
        >
          {formula}
        </motion.div>
      ))}
    </div>
  );
}
```

### 5.2 Hero Section

```typescript
// components/landing/Hero.tsx
"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { FloatingFormulas } from "./FloatingFormulas";
import Link from "next/link";

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-background-primary">
      {/* Floating formulas background */}
      <FloatingFormulas />
      
      {/* Gradient overlays */}
      <div className="absolute inset-0 bg-gradient-radial from-accent-primary/5 via-transparent to-transparent" />
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background-primary to-transparent" />
      
      {/* Content */}
      <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
        <motion.h1
          className="text-5xl md:text-7xl font-bold text-text-primary mb-6 tracking-tight"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Your AI{" "}
          <span className="bg-clip-text text-transparent bg-accent-gradient">
            Quant Dev
          </span>
        </motion.h1>
        
        <motion.p
          className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Turn trading ideas into code, stats, and deployed systems in one seamless workflow.
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <Link href="/sign-in">
            <Button size="lg" className="bg-accent-gradient text-lg px-8 py-6">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
```

### 5.3 Workflow Steps Section

```typescript
// components/landing/WorkflowSteps.tsx
"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import {
  Lightbulb,
  Code2,
  FlaskConical,
  Settings2,
  Rocket,
} from "lucide-react";

const STEPS = [
  {
    number: 1,
    title: "Discover",
    subtitle: "Measure the Edge in Any Idea",
    description:
      "Describe any feature in plain English, and instantly test whether it predicts market movement. We analyze each signal with advanced statistics/ML.",
    icon: Lightbulb,
    color: "text-yellow-400",
    bgColor: "bg-yellow-400/10",
  },
  {
    number: 2,
    title: "Build",
    subtitle: "Strategies & Indicators",
    description:
      "Describe your strategy in natural language. We convert it into TradingView Pine Script, ready to test and iterate.",
    icon: Code2,
    color: "text-blue-400",
    bgColor: "bg-blue-400/10",
  },
  {
    number: 3,
    title: "Test",
    subtitle: "Validate With Institutional Math",
    description:
      "Upload a backtest. We run institutional-grade bootstrapping and Monte Carlo simulations to reveal whether your performance is real or just luck.",
    icon: FlaskConical,
    color: "text-green-400",
    bgColor: "bg-green-400/10",
  },
  {
    number: 4,
    title: "Optimize",
    subtitle: "See What Truly Drives Performance",
    description:
      "We automatically compute features, run regression analysis, and uncover the hidden factors affecting your PnL, drawdown, and other KPIs.",
    icon: Settings2,
    color: "text-orange-400",
    bgColor: "bg-orange-400/10",
  },
  {
    number: 5,
    title: "Deploy",
    subtitle: "Launch or Simulate Prop Firm Performance",
    description:
      "Deploy live — or use the Prop Firm Assistant to simulate your odds of passing major prop firm challenges.",
    icon: Rocket,
    color: "text-purple-400",
    bgColor: "bg-purple-400/10",
  },
];

export function WorkflowSteps() {
  return (
    <section className="py-24 bg-background-secondary">
      <div className="container mx-auto px-4">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-text-primary mb-4">
            The OpenQuant Workflow
          </h2>
          <p className="text-text-secondary text-lg">
            From idea to deployed strategy in clear, ordered steps.
          </p>
        </motion.div>
        
        <div className="space-y-8">
          {STEPS.map((step, index) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="bg-background-card border-border-primary hover:border-accent-primary/50 transition-all duration-300">
                <CardContent className="p-8">
                  <div className="flex items-start gap-6">
                    {/* Step Number */}
                    <div className={`flex-shrink-0 w-12 h-12 rounded-full ${step.bgColor} flex items-center justify-center`}>
                      <span className={`text-xl font-bold ${step.color}`}>
                        {step.number}
                      </span>
                    </div>
                    
                    {/* Content */}
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-2xl font-semibold text-text-primary">
                          {step.title}
                        </h3>
                        <step.icon className={`h-6 w-6 ${step.color}`} />
                      </div>
                      <h4 className="text-lg text-accent-primary mb-3">
                        {step.subtitle}
                      </h4>
                      <p className="text-text-secondary leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## PART 6: DATABASE SCHEMA

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  // Relations
  strategies    Strategy[]
  backtests     Backtest[]
  ideations     Ideation[]
  subscriptions Subscription[]
}

model Strategy {
  id          String   @id @default(cuid())
  userId      String
  name        String
  description String?
  pineCode    String   @db.Text
  type        StrategyType @default(STRATEGY)
  isPublic    Boolean  @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  backtests   Backtest[]
  
  @@index([userId])
}

enum StrategyType {
  STRATEGY
  INDICATOR
}

model Backtest {
  id              String   @id @default(cuid())
  userId          String
  strategyId      String?
  name            String
  symbol          String
  timeframe       String
  startDate       DateTime
  endDate         DateTime
  initialCapital  Float
  
  // Results
  totalReturn     Float
  sharpeRatio     Float?
  maxDrawdown     Float
  winRate         Float
  profitFactor    Float?
  totalTrades     Int
  
  // Raw data
  tradesJson      Json     // Array of trade objects
  equityCurveJson Json     // Array of equity points
  
  // Monte Carlo results
  monteCarloJson  Json?
  
  createdAt       DateTime @default(now())
  
  user            User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  strategy        Strategy? @relation(fields: [strategyId], references: [id])
  
  @@index([userId])
  @@index([strategyId])
}

model Ideation {
  id                String   @id @default(cuid())
  userId            String
  featureDescription String  @db.Text
  symbol            String
  timeframe         String
  
  // Results
  icMean            Float?
  icIr              Float?
  pValue            Float?
  isSignificant     Boolean?
  mlAccuracy        Float?
  hasPredictivePower Boolean?
  
  // Full results
  resultsJson       Json?
  
  createdAt         DateTime @default(now())
  
  user              User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@index([userId])
}

model Subscription {
  id                     String   @id @default(cuid())
  userId                 String
  stripeCustomerId       String?  @unique
  stripeSubscriptionId   String?  @unique
  stripePriceId          String?
  stripeCurrentPeriodEnd DateTime?
  status                 SubscriptionStatus @default(INACTIVE)
  
  user                   User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@index([userId])
}

enum SubscriptionStatus {
  ACTIVE
  INACTIVE
  PAST_DUE
  CANCELED
}

model StrategyLibrary {
  id          String   @id @default(cuid())
  name        String
  description String   @db.Text
  category    String
  pineCode    String   @db.Text
  author      String?
  votes       Int      @default(0)
  isInfluencer Boolean @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
```

---

## PART 7: API ROUTES

```typescript
// app/api/ideation/analyze/route.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";

export async function POST(req: NextRequest) {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  
  const body = await req.json();
  const { description, symbol, timeframe = "1D" } = body;
  
  // Call Python backend
  const response = await fetch(`${process.env.PYTHON_API_URL}/ideation/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description, symbol, timeframe }),
  });
  
  const result = await response.json();
  
  // Save to database
  await prisma.ideation.create({
    data: {
      userId: session.user.id,
      featureDescription: description,
      symbol,
      timeframe,
      icMean: result.statistical_significance?.ic_mean,
      icIr: result.statistical_significance?.ic_ir,
      pValue: result.statistical_significance?.p_value,
      isSignificant: result.statistical_significance?.is_significant,
      mlAccuracy: result.ml_importance?.cv_accuracy,
      hasPredictivePower: result.ml_importance?.has_predictive_power,
      resultsJson: result,
    },
  });
  
  return NextResponse.json(result);
}
```

---

## PART 8: DEPLOYMENT

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  web:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/openquant
      - PYTHON_API_URL=http://api:8000
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - api
      - redis

  api:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/openquant
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=openquant
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## PART 9: GITHUB REPOS TO INTEGRATE

### Core Dependencies

| Feature | Repository | Stars | Purpose |
|---------|------------|-------|---------|
| Backtesting | `kernc/backtesting.py` | 5k+ | Python backtester |
| Factor Analysis | `stefan-jansen/alphalens-reloaded` | 1k+ | Alpha factor analysis |
| Portfolio Analysis | `stefan-jansen/pyfolio-reloaded` | 1k+ | Risk/performance metrics |
| Vectorized Backtest | `polakowo/vectorbt` | 4k+ | Fast vectorized backtesting |
| ML Trading | `stefan-jansen/machine-learning-for-trading` | 12k+ | ML notebooks |
| Charts | `tradingview/lightweight-charts` | 8k+ | Financial charts |
| Pine Scripts | `Alorse/pinescript-strategies` | 500+ | Strategy templates |
| UI Components | `shadcn/ui` | 70k+ | React components |

### Installation Commands

```bash
# Frontend
npx create-next-app@latest openquant --typescript --tailwind --app
cd openquant
npx shadcn@latest init
npm install @monaco-editor/react lightweight-charts recharts d3 framer-motion zustand @tanstack/react-query

# Backend
cd apps/api
pip install fastapi uvicorn pandas numpy scipy scikit-learn statsmodels
pip install alphalens-reloaded pyfolio-reloaded vectorbt backtesting
pip install yfinance chromadb openai redis
```

---

## PART 10: COMPLETE FILE LIST

```
Total files to create: ~150
- Frontend components: ~60
- Backend services: ~25
- API routes: ~20
- Utility files: ~15
- Configuration: ~15
- Database/Prisma: ~5
- Docker: ~5
- Documentation: ~5
```

---

## EXECUTION CHECKLIST

1. [ ] Initialize Next.js project with TypeScript
2. [ ] Install and configure shadcn/ui with dark theme
3. [ ] Set up Prisma with PostgreSQL schema
4. [ ] Create landing page with floating formulas
5. [ ] Build dashboard layout with sidebar
6. [ ] Implement Monaco editor with Pine Script syntax
7. [ ] Create TradingView Lightweight Charts integration
8. [ ] Build FastAPI Python backend
9. [ ] Implement Edge Discovery service with Alphalens
10. [ ] Create Monte Carlo simulation engine
11. [ ] Build Pine Script generator with RAG
12. [ ] Implement Prop Firm simulator
13. [ ] Add authentication with NextAuth
14. [ ] Set up Stripe for subscriptions
15. [ ] Create Docker deployment
16. [ ] Write comprehensive tests
17. [ ] Deploy to production

---

*This guide provides everything needed to build a production-ready QuantPad alternative. Follow the specifications precisely for a 1:1 recreation.*
