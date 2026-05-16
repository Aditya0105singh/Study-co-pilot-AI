"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/components/Dashboard";
import ChatInterface from "@/components/ChatInterface";
import StudyRooms from "@/components/StudyRooms";
import { type ToolId } from "@/lib/utils";

type ViewMode = "dashboard" | "tool" | "rooms";

export default function Home() {
  const [viewMode, setViewMode] = useState<ViewMode>("dashboard");
  const [currentTool, setCurrentTool] = useState<ToolId | null>(null);
  const [userName, setUserName] = useState("");
  const [apiChoice] = useState("Gemini");
  const [answerStyle] = useState("Beginner Friendly");
  const [pendingPrompt, setPendingPrompt] = useState<string | null>(null);

  // Load name from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("copilot_name");
    if (saved) setUserName(saved);
  }, []);

  const handleNameChange = (name: string) => {
    setUserName(name);
    localStorage.setItem("copilot_name", name);
  };

  const handleNavigate = (tool: ToolId | null) => {
    if (tool === null) {
      setViewMode("dashboard");
      setCurrentTool(null);
    } else {
      setViewMode("tool");
      setCurrentTool(tool);
    }
    setPendingPrompt(null);
  };

  const handleQuickAsk = (prompt: string, tool: ToolId) => {
    setPendingPrompt(prompt);
    setCurrentTool(tool);
    setViewMode("tool");
  };

  const handleStudyRooms = () => {
    setViewMode("rooms");
    setCurrentTool(null);
    setPendingPrompt(null);
  };

  return (
    <div className="flex min-h-screen relative z-10">
      <Sidebar
        currentTool={currentTool}
        currentView={viewMode}
        onNavigate={handleNavigate}
        onStudyRooms={handleStudyRooms}
        userName={userName}
        onNameChange={handleNameChange}
        apiChoice={apiChoice}
      />

      <main className="ml-[260px] flex-1 p-6 lg:p-8 min-h-screen">
        {viewMode === "dashboard" && (
          <Dashboard
            userName={userName}
            apiChoice={apiChoice}
            onToolSelect={(tool) => handleNavigate(tool)}
            onQuickAsk={handleQuickAsk}
          />
        )}
        {viewMode === "tool" && currentTool && (
          <ChatInterface
            key={currentTool + (pendingPrompt || "")}
            toolId={currentTool}
            apiChoice={apiChoice}
            answerStyle={answerStyle}
            pendingPrompt={pendingPrompt}
            onBack={() => handleNavigate(null)}
          />
        )}
        {viewMode === "rooms" && (
          <StudyRooms
            userName={userName}
            onBack={() => handleNavigate(null)}
          />
        )}
      </main>
    </div>
  );
}
