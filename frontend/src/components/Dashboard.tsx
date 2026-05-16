"use client";

import { useState, useEffect } from "react";
import { getGreeting, TOOLS, type ToolId } from "@/lib/utils";
import { getStats } from "@/lib/api";
import { ArrowUp, Sparkles } from "lucide-react";

interface DashboardProps {
  userName: string;
  apiChoice: string;
  onToolSelect: (tool: ToolId) => void;
  onQuickAsk: (prompt: string, tool: ToolId) => void;
}

const CHIPS = [
  { icon: "💡", label: "Recursion explained", tool: "explainer" as ToolId },
  { icon: "📝", label: "Quiz: OS Chapter 4", tool: "quizzer" as ToolId },
  { icon: "⚡", label: "DS Flashcards", tool: "flashcards" as ToolId },
  { icon: "📊", label: "TCP/IP Diagram", tool: "visualizer" as ToolId },
  { icon: "💼", label: "SDE Interview", tool: "interview" as ToolId },
];

export default function Dashboard({
  userName,
  apiChoice,
  onToolSelect,
  onQuickAsk,
}: DashboardProps) {
  const [query, setQuery] = useState("");
  const [stats, setStats] = useState<ReturnType<typeof getStats> | null>(null);

  useEffect(() => {
    setStats(getStats());
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    // Simple keyword routing
    const q = query.toLowerCase();
    let tool: ToolId = "explainer";
    if (q.includes("quiz") || q.includes("exam") || q.includes("test")) tool = "quizzer";
    else if (q.includes("flashcard")) tool = "flashcards";
    else if (q.includes("diagram") || q.includes("visual") || q.includes("chart")) tool = "visualizer";
    else if (q.includes("interview")) tool = "interview";
    else if (q.includes("resume") || q.includes("cv")) tool = "resume";

    onQuickAsk(query, tool);
    setQuery("");
  };

  const s = stats || { total: 0, week: 0, weekDelta: 0, topTool: null, topCount: 0, recent: [], weeklyByTool: {} };
  const greeting = getGreeting();
  const name = userName || "there";
  const topLabel = s.topTool
    ? TOOLS.find((t) => t.id === s.topTool)?.label || s.topTool
    : "—";

  return (
    <div className="animate-fade-up">
      {/* ── Hero ──────────────────────────────── */}
      <div className="mb-8">
        <h1 className="text-[2rem] font-extrabold text-text tracking-tight leading-tight">
          {greeting}, {name} <span className="inline-block animate-bounce">👋</span>
        </h1>
        <p className="text-text2 text-[0.88rem] mt-1">
          {s.total > 0
            ? `${s.week} interactions this week · ${apiChoice} active`
            : `Ready to study · ${apiChoice} active`}
        </p>
      </div>

      {/* ── Quick Ask ─────────────────────────── */}
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="glass rounded-2xl p-1 flex items-center gap-2">
          <div className="pl-4 text-purple">
            <Sparkles size={18} />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything — explain, quiz, visualize, interview prep..."
            className="flex-1 bg-transparent text-text text-[0.9rem] py-3 px-2 outline-none placeholder:text-muted/60"
          />
          <button
            type="submit"
            className="w-10 h-10 mr-1 rounded-xl bg-s2 hover:bg-purple/20 border border-b1 flex items-center justify-center text-text2 hover:text-purple transition-all"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </form>

      {/* ── Chips ─────────────────────────────── */}
      <div className="flex flex-wrap gap-2 mb-8 justify-center">
        {CHIPS.map((chip) => (
          <button
            key={chip.label}
            onClick={() => onQuickAsk(chip.label, chip.tool)}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-s1 border border-b1 text-text2 text-[0.82rem] hover:border-purple hover:text-purple hover:bg-purple-dim transition-all"
          >
            <span>{chip.icon}</span>
            {chip.label}
          </button>
        ))}
      </div>

      {/* ── Stat Cards ────────────────────────── */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          {
            title: "TOTAL SESSIONS",
            value: s.total > 0 ? s.total.toString() : "—",
            sub: `+${s.week} this week`,
            color: "#7c6fe0",
          },
          {
            title: "THIS WEEK",
            value: s.week > 0 ? s.week.toString() : "—",
            sub: `${s.weekDelta >= 0 ? "↑" : "↓"} ${Math.abs(s.weekDelta)} vs last week`,
            color: "#1fc8a0",
          },
          {
            title: "MOST USED TOOL",
            value: topLabel,
            sub: s.topCount > 0 ? `${s.topCount}× all time` : "—",
            color: "#f0a030",
          },
        ].map((card) => (
          <div
            key={card.title}
            className="glass rounded-xl p-5 relative overflow-hidden group hover:border-[rgba(255,255,255,0.14)] transition-all"
          >
            <div
              className="absolute top-0 left-0 w-full h-[2px]"
              style={{ background: card.color }}
            />
            <div className="text-[0.65rem] font-bold text-muted tracking-[1.2px] uppercase mb-2">
              {card.title}
            </div>
            <div
              className="text-[1.8rem] font-extrabold leading-none mb-1"
              style={{
                color: card.value === "—" ? "var(--color-muted)" : "var(--color-text)",
              }}
            >
              {card.value}
            </div>
            <div className="text-[0.75rem] text-text2">{card.sub}</div>
          </div>
        ))}
      </div>

      {/* ── Tool Grid ─────────────────────────── */}
      <div className="mb-4">
        <div className="text-[0.65rem] font-bold text-muted tracking-[1.2px] uppercase mb-3">
          TOOLS
        </div>
      </div>
      <div className="grid grid-cols-3 gap-4">
        {TOOLS.map((tool, i) => (
          <button
            key={tool.id}
            onClick={() => onToolSelect(tool.id)}
            className="glass rounded-xl p-5 text-left group hover:border-[rgba(255,255,255,0.14)] transition-all relative overflow-hidden"
            style={{ animationDelay: `${i * 60}ms` }}
          >
            <div className="flex items-start justify-between mb-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center text-lg"
                style={{ background: `${tool.color}18` }}
              >
                {tool.icon}
              </div>
              <span
                className="text-[0.6rem] font-bold tracking-wide px-2 py-0.5 rounded-full"
                style={{
                  background: `${tool.color}18`,
                  color: tool.color,
                }}
              >
                {tool.badge}
              </span>
            </div>
            <div className="text-[0.92rem] font-bold text-text mb-1 group-hover:text-purple transition-colors">
              {tool.label}
            </div>
            <div className="text-[0.72rem] text-muted">
              Launch →
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
