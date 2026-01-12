import type { Trade } from "@/lib/strategyStore";

function mulberry32(seed: number) {
  return () => {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function generateSampleTrades(count = 120): Trade[] {
  const rng = mulberry32(42);
  const start = new Date("2020-01-01T00:00:00.000Z").getTime();
  const day = 24 * 60 * 60 * 1000;

  const trades: Trade[] = [];
  for (let i = 0; i < count; i++) {
    const entry = new Date(start + i * 2 * day);
    const exit = new Date(entry.getTime() + day);

    const win = rng() < 0.55;
    const magnitude = win ? 0.01 + rng() * 0.015 : 0.006 + rng() * 0.012;
    const return_pct = win ? magnitude : -magnitude;
    const pnl = 10_000 * return_pct;

    trades.push({
      entry_time: entry.toISOString(),
      exit_time: exit.toISOString(),
      pnl,
      return_pct,
    });
  }

  return trades;
}

export function parseTradesCsv(csvText: string): Trade[] {
  const lines = csvText
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean);

  if (lines.length < 2) return [];

  const header = lines[0]
    .split(",")
    .map((h) => h.trim().toLowerCase());

  const idx = {
    entry_time: header.indexOf("entry_time"),
    exit_time: header.indexOf("exit_time"),
    pnl: header.indexOf("pnl"),
    return_pct: header.indexOf("return_pct"),
  };

  if (idx.entry_time === -1 || idx.exit_time === -1 || idx.return_pct === -1) return [];

  const trades: Trade[] = [];
  for (const line of lines.slice(1)) {
    const cols = line.split(",").map((c) => c.trim());
    const entry_time = cols[idx.entry_time];
    const exit_time = cols[idx.exit_time];
    const returnPctRaw = cols[idx.return_pct];
    const pnlRaw = idx.pnl === -1 ? undefined : cols[idx.pnl];

    const return_pct = Number(returnPctRaw);
    const pnl = pnlRaw === undefined ? return_pct * 10_000 : Number(pnlRaw);

    if (!entry_time || !exit_time) continue;
    if (!Number.isFinite(return_pct)) continue;
    if (!Number.isFinite(pnl)) continue;

    trades.push({ entry_time, exit_time, pnl, return_pct });
  }

  return trades;
}

export function buildEquityCurve(
  trades: Trade[],
  initialCapital = 10_000
): { date: string; equity: number; drawdown: number }[] {
  let equity = initialCapital;
  let peak = initialCapital;

  const curve: { date: string; equity: number; drawdown: number }[] = [
    { date: "Start", equity, drawdown: 0 },
  ];

  for (const trade of trades) {
    equity *= 1 + trade.return_pct;
    peak = Math.max(peak, equity);
    const drawdown = peak > 0 ? (peak - equity) / peak : 0;

    const dateLabel = trade.exit_time ? trade.exit_time.slice(0, 10) : "Trade";
    curve.push({ date: dateLabel, equity, drawdown });
  }

  return curve;
}

export function buildReturnHistogram(
  trades: Trade[],
  bins = 20
): { bin: string; count: number }[] {
  if (trades.length === 0) return [];

  const returns = trades.map((t) => t.return_pct);
  const min = Math.min(...returns);
  const max = Math.max(...returns);
  const span = Math.max(1e-9, max - min);
  const width = span / bins;

  const counts = Array.from({ length: bins }, () => 0);
  for (const r of returns) {
    const idx = Math.min(bins - 1, Math.max(0, Math.floor((r - min) / width)));
    counts[idx] += 1;
  }

  return counts.map((count, i) => {
    const a = min + i * width;
    const b = a + width;
    const label = `${(a * 100).toFixed(1)}%–${(b * 100).toFixed(1)}%`;
    return { bin: label, count };
  });
}

export function tradesToDailyReturns(trades: Trade[]): number[] {
  const byDay = new Map<string, number>();
  for (const t of trades) {
    const day = t.exit_time?.slice(0, 10);
    if (!day) continue;
    byDay.set(day, (byDay.get(day) ?? 0) + t.return_pct);
  }

  return Array.from(byDay.entries())
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([, r]) => r);
}
