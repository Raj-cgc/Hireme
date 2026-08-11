import { useEffect, useRef, useState } from "react";
import { askCandidateStream } from "@/api/chat";
import { candidate, suggestedQuestions } from "@/data/candidate";
import { CandidateSummary } from "./CandidateSummary";
import { GroundedBadge } from "./GroundedBadge";

type Message = { id: string; role: "user" | "ai"; text: string };

const newId = () => Math.random().toString(36).slice(2);

export function ChatRoom() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastQuestion, setLastQuestion] = useState<string | null>(null);
  const [summaryOpen, setSummaryOpen] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  async function send(question: string) {
    const q = question.trim();
    if (!q || loading) return;

    const aiMsgId = newId();
    setMessages((prev) => [
      ...prev,
      { id: newId(), role: "user", text: q },
      { id: aiMsgId, role: "ai", text: "" },
    ]);
    setInput("");
    setError(null);
    setLastQuestion(q);
    setLoading(true);

    try {
      await askCandidateStream(q, (chunk) => {
        setLoading(false);
        setMessages((prev) =>
          prev.map((m) => (m.id === aiMsgId ? { ...m, text: m.text + chunk } : m))
        );
      });
    } catch {
      setMessages((prev) => prev.filter((m) => m.id !== aiMsgId || m.text.length > 0));
      setError("Unable to connect. Please check that the backend is running.");
    } finally {
      setLoading(false);
      textareaRef.current?.focus();
    }
  }

  function retry() {
    if (lastQuestion) {
      setError(null);
      setMessages((prev) => prev.filter((m) => !(m.role === "user" && m.text === lastQuestion)));
      void send(lastQuestion);
    }
  }

  const empty = messages.length === 0 && !loading && !error;

  return (
    <main className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-4 py-6 sm:px-6 lg:flex-row lg:py-10">
      {/* Candidate summary: sidebar on desktop, collapsible on mobile */}
      <aside className="lg:w-72 lg:shrink-0">
        <div className="panel hidden p-5 lg:block">
          <CandidateSummary />
        </div>
        <div className="panel overflow-hidden lg:hidden">
          <button
            type="button"
            aria-expanded={summaryOpen}
            onClick={() => setSummaryOpen((o) => !o)}
            className="flex w-full items-center justify-between px-4 py-3 text-sm font-medium"
          >
            <span>
              {candidate.name} · {candidate.title}
            </span>
            <span aria-hidden="true" className="text-muted-foreground">
              {summaryOpen ? "−" : "+"}
            </span>
          </button>
          {summaryOpen && (
            <div className="border-t border-border p-4">
              <CandidateSummary />
            </div>
          )}
        </div>
      </aside>

      {/* Conversation */}
      <section className="panel flex min-h-[70vh] flex-1 flex-col lg:h-[calc(100vh-9rem)] lg:min-h-0">
        <header className="flex flex-wrap items-center justify-between gap-2 border-b border-border px-4 py-3 sm:px-5">
          <div>
            <h1 className="font-display text-sm font-semibold">AI Interview Room</h1>
            <p className="text-xs text-muted-foreground">
              Answers sourced from {candidate.name}'s resume
            </p>
          </div>
          <GroundedBadge />
        </header>

        <div
          className="flex-1 space-y-4 overflow-y-auto px-4 py-5 sm:px-5"
          role="log"
          aria-live="polite"
          aria-label="Interview conversation"
        >
          {empty && (
            <div className="animate-rise">
              <h2 className="text-lg font-semibold">Start the interview</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                Pick a question below, or ask your own.
              </p>
              <ul className="mt-4 grid gap-2 sm:grid-cols-2">
                {suggestedQuestions.map((q) => (
                  <li key={q}>
                    <button
                      type="button"
                      onClick={() => void send(q)}
                      className="w-full rounded-xl border border-border bg-surface-raised px-4 py-3 text-left text-sm transition-colors hover:border-primary/40 hover:text-primary"
                    >
                      {q}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {messages.map((m) => (
            <div
              key={m.id}
              className={`animate-rise flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={
                  m.role === "user"
                    ? "max-w-[85%] rounded-2xl rounded-br-md bg-primary px-4 py-2.5 text-sm text-primary-foreground"
                    : "max-w-[90%] rounded-2xl rounded-bl-md border border-border bg-surface-raised px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap"
                }
              >
                {m.role === "ai" && (
                  <p className="mb-1 text-[11px] tracking-widest text-primary uppercase">
                    Candidate AI
                  </p>
                )}
                {m.role === "ai" && m.text.length === 0 ? (
                  <span className="inline-flex items-center gap-1 py-1 text-muted-foreground">
                    <span className="thinking-dot size-1.5 rounded-full bg-primary" />
                    <span
                      className="thinking-dot size-1.5 rounded-full bg-primary"
                      style={{ animationDelay: "0.15s" }}
                    />
                    <span
                      className="thinking-dot size-1.5 rounded-full bg-primary"
                      style={{ animationDelay: "0.3s" }}
                    />
                  </span>
                ) : (
                  m.text
                )}
              </div>
            </div>
          ))}

          {error && (
            <div
              role="alert"
              className="rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm"
            >
              <p>{error}</p>
              <button
                type="button"
                onClick={retry}
                className="mt-3 rounded-lg border border-border px-3 py-1.5 text-xs font-medium transition-colors hover:bg-secondary"
              >
                Retry
              </button>
            </div>
          )}

          <div ref={endRef} />
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            void send(input);
          }}
          className="border-t border-border p-3 sm:p-4"
        >
          <div className="flex items-end gap-2 rounded-xl border border-border bg-surface-raised p-2 focus-within:border-primary/50">
            <label htmlFor="question" className="sr-only">
              Ask the candidate AI a question
            </label>
            <textarea
              id="question"
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  void send(input);
                }
              }}
              placeholder="Ask about skills, experience, projects…"
              className="max-h-40 min-h-10 flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-muted-foreground"
            />
            <button
              type="submit"
              disabled={loading || input.trim().length === 0}
              className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition-opacity disabled:opacity-40"
            >
              Send
            </button>
          </div>
          <p className="mt-2 text-[11px] text-muted-foreground">
            Enter to send · Shift + Enter for a new line
          </p>
        </form>
      </section>
    </main>
  );
}
