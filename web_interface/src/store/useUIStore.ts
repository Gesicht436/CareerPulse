import { create } from 'zustand';

interface UIState {
  isLoading: boolean;
  setIsLoading: (status: boolean) => void;
  notifications: string[];
  addNotification: (message: string) => void;
  clearNotifications: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  isLoading: false,
  setIsLoading: (isLoading) => set({ isLoading }),
  notifications: [],
  addNotification: (message) => set((state) => ({ notifications: [...state.notifications, message] })),
  clearNotifications: () => set({ notifications: [] }),
}));
