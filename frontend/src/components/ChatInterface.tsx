"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { type ToolId, getToolById } from "@/lib/utils";
import { sendPrompt, logActivity, type ChatMessage } from "@/lib/api";
import { ArrowLeft, Trash2, Copy, Check, Loader2, Paperclip, X, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatInterfaceProps {
  toolId: ToolId;
  apiChoice: string;
  answerStyle: string;
  pendingPrompt?: string | null;
  onBack: () => void;
}

const LANDING_DATA: Record<
  string,
  { headline: string; sub: string; chips: string[] }
> = {
  explainer: {
    headline: "What do you want to understand?",
    sub: "Get structured explanations with analogies, examples, and diagrams.",
    chips: [
      "Explain recursion with examples",
      "How does TCP/IP work?",
      "What is normalization in DBMS?",
      "Explain Big O notation simply",
    ],
  },
  visualizer: {
    headline: "What should we visualize?",
    sub: "Generate interactive Mermaid.js diagrams for any concept.",
    chips: [
      "TCP/IP protocol layers",
      "Binary search tree operations",
      "React component lifecycle",
      "Database normalization forms",
    ],
  },
  flashcards: {
    headline: "Flash review — pick a topic",
    sub: "AI-generated flashcards you can flip to test yourself.",
    chips: [
      "Data structures basics",
      "Operating system concepts",
      "JavaScript closures",
      "SQL query fundamentals",
    ],
  },
  quizzer: {
    headline: "Ready to test your knowledge?",
    sub: "Generate quizzes with MCQs, true/false, and short answers.",
    chips: [
      "Quiz me on OOP concepts",
      "DBMS exam questions",
      "Network protocols quiz",
      "Algorithm complexity test",
    ],
  },
  interview: {
    headline: "Prepare for your next interview",
    sub: "Get role-specific questions with ideal answers and tips.",
    chips: [
      "Frontend developer at Google",
      "Full-stack SDE interview",
      "Data science behavioral round",
      "System design questions",
    ],
  },
  resume: {
    headline: "Get your resume reviewed",
    sub: "AI-powered ATS scoring, critique, and improvement suggestions.",
    chips: [
      "Review my SDE resume",
      "Improve my project descriptions",
      "How to quantify my achievements?",
      "ATS optimization tips",
    ],
  },
};

export default function ChatInterface({
  toolId,
  apiChoice,
  answerStyle,
  pendingPrompt,
  onBack,
}: ChatInterfaceProps) {
  const tool = getToolById(toolId);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);
  const [pdfText, setPdfText] = useState<string | null>(null);
  const [pdfName, setPdfName] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const processedPending = useRef(false);

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = useCallback(
    async (prompt: string) => {
      if (!prompt.trim() || isLoading) return;

      const userMsg: ChatMessage = {
        role: "user",
        content: prompt,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const chatHistory = messages
          .slice(-6)
          .map((m) => `${m.role}: ${m.content}`)
          .join("\n");
        const context = pdfText
          ? `[Attached PDF Content]:\n${pdfText.slice(0, 4000)}\n\n[Chat History]:\n${chatHistory}`
          : chatHistory;
        const response = await sendPrompt(
          toolId,
          prompt,
          context,
          answerStyle,
          apiChoice
        );
        logActivity(toolId, prompt);

        const assistantMsg: ChatMessage = {
          role: "assistant",
          content: response,
          timestamp: Date.now(),
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } catch (err) {
        const errorMsg: ChatMessage = {
          role: "assistant",
          content: `❌ Error: ${err instanceof Error ? err.message : "Something went wrong"}. Make sure the backend is running on port 8000.`,
          timestamp: Date.now(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [apiChoice, answerStyle, isLoading, messages, toolId]
  );

  // Handle pending prompt from Quick Ask
  useEffect(() => {
    if (pendingPrompt && !processedPending.current) {
      processedPending.current = true;
      handleSend(pendingPrompt);
    }
  }, [pendingPrompt, handleSend]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    handleSend(input);
    setInput("");
  };

  const handleCopy = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  const landing = LANDING_DATA[toolId];

  if (!tool) return null;

  return (
    <div className="flex flex-col h-[calc(100vh-32px)] animate-fade-up">
      {/* ── Header ─────────────────────────────── */}
      <div className="flex items-center justify-between pb-4 mb-2 border-b border-b1">
        <div className="flex items-center gap-2">
          <span className="text-xl">{tool.icon}</span>
          <h2 className="text-lg font-bold text-text">{tool.label}</h2>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onBack}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-s1 border border-b1 text-text2 text-[0.82rem] hover:bg-s2 hover:text-text transition-all"
          >
            <ArrowLeft size={14} />
            Dashboard
          </button>
          <button
            onClick={() => setMessages([])}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-s1 border border-b1 text-text2 text-[0.82rem] hover:bg-s2 hover:text-text transition-all"
          >
            <Trash2 size={14} />
            Clear
          </button>
        </div>
      </div>

      {/* ── Messages ───────────────────────────── */}
      <div className="flex-1 overflow-y-auto pr-2">
        {messages.length === 0 && !isLoading && landing ? (
          /* Landing Screen */
          <div className="flex flex-col items-center justify-center h-full text-center animate-fade-in">
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-5"
              style={{ background: `${tool.color}18` }}
            >
              {tool.icon}
            </div>
            <h3 className="text-2xl font-extrabold text-text mb-2">
              {landing.headline}
            </h3>
            <p className="text-muted text-[0.88rem] mb-8 max-w-md">
              {landing.sub}
            </p>
            <div className="grid grid-cols-2 gap-3 w-full max-w-lg">
              {landing.chips.map((chip) => (
                <button
                  key={chip}
                  onClick={() => {
                    setInput("");
                    handleSend(chip);
                  }}
                  className="px-4 py-3 rounded-xl bg-s1 border border-b1 text-text2 text-[0.84rem] hover:border-purple hover:text-purple hover:bg-purple-dim transition-all text-left"
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>
        ) : (
          /* Chat Messages */
          <div className="space-y-4 py-4">
            {messages.map((msg, i) => (
              <div
                key={i}
                className="animate-fade-up"
                style={{ animationDelay: `${(i % 5) * 40}ms` }}
              >
                {msg.role === "user" ? (
                  <div className="flex justify-end">
                    <div className="max-w-[70%] px-4 py-3 rounded-2xl rounded-br-sm bg-purple/15 border border-purple/20 text-text text-[0.88rem]">
                      {msg.content}
                    </div>
                  </div>
                ) : (
                  <div className="glass rounded-2xl p-5 relative group">
                    <div className="flex items-center gap-1.5 mb-3 text-[0.65rem] font-bold text-muted tracking-[1px] uppercase">
                      <span
                        className="w-[5px] h-[5px] rounded-full"
                        style={{ background: tool.color }}
                      />
                      COPILOT · {tool.label}
                    </div>
                    <div className="prose-copilot">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                    <button
                      onClick={() => handleCopy(msg.content, i)}
                      className="absolute top-4 right-4 p-1.5 rounded-lg bg-s2 border border-b1 text-muted hover:text-purple opacity-0 group-hover:opacity-100 transition-all"
                      title="Copy response"
                    >
                      {copiedIdx === i ? (
                        <Check size={14} className="text-teal" />
                      ) : (
                        <Copy size={14} />
                      )}
                    </button>
                  </div>
                )}
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="glass rounded-2xl p-5 animate-fade-in">
                <div className="flex items-center gap-2 text-[0.65rem] font-bold text-muted tracking-[1px] uppercase mb-3">
                  <span
                    className="w-[5px] h-[5px] rounded-full animate-pulse"
                    style={{ background: tool.color }}
                  />
                  COPILOT · Thinking...
                </div>
                <div className="flex items-center gap-3 text-text2 text-sm">
                  <Loader2 size={18} className="animate-spin text-purple" />
                  <span>Generating response...</span>
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* ── PDF Attachment ──────────────────────── */}
      {pdfName && (
        <div className="mt-2 flex items-center gap-2 px-3 py-2 rounded-lg bg-s1 border border-b1 text-[0.78rem]">
          <FileText size={14} className="text-purple" />
          <span className="text-text2 flex-1 truncate">{pdfName}</span>
          <button
            onClick={() => { setPdfText(null); setPdfName(null); }}
            className="p-1 rounded hover:bg-s2 text-muted hover:text-coral transition-all"
          >
            <X size={14} />
          </button>
        </div>
      )}

      {/* ── Chat Input ─────────────────────────── */}
      <form
        onSubmit={handleSubmit}
        className="mt-2 glass rounded-2xl p-1 flex items-center gap-1"
      >
        {/* File upload */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (!file) return;
            setPdfName(file.name);
            const reader = new FileReader();
            reader.onload = (ev) => {
              const text = ev.target?.result as string;
              setPdfText(text);
            };
            reader.readAsText(file);
            e.target.value = "";
          }}
        />
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="w-9 h-9 ml-1 rounded-lg flex items-center justify-center text-muted hover:text-purple hover:bg-s2 transition-all"
          title="Attach file (PDF/TXT)"
        >
          <Paperclip size={16} />
        </button>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={pdfName ? `Ask about ${pdfName}...` : `Ask ${tool.label.toLowerCase()}...`}
          disabled={isLoading}
          className="flex-1 bg-transparent text-text text-[0.9rem] py-3 px-2 outline-none placeholder:text-muted/60 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="w-10 h-10 mr-1 rounded-xl bg-purple hover:bg-purple/80 disabled:bg-s2 disabled:text-muted flex items-center justify-center text-white transition-all"
        >
          {isLoading ? (
            <Loader2 size={18} className="animate-spin" />
          ) : (
            <ArrowLeft size={18} className="rotate-90" />
          )}
        </button>
      </form>
    </div>
  );
}
