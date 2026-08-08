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
