"use client";

import { API_BASE, type ToolId } from "./utils";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export async function sendPrompt(
  toolId: ToolId,
  prompt: string,
  context: string = "",
  style: string = "Beginner Friendly",
  apiChoice: string = "Gemini"
): Promise<string> {
  const tool = await import("./utils").then((m) => m.getToolById(toolId));
  if (!tool) throw new Error(`Unknown tool: ${toolId}`);

  const res = await fetch(`${API_BASE}${tool.endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      context,
      style,
      api_choice: apiChoice,
    }),
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }

  const data = await res.json();
  return data.response;
}

// Local storage helpers for activity tracking
const STORAGE_KEY = "copilot_activity";

interface ActivityEntry {
  tool: string;
  prompt: string;
  timestamp: number;
}

export function logActivity(tool: string, prompt: string) {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const entries: ActivityEntry[] = raw ? JSON.parse(raw) : [];
    entries.push({ tool, prompt, timestamp: Date.now() });
    // Keep last 200 entries
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(entries.slice(-200))
    );
  } catch {
    // localStorage unavailable
  }
}

export function getActivity(): ActivityEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function getStats() {
  const entries = getActivity();
  const now = Date.now();
  const weekMs = 7 * 24 * 60 * 60 * 1000;
  const thisWeek = entries.filter((e) => now - e.timestamp < weekMs);
  const lastWeek = entries.filter(
    (e) => now - e.timestamp >= weekMs && now - e.timestamp < weekMs * 2
  );

  // Find most used tool
  const counts: Record<string, number> = {};
  for (const e of entries) {
    counts[e.tool] = (counts[e.tool] || 0) + 1;
  }
  const topTool = Object.entries(counts).sort((a, b) => b[1] - a[1])[0];

  return {
    total: entries.length,
    week: thisWeek.length,
    weekDelta: thisWeek.length - lastWeek.length,
    topTool: topTool ? topTool[0] : null,
    topCount: topTool ? topTool[1] : 0,
    recent: entries.slice(-5).reverse(),
    weeklyByTool: thisWeek.reduce(
      (acc, e) => {
        acc[e.tool] = (acc[e.tool] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    ),
  };
}
