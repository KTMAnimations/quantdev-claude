"use client";

import { useState, useRef, useEffect } from "react";
import { Header } from "@/components/dashboard/Header";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, Bot, User, Loader2, AlertCircle } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
}

const SUGGESTIONS = [
  "How do I calculate the Sharpe ratio?",
  "Explain the Kelly criterion for position sizing",
  "What is a good win rate for a scalping strategy?",
  "How do I avoid overfitting in backtests?",
  "Write a Pine Script for RSI divergence",
  "What's a safe daily drawdown limit for prop firms?",
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
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    // Add user message and clear input
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setError(null);

    // Create placeholder for assistant message
    const assistantId = (Date.now() + 1).toString();
    setMessages((prev) => [
      ...prev,
      { id: assistantId, role: "assistant", content: "", isStreaming: true },
    ]);

    try {
      // Prepare messages for API (exclude the empty assistant placeholder)
      const apiMessages = messages
        .concat(userMessage)
        .filter((m) => m.content.trim())
        .map((m) => ({
          role: m.role,
          content: m.content,
        }));

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: apiMessages,
          stream: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`Chat request failed: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      let accumulatedContent = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();

            if (data === "[DONE]") {
              continue;
            }

            try {
              const parsed = JSON.parse(data);

              if (parsed.error) {
                throw new Error(parsed.error);
              }

              if (parsed.content) {
                accumulatedContent += parsed.content;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? { ...m, content: accumulatedContent }
                      : m
                  )
                );
              }
            } catch (parseError) {
              // Ignore JSON parse errors for incomplete chunks
              if (data && data !== "[DONE]") {
                console.debug("Skipping non-JSON chunk:", data);
              }
            }
          }
        }
      }

      // Mark streaming as complete
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId ? { ...m, isStreaming: false } : m
        )
      );
    } catch (err) {
      console.error("Chat error:", err);
      setError(err instanceof Error ? err.message : "An error occurred");

      // Update the assistant message with error
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? {
                ...m,
                content:
                  "Sorry, I encountered an error connecting to the chat service. Please make sure the backend is running and try again.",
                isStreaming: false,
              }
            : m
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestion = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header title="Quant Copilot" subtitle="Your AI trading assistant" />
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
                    <p className="whitespace-pre-wrap">
                      {message.content}
                      {message.isStreaming && (
                        <span className="inline-block w-2 h-4 ml-1 bg-accent-primary animate-pulse" />
                      )}
                    </p>
                  </div>
                </div>
              ))}

              {/* Loading indicator when waiting for stream to start */}
              {isLoading &&
                messages[messages.length - 1]?.content === "" &&
                messages[messages.length - 1]?.isStreaming && (
                  <div className="flex gap-3">
                    <div className="w-8 h-8 rounded-full bg-background-tertiary flex items-center justify-center">
                      <Bot className="h-4 w-4 text-text-secondary" />
                    </div>
                    <div className="bg-background-tertiary p-4 rounded-lg">
                      <Loader2 className="h-4 w-4 animate-spin text-accent-primary" />
                    </div>
                  </div>
                )}

              <div ref={messagesEndRef} />
            </div>

            {/* Error Banner */}
            {error && (
              <div className="px-6 py-3 bg-error/10 border-t border-error/30 flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-error" />
                <span className="text-sm text-error">{error}</span>
              </div>
            )}

            {/* Suggestions */}
            {messages.length === 1 && (
              <div className="px-6 pb-4">
                <p className="text-sm text-text-muted mb-2">
                  Suggested questions:
                </p>
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
                  onKeyDown={handleKeyDown}
                  disabled={isLoading}
                  className="bg-background-tertiary border-border-primary"
                />
                <Button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="bg-accent-gradient"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
