import { Hero } from "@/components/landing/Hero";
import { WorkflowSteps } from "@/components/landing/WorkflowSteps";
import { Features } from "@/components/landing/Features";

export default function LandingPage() {
  return (
    <main>
      <Hero />
      <WorkflowSteps />
      <Features />

      {/* Footer */}
      <footer className="py-12 bg-background-secondary border-t border-border-primary">
        <div className="container mx-auto px-4 text-center">
          <p className="text-text-muted">
            &copy; {new Date().getFullYear()} OpenQuant. Open-source quantitative trading platform.
          </p>
          <p className="text-text-muted text-sm mt-2">
            Built with Next.js, FastAPI, and Python
          </p>
        </div>
      </footer>
    </main>
  );
}
