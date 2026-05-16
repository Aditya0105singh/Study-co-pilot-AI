import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// API base URL
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Tool definitions
export const TOOLS = [
  { id: "explainer",  icon: "🧠", label: "Study & Understand",  color: "#7c6fe0", badge: "AI",  endpoint: "/api/explain" },
  { id: "visualizer", icon: "📊", label: "Visualize Concepts",  color: "#1fc8a0", badge: "Hot", endpoint: "/api/visualize" },
  { id: "flashcards", icon: "⚡", label: "Flashcards",          color: "#7c6fe0", badge: "New", endpoint: "/api/flashcards" },
  { id: "quizzer",    icon: "📝", label: "Exam Preparation",    color: "#f0a030", badge: "AI",  endpoint: "/api/quiz/generate" },
  { id: "interview",  icon: "💼", label: "Interview Practice",  color: "#f26d50", badge: "Pro", endpoint: "/api/interview" },
  { id: "resume",     icon: "📄", label: "Resume Review",       color: "#f0a030", badge: "AI",  endpoint: "/api/resume" },
] as const;

export type ToolId = (typeof TOOLS)[number]["id"];

export function getToolById(id: string) {
  return TOOLS.find((t) => t.id === id);
}

// Greeting helpers
export function getGreeting(): string {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}
