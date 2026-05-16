"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Play, Pause, RotateCcw } from "lucide-react";

const DURATIONS = [
  { label: "25m", seconds: 25 * 60, color: "#7c6fe0" },
  { label: "5m", seconds: 5 * 60, color: "#1fc8a0" },
  { label: "15m", seconds: 15 * 60, color: "#f0a030" },
];

export default function FocusTimer() {
  const [durationIdx, setDurationIdx] = useState(0);
  const [timeLeft, setTimeLeft] = useState(DURATIONS[0].seconds);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const dur = DURATIONS[durationIdx];

  const tick = useCallback(() => {
    setTimeLeft((prev) => {
      if (prev <= 1) {
        setIsRunning(false);
        return 0;
      }
      return prev - 1;
    });
  }, []);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(tick, 1000);
    } else if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isRunning, tick]);

  const toggle = () => {
    if (timeLeft <= 0) {
      setTimeLeft(dur.seconds);
    }
    setIsRunning((prev) => !prev);
  };

  const reset = () => {
    setIsRunning(false);
    setTimeLeft(dur.seconds);
  };

  const switchDuration = (idx: number) => {
    setIsRunning(false);
    setDurationIdx(idx);
    setTimeLeft(DURATIONS[idx].seconds);
  };

  const mins = Math.floor(timeLeft / 60)
    .toString()
    .padStart(2, "0");
  const secs = (timeLeft % 60).toString().padStart(2, "0");
  const progress = dur.seconds > 0 ? (timeLeft / dur.seconds) * 100 : 0;
  const circumference = 2 * Math.PI * 42;
  const dashOffset = ((100 - progress) / 100) * circumference;
  const activeColor = isRunning ? dur.color : "#555";

  return (
    <div className="px-4 py-2">
      <div className="text-[0.6rem] font-bold text-muted tracking-[1.4px] uppercase mb-3">
        Focus Timer
      </div>

      {/* Duration pills */}
      <div className="flex gap-1 mb-3 bg-[rgba(255,255,255,0.02)] rounded-full p-1 border border-b1">
        {DURATIONS.map((d, i) => (
          <button
            key={d.label}
            onClick={() => switchDuration(i)}
            className={`flex-1 text-[0.72rem] font-semibold py-1 rounded-full transition-all ${
              i === durationIdx
                ? "bg-purple text-white"
                : "text-muted hover:text-text2"
            }`}
          >
            {d.label}
          </button>
        ))}
      </div>

      {/* Ring */}
      <div className="flex justify-center mb-3">
        <div className="relative w-[110px] h-[110px]">
          <svg
            className="w-full h-full -rotate-90"
            viewBox="0 0 100 100"
          >
            <circle
              cx="50"
              cy="50"
              r="42"
              fill="none"
              stroke="rgba(255,255,255,0.04)"
              strokeWidth="5"
            />
            <circle
              cx="50"
              cy="50"
              r="42"
              fill="none"
              stroke={activeColor}
              strokeWidth="5"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={dashOffset}
              className="transition-all duration-1000 ease-linear"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-[1.6rem] font-extrabold text-text tracking-tight leading-none">
              {mins}:{secs}
            </span>
            <span
              className="text-[0.55rem] font-bold uppercase tracking-[1.5px] mt-1"
              style={{ color: activeColor }}
            >
              {timeLeft === 0
                ? "DONE"
                : isRunning
                  ? "ACTIVE"
                  : "PAUSED"}
            </span>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex gap-2">
        <button
          onClick={toggle}
          className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-s1 border border-b1 text-text2 text-[0.75rem] font-medium hover:bg-s2 hover:text-text transition-all"
        >
          {isRunning ? <Pause size={13} /> : <Play size={13} />}
          {isRunning ? "Pause" : "Start"}
        </button>
        <button
          onClick={reset}
          className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-s1 border border-b1 text-text2 text-[0.75rem] font-medium hover:bg-s2 hover:text-text transition-all"
        >
          <RotateCcw size={13} />
          Reset
        </button>
      </div>
    </div>
  );
}
