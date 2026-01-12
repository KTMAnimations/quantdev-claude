import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Dark Theme - QuantPad uses deep dark backgrounds
        background: {
          primary: "#0a0a0f",
          secondary: "#111118",
          tertiary: "#1a1a24",
          card: "#16161e",
          elevated: "#1e1e2a",
        },
        // Accent Colors - Purple/Blue gradient accent
        accent: {
          primary: "#8b5cf6",      // Violet-500
          secondary: "#a78bfa",    // Violet-400
          tertiary: "#6366f1",     // Indigo-500
        },
        // Text Colors
        text: {
          primary: "#f8fafc",      // Slate-50
          secondary: "#94a3b8",    // Slate-400
          muted: "#64748b",        // Slate-500
          disabled: "#475569",     // Slate-600
        },
        // Status Colors
        success: "#22c55e",
        "success-muted": "#16a34a",
        warning: "#eab308",
        error: "#ef4444",
        info: "#3b82f6",
        // Chart Colors
        chart: {
          positive: "#22c55e",
          negative: "#ef4444",
          neutral: "#8b5cf6",
          "line-1": "#8b5cf6",
          "line-2": "#06b6d4",
          "line-3": "#f59e0b",
        },
        // Border & Dividers
        border: {
          primary: "#27272a",
          secondary: "#3f3f46",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "Consolas", "monospace"],
      },
      fontSize: {
        xs: "0.75rem",
        sm: "0.875rem",
        base: "1rem",
        lg: "1.125rem",
        xl: "1.25rem",
        "2xl": "1.5rem",
        "3xl": "1.875rem",
        "4xl": "2.25rem",
        "5xl": "3rem",
      },
      borderRadius: {
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
      boxShadow: {
        sm: "0 1px 2px rgba(0, 0, 0, 0.3)",
        md: "0 4px 6px rgba(0, 0, 0, 0.4)",
        lg: "0 10px 15px rgba(0, 0, 0, 0.5)",
        glow: "0 0 20px rgba(139, 92, 246, 0.3)",
      },
      backgroundImage: {
        "accent-gradient": "linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)",
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
      },
      animation: {
        float: "float 20s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0) rotate(0deg)", opacity: "0.2" },
          "50%": { transform: "translateY(-20px) rotate(5deg)", opacity: "0.5" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
