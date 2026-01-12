"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Lightbulb,
  Code2,
  FlaskConical,
  Settings2,
  Rocket,
  Library,
  MessageSquare,
  Home,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const NAV_ITEMS = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: Home,
  },
  {
    title: "Ideation",
    href: "/ideation",
    icon: Lightbulb,
    description: "Edge Discovery",
  },
  {
    title: "Code",
    href: "/code",
    icon: Code2,
    description: "Pine Script Generator",
  },
  {
    title: "Test",
    href: "/test",
    icon: FlaskConical,
    description: "Monte Carlo Testing",
  },
  {
    title: "Optimize",
    href: "/optimize",
    icon: Settings2,
    description: "Regression Analysis",
  },
  {
    title: "Deploy",
    href: "/deploy",
    icon: Rocket,
    description: "Prop Firm Simulator",
  },
  {
    title: "Library",
    href: "/library",
    icon: Library,
    description: "Strategy Library",
  },
  {
    title: "Copilot",
    href: "/copilot",
    icon: MessageSquare,
    description: "AI Chat",
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "h-screen bg-background-secondary border-r border-border-primary flex flex-col transition-all duration-300",
        collapsed ? "w-16" : "w-64"
      )}
    >
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border-primary">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-accent-gradient flex items-center justify-center">
              <span className="text-white font-bold text-lg">O</span>
            </div>
            <span className="font-semibold text-text-primary">OpenQuant</span>
          </Link>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className="ml-auto"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200",
                isActive
                  ? "bg-accent-primary/10 text-accent-primary"
                  : "text-text-secondary hover:bg-background-tertiary hover:text-text-primary"
              )}
            >
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {!collapsed && (
                <div className="flex flex-col">
                  <span className="font-medium">{item.title}</span>
                  {item.description && (
                    <span className="text-xs text-text-muted">
                      {item.description}
                    </span>
                  )}
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Section */}
      <div className="p-4 border-t border-border-primary">
        {!collapsed && (
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-accent-primary/20 flex items-center justify-center">
              <span className="text-accent-primary font-medium text-sm">U</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-text-primary truncate">
                User
              </p>
              <p className="text-xs text-text-muted truncate">Free Plan</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}
