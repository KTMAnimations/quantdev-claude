import type { Metadata } from "next";
import "@/styles/globals.css";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "OpenQuant - Your AI Quant Dev",
  description:
    "Turn trading ideas into code, stats, and deployed systems in one seamless workflow.",
  keywords: [
    "quantitative trading",
    "trading strategies",
    "pine script",
    "monte carlo",
    "backtesting",
    "prop firm",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background-primary text-text-primary antialiased">
        {children}
        <Toaster theme="dark" richColors closeButton />
      </body>
    </html>
  );
}
