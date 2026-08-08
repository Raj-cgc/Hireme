import { createFileRoute } from "@tanstack/react-router";
import { Hero } from "@/components/Hero";
import { candidate } from "@/data/candidate";

const title = `${candidate.name} — Interview an AI trained on their resume | HireMeAI`;
const description = `Ask an AI representation of ${candidate.name}, ${candidate.title}, about skills, experience and projects. Answers are grounded strictly in the resume.`;

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <main>
      <Hero />
      <section className="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-semibold sm:text-3xl">How the interview works</h2>
        <div className="mt-8 grid gap-5 sm:grid-cols-3">
          {[
            {
              step: "01",
              title: "Resume parsed",
              body: "The resume is converted into a structured profile: skills, roles, education, projects.",
            },
            {
              step: "02",
              title: "You ask anything",
              body: "Type recruiter questions in plain language, or start from suggested prompts.",
            },
            {
              step: "03",
              title: "Grounded answers",
              body: "The AI answers only from the resume, and says so clearly when data is missing.",
            },
          ].map((c) => (
            <article key={c.step} className="panel p-5">
              <span className="font-display text-sm text-primary">{c.step}</span>
              <h3 className="mt-2 text-base font-semibold">{c.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{c.body}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
