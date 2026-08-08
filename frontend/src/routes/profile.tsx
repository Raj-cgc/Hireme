import { createFileRoute, Link } from "@tanstack/react-router";
import { ExperienceTimeline } from "@/components/ExperienceTimeline";
import { candidate } from "@/data/candidate";

const title = `${candidate.name} — Candidate Profile | HireMeAI`;
const description = `Skills, experience timeline, education, projects, and certifications for ${candidate.name}, ${candidate.title}.`;

export const Route = createFileRoute("/profile")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
    ],
  }),
  component: ProfilePage,
});

function Section({ heading, children }: { heading: string; children: React.ReactNode }) {
  return (
    <section className="panel p-5 sm:p-7">
      <h2 className="text-lg font-semibold sm:text-xl">{heading}</h2>
      <div className="mt-5">{children}</div>
    </section>
  );
}

function ProfilePage() {
  return (
    <main className="mx-auto w-full max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
      <header className="mb-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs tracking-widest text-primary uppercase font-semibold">
              ✓ Verified Resume Profile
            </p>
            <h1 className="mt-2 text-3xl font-semibold sm:text-4xl">{candidate.name}</h1>
            <p className="mt-2 text-muted-foreground">
              {candidate.title} · {candidate.location}
            </p>
          </div>
          <Link
            to="/chat"
            className="inline-flex rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground transition-transform hover:-translate-y-0.5"
          >
            Ask Candidate AI
          </Link>
        </div>

        <p className="mt-4 max-w-3xl text-sm leading-relaxed text-muted-foreground">
          {candidate.summary}
        </p>

        {/* Contact & Social Links */}
        <div className="mt-6 flex flex-wrap gap-3 text-xs">
          {candidate.email && (
            <a
              href={`mailto:${candidate.email}`}
              className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface-raised px-3 py-1.5 font-medium text-foreground transition-colors hover:border-primary/50"
            >
              ✉️ {candidate.email}
            </a>
          )}
          {candidate.phone && (
            <a
              href={`tel:${candidate.phone}`}
              className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface-raised px-3 py-1.5 font-medium text-foreground transition-colors hover:border-primary/50"
            >
              📞 {candidate.phone}
            </a>
          )}
          {candidate.linkedin && (
            <a
              href={candidate.linkedin}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface-raised px-3 py-1.5 font-medium text-foreground transition-colors hover:border-primary/50"
            >
              🔗 LinkedIn
            </a>
          )}
          {candidate.github && (
            <a
              href={candidate.github}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-surface-raised px-3 py-1.5 font-medium text-foreground transition-colors hover:border-primary/50"
            >
              💻 GitHub
            </a>
          )}
        </div>
      </header>

      <div className="space-y-6">
        <Section heading="Technical Skills">
          <ul className="flex flex-wrap gap-2">
            {candidate.skills.map((s) => (
              <li
                key={s}
                className="rounded-full border border-border bg-surface-raised px-3.5 py-1.5 text-sm font-medium text-foreground"
              >
                {s}
              </li>
            ))}
          </ul>
        </Section>

        <Section heading="Experience">
          <ExperienceTimeline />
        </Section>

        <Section heading="Projects">
          <div className="grid gap-4 sm:grid-cols-2">
            {candidate.projects.map((p) => (
              <article key={p.name} className="rounded-xl border border-border/60 bg-surface-raised p-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-semibold">{p.name}</h3>
                  {p.github && (
                    <a
                      href={p.github}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-primary hover:underline"
                    >
                      GitHub ↗
                    </a>
                  )}
                </div>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {p.description}
                </p>
                <ul className="mt-4 flex flex-wrap gap-2">
                  {p.tags.map((t) => (
                    <li key={t} className="rounded-md bg-primary/10 px-2.5 py-1 text-[11px] font-medium text-primary">
                      {t}
                    </li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </Section>

        <Section heading="Education">
          <ul className="space-y-4">
            {candidate.education.map((e) => (
              <li key={e.institution} className="rounded-xl border border-border/50 bg-surface-raised p-4">
                <p className="text-base font-medium">{e.institution}</p>
                <p className="mt-1 text-sm text-muted-foreground">{e.detail}</p>
              </li>
            ))}
          </ul>
        </Section>

        <Section heading="Achievements & Certifications">
          <ul className="grid gap-3 sm:grid-cols-2">
            {candidate.certifications.map((c) => (
              <li
                key={c}
                className="flex items-center gap-2.5 rounded-xl border border-border/50 bg-surface-raised p-3.5 text-sm text-foreground"
              >
                <span className="text-primary font-bold">🏆</span>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </Section>
      </div>
    </main>
  );
}
