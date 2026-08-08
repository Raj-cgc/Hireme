import { candidate } from "@/data/candidate";

export function ExperienceTimeline() {
  return (
    <ol className="relative space-y-6 border-l border-border pl-6">
      {candidate.experience.map((job) => (
        <li key={`${job.company}-${job.role}`} className="relative">
          <span
            aria-hidden="true"
            className="absolute top-1.5 -left-[31px] size-2.5 rounded-full bg-primary ring-4 ring-background"
          />
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 className="text-base font-semibold">{job.role}</h3>
            <span className="text-xs text-muted-foreground">{job.duration}</span>
          </div>
          <p className="text-sm text-primary">{job.company}</p>
          <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{job.description}</p>
          <ul className="mt-3 flex flex-wrap gap-2">
            {job.skills.map((s) => (
              <li
                key={s}
                className="rounded-md bg-surface-raised px-2 py-1 text-[11px] text-muted-foreground"
              >
                {s}
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ol>
  );
}
