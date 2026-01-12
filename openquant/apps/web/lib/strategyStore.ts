import { create } from "zustand";

export interface Trade {
  entry_time: string;
  exit_time: string;
  pnl: number;
  return_pct: number;
}

interface StrategyStore {
  pineCode: string | null;
  trades: Trade[];
  setPineCode: (pineCode: string | null) => void;
  setTrades: (trades: Trade[]) => void;
  clear: () => void;
}

export const useStrategyStore = create<StrategyStore>((set) => ({
  pineCode: null,
  trades: [],
  setPineCode: (pineCode) => set({ pineCode }),
  setTrades: (trades) => set({ trades }),
  clear: () => set({ pineCode: null, trades: [] }),
}));

