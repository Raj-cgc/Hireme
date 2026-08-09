import { Link } from "@tanstack/react-router";
import { candidate } from "@/data/candidate";
import { GroundedBadge } from "./GroundedBadge";

export function Hero() {
  return (
    <section className="hero-glow relative overflow-hidden border-b border-border">
      <div className="mx-auto grid w-full max-w-6xl gap-12 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
        <div className="animate-rise">
          <GroundedBadge />
          <h1 className="mt-5 text-4xl leading-[1.08] font-semibold sm:text-5xl lg:text-6xl">
            Hi ! I am {candidate.name}&apos;s AI portfolio assistant.
            <br />
            <span className="text-primary">Ask me anything.</span>
          </h1>
          <p className="mt-5 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            {candidate.tagline} Interview an AI trained strictly on {candidate.name}'s resume —
            no guesswork, no filler, just verifiable answers.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              to="/chat"
              className="shadow-accent inline-flex items-center justify-center rounded-xl bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-transform hover:-translate-y-0.5"
            >
              Talk to Candidate AI
            </Link>
            <Link
              to="/profile"
              className="inline-flex items-center justify-center rounded-xl border border-border px-6 py-3 text-sm font-medium text-foreground transition-colors hover:bg-secondary"
            >
              View full profile
            </Link>
          </div>

          <dl className="mt-10 grid max-w-lg grid-cols-1 gap-4 sm:grid-cols-3">
            {candidate.highlights.map((h) => (
              <div key={h.label} className="panel px-4 py-3">
                <dt className="text-[11px] tracking-widest text-muted-foreground uppercase">
                  {h.label}
                </dt>
                <dd className="mt-1 text-sm font-medium">{h.value}</dd>
              </div>
            ))}
          </dl>
        </div>

        <div className="panel shadow-elevated animate-rise p-5 sm:p-6">
          <div className="flex items-center gap-3 border-b border-border pb-4">
            <span className="grid size-11 place-items-center rounded-full bg-primary/15 font-display text-lg font-semibold text-primary">
              {candidate.name.charAt(0)}
            </span>
            <div>
              <p className="font-display text-base font-semibold">{candidate.name}</p>
              <p className="text-xs text-muted-foreground">
                {candidate.title} · {candidate.location}
              </p>
            </div>
          </div>
          <div className="mt-4 space-y-3 text-sm">
            <div className="rounded-xl bg-surface-raised px-4 py-3 text-muted-foreground">
              What are their strongest technical skills?
            </div>
            <div className="rounded-xl border border-primary/25 bg-primary/8 px-4 py-3 leading-relaxed">
              {candidate.summary}
            </div>
          </div>
          <p className="mt-4 text-xs text-muted-foreground">
            Answers come only from the parsed resume. Missing data is reported, never invented.
          </p>
        </div>
      </div>
    </section>
  );
}
