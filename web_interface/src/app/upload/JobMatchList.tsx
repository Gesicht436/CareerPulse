"use client";

import { useResumeStore } from "@/store/useResumeStore";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Briefcase, Building2, ChevronRight } from "lucide-react";

export const JobMatchList = () => {
  const { matchResults } = useResumeStore();

  if (!matchResults || !matchResults.top_matches) return null;

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col space-y-2">
        <h2 className="text-2xl font-bold tracking-tight">Top Job Matches</h2>
        <p className="text-muted-foreground">
          Based on your redacted resume profile, we found these relevant opportunities.
        </p>
      </div>

      <div className="grid gap-4">
        {matchResults.top_matches.map((match: any, index: number) => (
          <Card key={index} className="overflow-hidden hover:border-primary/50 transition-colors">
            <div className="p-6 flex flex-col md:flex-row gap-6">
              <div className="flex-1 space-y-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 text-primary">
                      <Briefcase className="h-4 w-4" />
                      <span className="text-sm font-medium uppercase tracking-wider">Matched Role</span>
                    </div>
                    <CardTitle className="text-xl">{match.job_title}</CardTitle>
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Building2 className="h-4 w-4" />
                      <span className="text-sm">{match.company}</span>
                    </div>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="text-3xl font-bold text-primary">
                      {match.match_details.overall_score}%
                    </div>
                    <div className="text-xs text-muted-foreground uppercase tracking-tighter">Match Score</div>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-medium uppercase text-muted-foreground">
                    <span>Semantic Similarity</span>
                    <span>{match.match_details.overall_score}%</span>
                  </div>
                  <Progress value={match.match_details.overall_score} className="h-2" />
                </div>

                <div className="flex flex-wrap gap-2">
                  {match.match_details.matched_skills.slice(0, 5).map((skill: string, idx: number) => (
                    <div key={idx} className="bg-primary/5 text-primary border border-primary/10 text-[10px] px-2 py-0.5 rounded-full font-medium">
                      {skill}
                    </div>
                  ))}
                  {match.match_details.matched_skills.length > 5 && (
                    <div className="text-muted-foreground border border-muted-foreground/20 text-[10px] px-2 py-0.5 rounded-full font-medium">
                      +{match.match_details.matched_skills.length - 5} more
                    </div>
                  )}
                </div>
              </div>
              
              <div className="flex items-center justify-center border-t md:border-t-0 md:border-l pt-4 md:pt-0 md:pl-6">
                <button className="flex items-center gap-2 text-sm font-semibold text-primary hover:underline">
                  View Full Report <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
