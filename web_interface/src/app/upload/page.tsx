import { FileUploadZone } from "./FileUploadZone";
import { ShieldCheck, Lock, EyeOff } from "lucide-react";

export default function UploadPage() {
  return (
    <div className="container mx-auto py-12 px-4 md:px-6 space-y-12">
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">
          Secure Resume Analysis
        </h1>
        <p className="mx-auto max-w-[600px] text-muted-foreground md:text-xl">
          Upload your resume for a secure, AI-powered match analysis and skill-gap report.
        </p>
      </div>

      <FileUploadZone />

      <div className="grid gap-8 sm:grid-cols-3 max-w-4xl mx-auto pt-12 border-t">
        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-3 rounded-full bg-primary/10">
            <Lock className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold text-lg">Zero-Trust Upload</h3>
          <p className="text-sm text-muted-foreground">
            PII is redacted locally on your device before it ever reaches our servers.
          </p>
        </div>
        
        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-3 rounded-full bg-primary/10">
            <ShieldCheck className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold text-lg">Adversarial Defense</h3>
          <p className="text-sm text-muted-foreground">
            Built-in protection against hidden text and prompt injection attempts.
          </p>
        </div>

        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-3 rounded-full bg-primary/10">
            <EyeOff className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold text-lg">Privacy Guaranteed</h3>
          <p className="text-sm text-muted-foreground">
            Your personal data is never stored, only the skill-based embeddings are processed.
          </p>
        </div>
      </div>
    </div>
  );
}
