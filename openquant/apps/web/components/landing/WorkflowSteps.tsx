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
      "Deploy live \u2014 or use the Prop Firm Assistant to simulate your odds of passing major prop firm challenges.",
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
                    <div
                      className={`flex-shrink-0 w-12 h-12 rounded-full ${step.bgColor} flex items-center justify-center`}
                    >
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
