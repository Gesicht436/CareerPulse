"use client";

import { useCallback, useState } from "react";
import { useResumeStore } from "@/store/useResumeStore";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, X, ShieldAlert } from "lucide-react";
import { toast } from "sonner";

export const FileUploadZone = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const { file, setFile, setAnalysisResult } = useResumeStore();

  const uploadResume = async () => {
    if (!file) return;

    setIsUploading(true);
    toast.info("Analyzing resume for security and PII...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/v1/security/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload resume");
      }

      const result = await response.json();
      setAnalysisResult(result);
      
      if (result.security_report.is_safe) {
        toast.success("Resume analyzed and secure!");
        // We can redirect or update UI here
      } else {
        const criticalFlags = result.security_report.flags.filter((f: any) => f.severity === 'critical' || f.severity === 'high');
        if (criticalFlags.length > 0) {
          toast.error(`Security Warning: ${criticalFlags[0].detail}`);
        } else {
          toast.warning("Analysis complete with some minor warnings.");
        }
      }
    } catch (error) {
      console.error("Upload error:", error);
      toast.error("An error occurred during upload. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleFile = (selectedFile: File) => {
    if (selectedFile.type !== "application/pdf") {
      toast.error("Please upload a PDF file.");
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      toast.error("File size should be less than 5MB.");
      return;
    }
    setFile(selectedFile);
    toast.success("File uploaded successfully.");
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) handleFile(droppedFile);
  }, []);

  const onSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) handleFile(selectedFile);
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      <Card
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        className={`relative border-2 border-dashed transition-all duration-200 p-12 text-center flex flex-col items-center justify-center gap-4 ${
          isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25"
        } ${file ? "border-solid border-primary/50" : ""}`}
      >
        {!file ? (
          <>
            <div className="p-4 rounded-full bg-primary/10">
              <Upload className="h-8 w-8 text-primary" />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">Upload your Resume</h3>
              <p className="text-muted-foreground">
                Drag and drop your PDF here, or click to browse
              </p>
            </div>
            <input
              type="file"
              accept=".pdf"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              onChange={onSelect}
            />
          </>
        ) : (
          <div className="flex items-center gap-4 w-full justify-between p-4 bg-muted/50 rounded-lg">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-primary/20">
                <FileText className="h-6 w-6 text-primary" />
              </div>
              <div className="text-left">
                <p className="font-medium truncate max-w-[200px]">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setFile(null)}
              className="hover:bg-destructive/10 hover:text-destructive"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        )}
      </Card>

      {file && (
        <div className="flex flex-col gap-4 items-center">
          <div className="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 p-3 rounded-md border border-amber-200">
            <ShieldAlert className="h-4 w-4" />
            <span>CareerPulse will redact PII (Name, Email, Phone) locally before analysis.</span>
          </div>
          <Button 
            size="lg" 
            className="w-full sm:w-auto px-12 h-12"
            onClick={uploadResume}
            disabled={isUploading}
          >
            {isUploading ? "Analyzing..." : "Start Secure Analysis"}
          </Button>
        </div>
      )}
    </div>
  );
};
