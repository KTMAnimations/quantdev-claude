import Link from "next/link";
import {
  Code2,
  FlaskConical,
  Lightbulb,
  MessageSquare,
  Rocket,
  Settings2,
  Library,
} from "lucide-react";

import { Header } from "@/components/dashboard/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const QUICK_START = [
  {
    title: "Discover Your Edge",
    description: "Turn an idea into a testable feature.",
    href: "/ideation",
    icon: Lightbulb,
  },
  {
    title: "Generate Pine Script",
    description: "Describe a strategy and get code.",
    href: "/code",
    icon: Code2,
  },
  {
    title: "Monte Carlo Testing",
    description: "Stress-test your backtest results.",
    href: "/test",
    icon: FlaskConical,
  },
  {
    title: "Regression Analysis",
    description: "Find drivers of performance.",
    href: "/optimize",
    icon: Settings2,
  },
  {
    title: "Prop Firm Simulator",
    description: "See if you can pass the rules.",
    href: "/deploy",
    icon: Rocket,
  },
  {
    title: "Strategy Library",
    description: "Browse community strategies.",
    href: "/library",
    icon: Library,
  },
  {
    title: "Quant Copilot",
    description: "Chat about trading + stats.",
    href: "/copilot",
    icon: MessageSquare,
  },
] as const;

export default function DashboardPage() {
  return (
    <div className="flex flex-col h-full">
      <Header title="Dashboard" subtitle="Quick start" />
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {QUICK_START.map((item) => {
            const Icon = item.icon;
            return (
              <Link key={item.href} href={item.href} className="block">
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Icon className="h-5 w-5 text-accent-primary" />
                      {item.title}
                    </CardTitle>
                    <CardDescription>{item.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <span className="text-sm text-accent-primary">Open →</span>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

