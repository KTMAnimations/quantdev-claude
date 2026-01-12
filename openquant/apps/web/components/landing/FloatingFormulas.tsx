"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const FORMULAS = [
  "S = (Rp - Rf) / \u03C3p",         // Sharpe Ratio
  "\u03C3 = \u221A(\u03A3(xi - \u03BC)\u00B2 / N)",      // Standard Deviation
  "E[X] = \u03A3 xi \u00B7 P(xi)",        // Expected Value
  "f* = (bp - q) / b",          // Kelly Criterion
  "MDD = (Peak - Trough) / Peak", // Max Drawdown
  "Sortino = (R - T) / DR",     // Sortino Ratio
  "\u03B2 = Cov(ri, rm) / Var(rm)",  // Beta
  "\u03B1 = Ri - [Rf + \u03B2(Rm - Rf)]", // Alpha
  "VaR = \u03BC - z\u03C3",               // Value at Risk
  "PF = \u03A3Wins / \u03A3|Losses|",     // Profit Factor
  "CAGR = (Vf/Vi)^(1/t) - 1",   // CAGR
  "R\u00B2 = 1 - (SSres/SStot)",     // R-Squared
  "\u03C1 = Cov(X,Y) / \u03C3x\u03C3y",        // Correlation
  "IR = (Rp - Rb) / \u03C3(Rp - Rb)", // Information Ratio
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
            x: `${Math.random() * 100}%`,
            y: `${Math.random() * 100}%`,
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
