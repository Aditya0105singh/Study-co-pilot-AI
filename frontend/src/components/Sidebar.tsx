"use client";

import { TOOLS, type ToolId } from "@/lib/utils";
import {
  LayoutDashboard,
  Users,
  ChevronRight,
} from "lucide-react";
import FocusTimer from "./FocusTimer";

interface SidebarProps {
  currentTool: ToolId | null;
  currentView: "dashboard" | "tool" | "rooms";
  onNavigate: (tool: ToolId | null) => void;
  onStudyRooms: () => void;
  userName: string;
  onNameChange: (name: string) => void;
  apiChoice: string;
}

export default function Sidebar({
  currentTool,
  currentView,
  onNavigate,
  onStudyRooms,
  userName,
  onNameChange,
  apiChoice,
}: SidebarProps) {
  return (
    <aside className="fixed left-0 top-0 bottom-0 w-[260px] z-50 flex flex-col border-r border-b1 bg-[rgba(0,0,0,0.92)] backdrop-blur-[24px] backdrop-saturate-[160%]">
      {/* ── Logo ────────────────────────────── */}
      <div className="flex items-center gap-3 px-5 pt-5 pb-3">
        <div className="w-9 h-9 rounded-[10px] bg-gradient-to-br from-purple to-[#5b51c8] flex items-center justify-center text-white text-xs font-extrabold shadow-[0_2px_12px_rgba(124,111,224,0.3)]">
          SC
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-[0.98rem] font-bold text-text leading-tight">
            Copilot AI
          </div>
          <div className="text-[0.62rem] text-muted">
            Study Intelligence Suite
          </div>
        </div>
        <div className="flex items-center gap-1 text-[0.66rem] font-semibold px-2 py-0.5 rounded-full bg-teal-dim text-teal border border-[rgba(31,200,160,0.22)] whitespace-nowrap">
          <span className="w-[5px] h-[5px] rounded-full bg-teal animate-pulse" />
          {apiChoice}
        </div>
      </div>

      {/* ── Name Input ──────────────────────── */}
      <div className="px-4 pb-2">
        <input
          type="text"
          value={userName}
          onChange={(e) => onNameChange(e.target.value)}
          placeholder="Your name…"
          className="w-full bg-s1 border border-b1 rounded-lg px-3 py-[7px] text-[0.84rem] text-text placeholder:text-muted/60 focus:border-purple focus:ring-1 focus:ring-purple/20 outline-none transition-all"
        />
      </div>

      <div className="h-px bg-b1 mx-4" />

      {/* ── Dashboard Button ────────────────── */}
      <div className="px-3 pt-3">
        <button
          onClick={() => onNavigate(null)}
          className={`w-full flex items-center gap-2.5 px-3 py-[7px] rounded-lg text-[0.84rem] font-medium transition-all ${
            currentView === "dashboard"
              ? "bg-purple-dim text-purple font-semibold"
              : "text-text2 hover:bg-s2 hover:text-text"
          }`}
        >
          <LayoutDashboard size={16} />
          Dashboard
        </button>
      </div>

      {/* ── Tools ───────────────────────────── */}
      <div className="px-4 pt-4 pb-1">
        <div className="text-[0.6rem] font-bold text-muted tracking-[1.4px] uppercase">
          Tools
        </div>
      </div>
      <nav className="flex-1 overflow-y-auto px-3 space-y-0.5">
        {TOOLS.map((tool) => (
          <button
            key={tool.id}
            onClick={() => onNavigate(tool.id)}
            className={`w-full flex items-center gap-2.5 px-3 py-[7px] rounded-lg text-[0.84rem] transition-all group ${
              currentView === "tool" && currentTool === tool.id
                ? "bg-purple-dim text-purple font-semibold"
                : "text-text2 hover:bg-s2 hover:text-text"
            }`}
          >
            <span className="text-base">{tool.icon}</span>
            <span className="flex-1 text-left">{tool.label}</span>
            <ChevronRight
              size={14}
              className="opacity-0 group-hover:opacity-50 transition-opacity"
            />
          </button>
        ))}

        {/* ── Collaborate ─────────────────────── */}
        <div className="pt-3 pb-1 px-1">
          <div className="text-[0.6rem] font-bold text-muted tracking-[1.4px] uppercase">
            Collaborate
          </div>
        </div>
        <button
          onClick={onStudyRooms}
          className={`w-full flex items-center gap-2.5 px-3 py-[7px] rounded-lg text-[0.84rem] transition-all group ${
            currentView === "rooms"
              ? "bg-purple-dim text-purple font-semibold"
              : "text-text2 hover:bg-s2 hover:text-text"
          }`}
        >
          <Users size={16} />
          <span className="flex-1 text-left">Study Rooms</span>
          <ChevronRight
            size={14}
            className="opacity-0 group-hover:opacity-50 transition-opacity"
          />
        </button>
      </nav>

      <div className="h-px bg-b1 mx-4" />

      {/* ── Focus Timer ─────────────────────── */}
      <FocusTimer />

      <div className="h-px bg-b1 mx-4" />

      {/* ── Footer ──────────────────────────── */}
      <div className="px-4 py-3 text-center text-[0.6rem] text-muted">
        v2.0 · Student Copilot AI
      </div>
    </aside>
  );
}
