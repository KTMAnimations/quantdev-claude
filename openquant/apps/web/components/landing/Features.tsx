"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Brain,
  BarChart3,
  Shuffle,
  Target,
  Code,
  Wallet,
} from "lucide-react";

const FEATURES = [
  {
    title: "AI-Powered Edge Discovery",
    description:
      "Describe any trading feature in plain English and get instant statistical analysis. Uses Alphalens and ML to measure predictive power.",
    icon: Brain,
  },
  {
    title: "Monte Carlo Simulations",
    description:
      "Institutional-grade bootstrapping and randomization tests to separate skill from luck. 10,000+ simulations for robust confidence intervals.",
    icon: Shuffle,
  },
  {
    title: "Pine Script Generator",
    description:
      "Natural language to TradingView code. RAG-powered generation with syntax validation and error correction.",
    icon: Code,
  },
  {
    title: "Advanced Analytics",
    description:
      "Sharpe ratios, drawdown analysis, factor regression, and SHAP explainability. Full Pyfolio-style tearsheets.",
    icon: BarChart3,
  },
  {
    title: "Prop Firm Simulator",
    description:
      "Model your odds of passing FTMO, The5%ers, Apex, and more. Accounts for daily limits, trailing drawdowns, and consistency rules.",
    icon: Target,
  },
  {
    title: "Expected Value Calculator",
    description:
      "Calculate the true expected value of taking a prop firm challenge based on your strategy's edge and risk profile.",
    icon: Wallet,
  },
];

export function Features() {
  return (
    <section className="py-24 bg-background-primary">
      <div className="container mx-auto px-4">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-text-primary mb-4">
            Institutional-Grade Tools
          </h2>
          <p className="text-text-secondary text-lg max-w-2xl mx-auto">
            Everything you need to discover, validate, and deploy quantitative trading strategies.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full bg-background-card border-border-primary hover:border-accent-primary/50 transition-all duration-300">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-accent-primary/10 flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-accent-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-text-secondary">{feature.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
