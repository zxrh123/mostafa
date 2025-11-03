import { FormEvent, useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Send, Sparkles } from 'lucide-react';

import { connectRealtime, disconnectRealtime } from '../lib/realtime';
import { sendAICommand } from '../lib/api';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export function AIChatWidget() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: '??????! ??? ????? ???????. ?? ?? ?? ????? ??????? ??????? ????????.',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const socket = connectRealtime();
    if (!socket) return;

    socket.onmessage = (event) => {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'system',
          content: event.data,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    };

    return () => {
      disconnectRealtime();
    };
  }, []);

  useEffect(() => {
    const el = containerRef.current;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsSending(true);

    try {
      const response = await sendAICommand({
        conversation_id: 'dashboard',
        sender: 'operator',
        message: userMessage.content,
        context: { auto_execute: false }
      });

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `?????: ${response.intent}\n?????: ${(response.confidence * 100).toFixed(1)}%\n????????: ${response.generated_script ?? '?? ??? ??????? ???.'}`,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'system',
          content: '???? ??????? ?? ????? ???????. ???? ?? ??????? ???????.',
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45 }}
      className="glass-panel p-5 h-full flex flex-col"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="p-3 rounded-2xl bg-gradient-to-br from-neon/20 to-magenta/20">
            <Brain className="w-6 h-6 text-neon" />
          </span>
          <div>
            <p className="text-sm font-semibold text-white">????? ??????? ?????</p>
            <p className="text-xs text-white/60">??????? ????? ?? ???? ?? ?????</p>
          </div>
        </div>
        <motion.span
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="flex items-center gap-1 text-xs text-neon"
        >
          <Sparkles className="w-4 h-4" /> ??? ????
        </motion.span>
      </div>
      <div ref={containerRef} className="flex-1 overflow-y-auto space-y-3 pr-2">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`p-4 rounded-2xl whitespace-pre-line leading-relaxed border border-white/5 ${
              message.role === 'user'
                ? 'bg-magenta/20 self-end text-right'
                : message.role === 'assistant'
                ? 'bg-neon/10 text-left'
                : 'bg-black/30 text-white/70'
            }`}
          >
            <p className="text-xs text-white/50 mb-1">{message.timestamp}</p>
            <p className="text-sm text-white">{message.content}</p>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="mt-4 flex items-center gap-2">
        <input
          className="flex-1 bg-black/40 border border-white/10 rounded-2xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-neon/60"
          placeholder="???? ???? ??????? ???..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          disabled={isSending}
        />
        <button
          type="submit"
          disabled={isSending}
          className="px-4 py-3 rounded-2xl bg-gradient-to-r from-neon to-magenta text-sm font-semibold text-black flex items-center gap-2 disabled:opacity-50"
        >
          ?????
          <Send className="w-4 h-4" />
        </button>
      </form>
    </motion.div>
  );
}
