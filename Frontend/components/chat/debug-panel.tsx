"use client";

import { useCallback, useState } from "react";
import { cn } from "@/lib/utils";

// One pipeline step as the backend records it (Backend/pipeline/trace.py).
// Input and output are plain text; the model's own reply is only shown when
// the step failed, to see what was wrong with it.
type TraceStep = {
  name: string;
  model?: string;
  ms?: number;
  input?: unknown;
  raw_output?: unknown;
  output?: unknown;
  error?: string;
  fallback?: boolean;
  // false when the model doesn't support JSON mode
  json_mode?: boolean;
  source?: string;
  skipped?: string;
};

type PipelineTrace = {
  steps?: TraceStep[];
  total_ms?: number;
};

function formatMs(ms?: number) {
  if (typeof ms !== "number") {
    return "";
  }
  return ms >= 1000 ? `${(ms / 1000).toFixed(1)} s` : `${ms} ms`;
}

function Chevron({ open }: { open: boolean }) {
  return (
    <span
      className={cn("inline-block transition-transform", open && "rotate-180")}
    >
      ▾
    </span>
  );
}

function CollapsibleSection({
  title,
  meta,
  failed = false,
  children,
}: {
  title: string;
  meta?: string;
  failed?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const toggle = useCallback(() => setOpen((v) => !v), []);

  return (
    <div className="overflow-hidden rounded-md border border-border/40 bg-background/60">
      <button
        className="flex w-full items-center justify-between px-2.5 py-1.5 text-left text-muted-foreground text-xs hover:text-foreground"
        onClick={toggle}
        type="button"
      >
        <span className="flex min-w-0 items-baseline gap-2">
          <span
            className={cn("truncate font-medium", failed && "text-red-400")}
          >
            {title}
          </span>
          {meta ? (
            <span className="shrink-0 text-[10px] text-muted-foreground/80">
              {meta}
            </span>
          ) : null}
        </span>
        <Chevron open={open} />
      </button>

      {open ? (
        <div className="space-y-2 border-border/40 border-t px-2.5 py-2">
          {children}
        </div>
      ) : null}
    </div>
  );
}

// Anything that isn't text already is written out as "key: value" lines
function toText(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }
  if (Array.isArray(value)) {
    return value.map(toText).join("\n");
  }
  if (value && typeof value === "object") {
    return Object.entries(value)
      .map(([key, item]) => `${key}: ${toText(item)}`)
      .join("\n");
  }
  return String(value);
}

function Value({ label, value }: { label: string; value: unknown }) {
  if (value === undefined || value === null || value === "") {
    return null;
  }

  return (
    <div>
      <div className="mb-0.5 font-medium text-[10px] text-muted-foreground/70 uppercase tracking-wide">
        {label}
      </div>
      <div className="max-h-64 overflow-auto whitespace-pre-wrap break-words rounded border border-border/40 bg-background/60 p-1.5 text-[11px] text-foreground/80 leading-relaxed">
        {toText(value)}
      </div>
    </div>
  );
}

function StepSection({ step }: { step: TraceStep }) {
  const meta = [
    step.model,
    step.source === "self-hosted" && "self-hosted",
    formatMs(step.ms),
    step.json_mode === false && "no JSON mode",
    step.fallback && "fell back",
    step.skipped && "skipped",
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <CollapsibleSection
      failed={Boolean(step.error)}
      meta={meta}
      title={step.name}
    >
      {step.error ? <div className="text-red-400">{step.error}</div> : null}
      {step.skipped ? (
        <div className="text-muted-foreground">Skipped: {step.skipped}</div>
      ) : null}
      <Value label="Result" value={step.output} />
      <Value label="Input" value={step.input} />
      {step.error ? (
        <Value label="Model reply" value={step.raw_output} />
      ) : null}
    </CollapsibleSection>
  );
}

export function DebugPanel({ data }: { data: unknown }) {
  const [open, setOpen] = useState(false);
  const toggle = useCallback(() => setOpen((v) => !v), []);
  const trace = data as PipelineTrace | undefined;
  const steps = Array.isArray(trace?.steps) ? trace.steps : null;
  const failedStep = steps?.find((step) => step.error);

  const summary = steps
    ? [`${steps.length} steps`, formatMs(trace?.total_ms)]
        .filter(Boolean)
        .join(" · ")
    : "";

  return (
    <div className="w-[min(100%,560px)] overflow-hidden rounded-lg border border-border/50 bg-muted/30 text-[12px]">
      <button
        className="flex w-full items-center justify-between px-3 py-2 text-left text-muted-foreground text-xs hover:text-foreground"
        onClick={toggle}
        type="button"
      >
        <span className="flex items-baseline gap-2">
          <span>Pipeline trace</span>
          {summary ? (
            <span className="text-[10px] text-muted-foreground/80">
              {summary}
            </span>
          ) : null}
          {failedStep ? (
            <span className="text-[10px] text-red-400">
              {failedStep.fallback
                ? `${failedStep.name} fell back`
                : `failed at ${failedStep.name}`}
            </span>
          ) : null}
        </span>
        <Chevron open={open} />
      </button>

      {open ? (
        <div className="space-y-2 border-border/50 border-t px-3 py-2.5">
          {steps?.map((step) => (
            <StepSection key={step.name} step={step} />
          ))}
        </div>
      ) : null}
    </div>
  );
}
