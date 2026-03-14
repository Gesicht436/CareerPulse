import { create } from 'zustand';

interface ResumeState {
  file: File | null;
  redactedFile: File | null;
  isRedacting: boolean;
  analysisResult: any | null;
  setFile: (file: File | null) => void;
  setRedactedFile: (file: File | null) => void;
  setIsRedacting: (status: boolean) => void;
  setAnalysisResult: (result: any | null) => void;
}

export const useResumeStore = create<ResumeState>((set) => ({
  file: null,
  redactedFile: null,
  isRedacting: false,
  analysisResult: null,
  setFile: (file) => set({ file }),
  setRedactedFile: (redactedFile) => set({ redactedFile }),
  setIsRedacting: (isRedacting) => set({ isRedacting }),
  setAnalysisResult: (analysisResult) => set({ analysisResult }),
}));
