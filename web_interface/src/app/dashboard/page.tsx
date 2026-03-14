import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { TrendingUp, Award, Clock } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="container mx-auto py-12 px-4 md:px-6 space-y-8">
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 max-w-6xl mx-auto w-full">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl">Career Dashboard</h1>
          <p className="text-muted-foreground">
            Track your career readiness and resume performance.
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3 max-w-6xl mx-auto w-full">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Average Match Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">78%</div>
            <p className="text-xs text-muted-foreground">+2% from last upload</p>
            <Progress value={78} className="mt-4" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Top Skill Match</CardTitle>
            <Award className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Python</div>
            <p className="text-xs text-muted-foreground">Matched in 12/15 job descriptions</p>
            <div className="flex flex-wrap gap-2 mt-4">
              <span className="bg-primary/10 text-primary text-[10px] px-2 py-1 rounded">FastAPI</span>
              <span className="bg-primary/10 text-primary text-[10px] px-2 py-1 rounded">Next.js</span>
              <span className="bg-primary/10 text-primary text-[10px] px-2 py-1 rounded">TypeScript</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Analyses Run</CardTitle>
            <Clock className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4</div>
            <p className="text-xs text-muted-foreground">Last run 2 hours ago</p>
          </CardContent>
        </Card>
      </div>

      <Card className="max-w-6xl mx-auto w-full">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                <div className="space-y-1">
                  <p className="text-sm font-medium">Software Engineer Analysis</p>
                  <p className="text-xs text-muted-foreground">Comparison against Google SDE-II</p>
                </div>
                <div className="text-sm font-semibold text-primary">82% Match</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
