import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { ArrowRight, ShieldCheck, Target, TrendingUp } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center w-full">
      {/* Hero Section */}
      <section className="w-full py-24 md:py-32 lg:py-40 bg-linear-to-b from-background to-muted/50">
        <div className="container mx-auto px-4 md:px-6">
          <div className="flex flex-col items-center space-y-8 text-center max-w-4xl mx-auto">
            <div className="space-y-4">
              <h1 className="text-4xl font-extrabold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl">
                Optimize Your Career with <br />
                <span className="bg-linear-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Precision & Security
                </span>
              </h1>
              <p className="mx-auto max-width-[700px] text-muted-foreground md:text-xl/relaxed lg:text-2xl/relaxed">
                CareerPulse is an adversarial-robust ATS simulator that protects your privacy while 
                providing deep insights into your resume's performance.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/upload">
                <Button size="lg" className="h-12 px-8 text-lg">
                  Get Started <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" size="lg" className="h-12 px-8 text-lg">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="w-full py-24 bg-background">
        <div className="container mx-auto px-4 md:px-6">
          <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
            <Card className="border-2 hover:border-primary/50 transition-colors shadow-none">
              <CardHeader>
                <ShieldCheck className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Security-First Analysis</CardTitle>
                <CardDescription>
                  Client-side PII redaction and adversarial detection to keep your data safe.
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="border-2 hover:border-primary/50 transition-colors shadow-none">
              <CardHeader>
                <Target className="h-12 w-12 text-primary mb-4" />
                <CardTitle>RAG-Based Matching</CardTitle>
                <CardDescription>
                  Advanced semantic similarity engine to match your skills with job requirements.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-2 hover:border-primary/50 transition-colors shadow-none">
              <CardHeader>
                <TrendingUp className="h-12 w-12 text-primary mb-4" />
                <CardTitle>Explainable AI Feedback</CardTitle>
                <CardDescription>
                  Actionable insights and skill-gap analysis to help you land your dream role.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Trust Banner */}
      <section className="w-full py-16 border-y bg-muted/20">
        <div className="container mx-auto px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-6 text-center max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold tracking-tighter sm:text-3xl">
              Trusted by Professionals from Top Tech Companies
            </h2>
            <div className="flex flex-wrap justify-center gap-12 opacity-50 grayscale">
              <span className="text-xl font-semibold hover:opacity-100 transition-opacity">Google</span>
              <span className="text-xl font-semibold hover:opacity-100 transition-opacity">Amazon</span>
              <span className="text-xl font-semibold hover:opacity-100 transition-opacity">Microsoft</span>
              <span className="text-xl font-semibold hover:opacity-100 transition-opacity">Meta</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
