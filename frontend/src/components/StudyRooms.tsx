"use client";

import { useState } from "react";
import { ArrowLeft, Send, Users, Hash, Plus, LogIn } from "lucide-react";

interface Room {
  name: string;
  code: string;
  creator: string;
  participants: string[];
  messages: { sender: string; text: string; time: string }[];
}

interface StudyRoomsProps {
  userName: string;
  onBack: () => void;
}

function generateCode(): string {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
}

export default function StudyRooms({ userName, onBack }: StudyRoomsProps) {
  const [rooms, setRooms] = useState<Record<string, Room>>({});
  const [currentRoom, setCurrentRoom] = useState<string | null>(null);
  const [roomName, setRoomName] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [chatInput, setChatInput] = useState("");
  const [error, setError] = useState("");

  const createRoom = () => {
    if (!roomName.trim()) return;
    const code = generateCode();
    const room: Room = {
      name: roomName,
      code,
      creator: userName || "Anonymous",
      participants: [userName || "Anonymous"],
      messages: [],
    };
    setRooms((prev) => ({ ...prev, [code]: room }));
    setCurrentRoom(code);
    setRoomName("");
    setError("");
  };

  const joinRoom = () => {
    const code = joinCode.toUpperCase().trim();
    if (!code) return;
    if (rooms[code]) {
      const room = rooms[code];
      if (!room.participants.includes(userName || "Anonymous")) {
        room.participants.push(userName || "Anonymous");
      }
      setCurrentRoom(code);
      setJoinCode("");
      setError("");
    } else {
      setError("Room not found. Check the code and try again.");
    }
  };

  const leaveRoom = () => {
    if (currentRoom && rooms[currentRoom]) {
      const room = rooms[currentRoom];
      room.participants = room.participants.filter(
        (p) => p !== (userName || "Anonymous")
      );
    }
    setCurrentRoom(null);
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || !currentRoom) return;
    const room = rooms[currentRoom];
    room.messages.push({
      sender: userName || "Anonymous",
      text: chatInput,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    });
    setRooms({ ...rooms });
    setChatInput("");
  };

  // ── Active Room View ────────────────────
  if (currentRoom && rooms[currentRoom]) {
    const room = rooms[currentRoom];
    return (
      <div className="flex flex-col h-[calc(100vh-32px)] animate-fade-up">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-b1">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-teal animate-pulse" />
            <h2 className="text-lg font-bold text-text">{room.name}</h2>
            <span className="font-mono text-xs px-2 py-0.5 rounded-md bg-purple-dim text-purple border border-purple/20">
              {room.code}
            </span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onBack}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-s1 border border-b1 text-text2 text-[0.82rem] hover:bg-s2 hover:text-text transition-all"
            >
              <ArrowLeft size={14} />
              Dashboard
            </button>
            <button
              onClick={leaveRoom}
              className="px-3 py-1.5 rounded-lg bg-coral-dim border border-coral/20 text-coral text-[0.82rem] hover:bg-coral/20 transition-all"
            >
              Leave Space
            </button>
          </div>
        </div>

        <div className="grid grid-cols-[1fr_320px] gap-4 flex-1 min-h-0">
          {/* Main — Participants */}
          <div className="flex flex-col">
            <div className="text-[0.65rem] font-bold text-muted tracking-[1.2px] uppercase mb-3">
              <Users size={13} className="inline mr-1" />
              Participants ({room.participants.length})
            </div>
            <div className="grid grid-cols-3 gap-3 mb-4">
              {room.participants.map((p) => (
                <div
                  key={p}
                  className="glass rounded-xl p-4 flex flex-col items-center justify-center gap-2"
                >
                  <div className="w-12 h-12 rounded-full bg-purple-dim flex items-center justify-center text-lg font-bold text-purple">
                    {p.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-[0.82rem] text-text font-medium">
                    {p}
                  </span>
                  <span className="text-[0.6rem] text-teal font-semibold uppercase tracking-wide">
                    Online
                  </span>
                </div>
              ))}
            </div>

            {/* Shared Space placeholder */}
            <div className="flex-1 glass rounded-xl flex items-center justify-center">
              <div className="text-center text-muted">
                <div className="text-3xl mb-2">📋</div>
                <div className="text-sm font-medium">Shared Workspace</div>
                <div className="text-xs mt-1">
                  Collaborative notes coming soon
                </div>
              </div>
            </div>
          </div>

          {/* Chat */}
          <div className="flex flex-col glass rounded-xl overflow-hidden">
            <div className="px-4 py-3 border-b border-b1 text-[0.78rem] font-bold text-text">
              💬 Room Chat
            </div>
            <div className="flex-1 overflow-y-auto p-3 space-y-2">
              {room.messages.length === 0 && (
                <div className="text-center text-muted text-xs py-8">
                  No messages yet. Say hi! 👋
                </div>
              )}
              {room.messages.map((msg, i) => (
                <div
                  key={i}
                  className="bg-[rgba(255,255,255,0.02)] rounded-lg p-2.5 border-l-2 border-purple"
                >
                  <div className="flex items-center justify-between mb-0.5">
                    <span className="text-[0.75rem] font-semibold text-purple">
                      {msg.sender}
                    </span>
                    <span className="text-[0.6rem] text-muted">
                      {msg.time}
                    </span>
                  </div>
                  <p className="text-[0.82rem] text-text2 m-0">{msg.text}</p>
                </div>
              ))}
            </div>
            <form
              onSubmit={sendMessage}
              className="p-2 border-t border-b1 flex gap-2"
            >
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Send a message…"
                className="flex-1 bg-s1 border border-b1 rounded-lg px-3 py-2 text-[0.82rem] text-text placeholder:text-muted/50 outline-none focus:border-purple transition-all"
              />
              <button
                type="submit"
                className="w-9 h-9 rounded-lg bg-purple flex items-center justify-center text-white hover:bg-purple/80 transition-all"
              >
                <Send size={14} />
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  // ── Lobby View ──────────────────────────
  return (
    <div className="animate-fade-up">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-extrabold text-text">Study Rooms</h1>
          <p className="text-text2 text-[0.88rem] mt-1">
            Collaborative spaces for focused group learning
          </p>
        </div>
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-s1 border border-b1 text-text2 text-[0.82rem] hover:bg-s2 hover:text-text transition-all"
        >
          <ArrowLeft size={14} />
          Dashboard
        </button>
      </div>

      {!userName && (
        <div className="glass rounded-xl p-4 mb-6 text-center text-text2 text-sm">
          👋 Enter your name in the sidebar to create or join rooms.
        </div>
      )}

      {/* Create / Join */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        {/* Create */}
        <div className="glass rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-9 h-9 rounded-xl bg-purple-dim flex items-center justify-center">
              <Plus size={18} className="text-purple" />
            </div>
            <div>
              <div className="text-[0.92rem] font-bold text-text">
                Create Room
              </div>
              <div className="text-[0.72rem] text-muted">
                Start a new space
              </div>
            </div>
          </div>
          <input
            type="text"
            value={roomName}
            onChange={(e) => setRoomName(e.target.value)}
            placeholder="e.g., Physics Deep-Dive"
            className="w-full bg-s1 border border-b1 rounded-lg px-3 py-2.5 text-[0.84rem] text-text placeholder:text-muted/50 outline-none focus:border-purple mb-3 transition-all"
            onKeyDown={(e) => e.key === "Enter" && createRoom()}
          />
          <button
            onClick={createRoom}
            disabled={!userName || !roomName.trim()}
            className="w-full py-2.5 rounded-lg bg-purple text-white text-[0.84rem] font-semibold hover:bg-purple/80 disabled:bg-s2 disabled:text-muted transition-all"
          >
            Create Space
          </button>
        </div>

        {/* Join */}
        <div className="glass rounded-xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-9 h-9 rounded-xl bg-teal-dim flex items-center justify-center">
              <LogIn size={18} className="text-teal" />
            </div>
            <div>
              <div className="text-[0.92rem] font-bold text-text">
                Join Room
              </div>
              <div className="text-[0.72rem] text-muted">
                Enter a 6-character code
              </div>
            </div>
          </div>
          <input
            type="text"
            value={joinCode}
            onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
            placeholder="Room code…"
            maxLength={6}
            className="w-full bg-s1 border border-b1 rounded-lg px-3 py-2.5 text-[0.84rem] text-text placeholder:text-muted/50 outline-none focus:border-teal mb-3 font-mono tracking-wider transition-all"
            onKeyDown={(e) => e.key === "Enter" && joinRoom()}
          />
          {error && (
            <div className="text-[0.75rem] text-coral mb-2">{error}</div>
          )}
          <button
            onClick={joinRoom}
            disabled={!userName || !joinCode.trim()}
            className="w-full py-2.5 rounded-lg bg-teal text-white text-[0.84rem] font-semibold hover:bg-teal/80 disabled:bg-s2 disabled:text-muted transition-all"
          >
            Join Space
          </button>
        </div>
      </div>

      {/* Active Rooms */}
      {Object.keys(rooms).length > 0 && (
        <div>
          <div className="text-[0.65rem] font-bold text-muted tracking-[1.2px] uppercase mb-3">
            <Hash size={13} className="inline mr-1" />
            Active Spaces
          </div>
          <div className="space-y-2">
            {Object.entries(rooms).map(([code, room]) => (
              <div
                key={code}
                className="glass rounded-xl p-4 flex items-center justify-between hover:border-b2 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-teal animate-pulse" />
                  <div>
                    <span className="text-[0.88rem] font-semibold text-text">
                      {room.name}
                    </span>
                    <span className="ml-2 font-mono text-[0.7rem] text-purple bg-purple-dim px-1.5 py-0.5 rounded">
                      {code}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-[0.75rem] text-text2">
                    {room.participants.length} online
                  </span>
                  <button
                    onClick={() => {
                      const r = rooms[code];
                      if (
                        !r.participants.includes(userName || "Anonymous")
                      ) {
                        r.participants.push(userName || "Anonymous");
                      }
                      setCurrentRoom(code);
                    }}
                    className="px-3 py-1.5 rounded-lg bg-s2 border border-b1 text-[0.78rem] text-text2 hover:text-text hover:bg-s3 transition-all"
                  >
                    Enter →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
