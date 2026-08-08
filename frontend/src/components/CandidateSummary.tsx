import { candidate } from "@/data/candidate";
import { GroundedBadge } from "./GroundedBadge";

export function CandidateSummary() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <span className="grid size-12 place-items-center rounded-full bg-primary/15 font-display text-lg font-semibold text-primary">
          {candidate.name.charAt(0)}
        </span>
        <div>
          <p className="font-display text-base font-semibold">{candidate.name}</p>
          <p className="text-xs text-muted-foreground">
            {candidate.title} · {candidate.location}
          </p>
        </div>
      </div>

      <p className="text-sm leading-relaxed text-muted-foreground">{candidate.summary}</p>

      <div>
        <h3 className="text-[11px] tracking-widest text-muted-foreground uppercase">Core skills</h3>
        <ul className="mt-3 flex flex-wrap gap-2">
          {candidate.skills.slice(0, 8).map((s) => (
            <li
              key={s}
              className="rounded-full border border-border bg-surface-raised px-2.5 py-1 text-xs"
            >
              {s}
            </li>
          ))}
        </ul>
      </div>

      <GroundedBadge />
    </div>
  );
}
