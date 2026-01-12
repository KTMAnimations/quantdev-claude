import Link from "next/link";
import { ArrowRight, Lock } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SignInPage() {
  return (
    <main className="min-h-screen flex items-center justify-center px-4 bg-background-primary">
      <Card className="w-full max-w-md bg-background-card border-border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-2xl">
            <Lock className="h-5 w-5 text-accent-primary" />
            Sign In
          </CardTitle>
          <CardDescription>
            Auth isn&apos;t wired up in this repo yet — use the demo without an account.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <div>
            <label className="text-sm text-text-secondary mb-2 block">Email</label>
            <Input type="email" placeholder="you@example.com" />
          </div>
          <div>
            <label className="text-sm text-text-secondary mb-2 block">Password</label>
            <Input type="password" placeholder="••••••••" />
          </div>

          <p className="text-xs text-text-muted">
            These fields are currently non-functional.
          </p>
        </CardContent>

        <CardFooter className="gap-3">
          <Button asChild className="flex-1">
            <Link href="/dashboard">
              Continue
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/">Back</Link>
          </Button>
        </CardFooter>
      </Card>
    </main>
  );
}

