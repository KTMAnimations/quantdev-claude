import { Header } from "@/components/dashboard/Header";
import { EdgeDiscoveryPanel } from "@/components/ideation/EdgeDiscoveryPanel";

export default function IdeationPage() {
  return (
    <div className="flex flex-col h-full">
      <Header
        title="Edge Discovery"
        subtitle="Describe any feature and measure its predictive power"
      />
      <div className="flex-1 p-6">
        <EdgeDiscoveryPanel />
      </div>
    </div>
  );
}
