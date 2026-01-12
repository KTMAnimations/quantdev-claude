"use client";

import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User, Loader2 } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const SUGGESTIONS = [
  "How do I calculate the Sharpe ratio?",
  "Explain the Kelly criterion for position sizing",
  "What is a good win rate for a scalping strategy?",
  "How do I avoid overfitting in backtests?",
];

export default function CopilotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Hi! I'm your quant trading assistant. I can help you with strategy development, statistical analysis, Pine Script coding, and risk management. What would you like to know?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulate AI response
    await new Promise((resolve) => setTimeout(resolve, 1500));

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: getResponse(input),
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const getResponse = (query: string): string => {
    const q = query.toLowerCase();
    if (q.includes("sharpe")) {
      return "The Sharpe ratio measures risk-adjusted returns. It's calculated as:\n\nSharpe = (Portfolio Return - Risk-Free Rate) / Portfolio Standard Deviation\n\nA Sharpe ratio above 1.0 is considered good, above 2.0 is very good, and above 3.0 is excellent. For trading strategies, aim for at least 1.5 to account for real-world slippage and costs.";
    }
    if (q.includes("kelly")) {
      return "The Kelly Criterion determines optimal position size:\n\nf* = (bp - q) / b\n\nWhere:\n- f* = fraction of capital to bet\n- b = odds received (profit/risk)\n- p = probability of winning\n- q = probability of losing (1 - p)\n\nMany traders use 'fractional Kelly' (25-50% of the calculated value) to reduce volatility and account for estimation errors.";
    }
    if (q.includes("win rate") || q.includes("scalping")) {
      return "For scalping strategies, a good win rate depends on your risk/reward ratio:\n\n- With 1:1 R:R, aim for 55-60% win rate\n- With 2:1 R:R, 40-45% is sufficient\n- With 3:1 R:R, 30-35% can still be profitable\n\nRemember that transaction costs significantly impact scalping. A strategy with 60% win rate and 1:1 R:R needs at least 70% gross win rate to remain profitable after costs.";
    }
    if (q.includes("overfit")) {
      return "To avoid overfitting in backtests:\n\n1. **Use out-of-sample testing** - Never optimize on data you'll test on\n2. **Walk-forward analysis** - Continuously re-optimize and test on new data\n3. **Keep rules simple** - Fewer parameters = less overfitting risk\n4. **Statistical significance** - Ensure enough trades for reliable statistics\n5. **Monte Carlo simulation** - Test robustness to trade order changes\n6. **Multiple markets/timeframes** - A robust edge should work across instruments\n7. **Parameter stability** - Small parameter changes shouldn't dramatically affect results";
    }
    return "That's a great question about quantitative trading! I'd recommend breaking this down into the statistical and practical components. Could you provide more context about your specific use case or trading style? This will help me give you more targeted advice.";
  };

  const handleSuggestion = (suggestion: string) => {
    setInput(suggestion);
  };

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Quant Copilot"
        subtitle="Your AI trading assistant"
      />
      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <Card className="flex-1 flex flex-col bg-background-card border-border-primary overflow-hidden">
          <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === "user"
                        ? "bg-accent-primary/20"
                        : "bg-background-tertiary"
                    }`}
                  >
                    {message.role === "user" ? (
                      <User className="h-4 w-4 text-accent-primary" />
                    ) : (
                      <Bot className="h-4 w-4 text-text-secondary" />
                    )}
                  </div>
                  <div
                    className={`max-w-[80%] p-4 rounded-lg ${
                      message.role === "user"
                        ? "bg-accent-primary/10 text-text-primary"
                        : "bg-background-tertiary text-text-primary"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-background-tertiary flex items-center justify-center">
                    <Bot className="h-4 w-4 text-text-secondary" />
                  </div>
                  <div className="bg-background-tertiary p-4 rounded-lg">
                    <Loader2 className="h-4 w-4 animate-spin text-accent-primary" />
                  </div>
                </div>
              )}
            </div>

            {/* Suggestions */}
            {messages.length === 1 && (
              <div className="px-6 pb-4">
                <p className="text-sm text-text-muted mb-2">Suggested questions:</p>
                <div className="flex flex-wrap gap-2">
                  {SUGGESTIONS.map((suggestion) => (
                    <Button
                      key={suggestion}
                      variant="outline"
                      size="sm"
                      onClick={() => handleSuggestion(suggestion)}
                      className="text-xs"
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="p-4 border-t border-border-primary">
              <div className="flex gap-3">
                <Input
                  placeholder="Ask about trading strategies, statistics, or Pine Script..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  className="bg-background-tertiary border-border-primary"
                />
                <Button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="bg-accent-gradient"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
