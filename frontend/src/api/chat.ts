const API_URL = (import.meta.env['VITE_API_URL'] as string | undefined) ?? "http://localhost:8000";

export type ChatResponse = { answer: string };

export async function askCandidate(question: string, signal?: AbortSignal): Promise<string> {
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
    signal: signal ?? null,
  });

  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`);
  }

  const data = (await res.json()) as Partial<ChatResponse>;
  if (typeof data.answer !== "string") {
    throw new Error("Unexpected response from the interview service.");
  }
  return data.answer;
}

export async function askCandidateStream(
  question: string,
  onChunk: (chunk: string) => void,
  signal?: AbortSignal
): Promise<void> {
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
    signal: signal ?? null,
  });

  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`);
  }

  if (!res.body) {
    throw new Error("Response body is null");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;
      const dataStr = trimmed.slice(5).trim();
      if (dataStr === "[DONE]") {
        return;
      }
      try {
        const parsed = JSON.parse(dataStr) as { content?: string };
        if (parsed.content) {
          onChunk(parsed.content);
        }
      } catch {
        // Skip malformed line
      }
    }
  }
}

