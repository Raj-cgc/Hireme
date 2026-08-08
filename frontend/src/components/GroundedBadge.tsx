export function GroundedBadge({ className = "" }: { className?: string }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-2.5 py-1 text-[11px] font-medium tracking-wide text-primary ${className}`}
    >
      <span aria-hidden="true">✓</span>
      Resume-grounded AI
    </span>
  );
}
