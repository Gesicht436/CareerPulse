import { create } from 'zustand';

interface ResumeState {
  file: File | null;
  redactedFile: File | null;
  isRedacting: boolean;
  analysisResult: any | null;
  matchResults: any | null; // Added this
  setFile: (file: File | null) => void;
  setRedactedFile: (file: File | null) => void;
  setIsRedacting: (status: boolean) => void;
  setAnalysisResult: (result: any | null) => void;
  setMatchResults: (results: any | null) => void; // Added this
}

export const useResumeStore = create<ResumeState>((set) => ({
  file: null,
  redactedFile: null,
  isRedacting: false,
  analysisResult: null,
  matchResults: null, // Initialized this
  setFile: (file) => set({ file }),
  setRedactedFile: (redactedFile) => set({ redactedFile }),
  setIsRedacting: (isRedacting) => set({ isRedacting }),
  setAnalysisResult: (analysisResult) => set({ analysisResult }),
  setMatchResults: (matchResults) => set({ matchResults }), // Implemented this
}));
