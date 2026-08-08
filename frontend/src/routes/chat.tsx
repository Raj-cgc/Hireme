import { createFileRoute } from "@tanstack/react-router";
import { ChatRoom } from "@/components/ChatRoom";
import { candidate } from "@/data/candidate";

const title = `Interview ${candidate.name}'s AI | HireMeAI`;
const description = `Ask questions and get resume-grounded answers about ${candidate.name}'s skills, experience and projects.`;

export const Route = createFileRoute("/chat")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: ChatPage,
});

function ChatPage() {
  return <ChatRoom />;
}
