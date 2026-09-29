"use client";

import {
  BookOpenIcon,
  BrainIcon,
  CaptionsIcon,
  EyeIcon,
  ImageIcon,
  LayersIcon,
  ListFilterIcon,
  MessageSquareTextIcon,
  NetworkIcon,
  SignpostIcon,
  TextSearchIcon,
} from "lucide-react";
import { type ReactNode, useCallback, useState } from "react";
import { chatModels, visionModels } from "@/lib/ai/models";
import { cn } from "@/lib/utils";

// One pipeline step as the backend records it (Backend/pipeline/trace.py).
// "output" is the step's result in a line; "input" and "raw_output" are the
// exact text the model was sent and replied with.
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
};

// Plain names and icons for the backend's step names. The four tasks the
// router plans get blue icons, the steps that help them grey ones.
const STEPS: {
  icon: ReactNode;
  label: string;
  prefix: string;
  task: boolean;
}[] = [
  { icon: <SignpostIcon />, label: "Plan", prefix: "router", task: false },
  {
    icon: <EyeIcon />,
    label: "Image description",
    prefix: "vision description",
    task: true,
  },
  {
    icon: <BrainIcon />,
    label: "Memory",
    prefix: "memory search",
    task: false,
  },
  { icon: <TextSearchIcon />, label: "Question", prefix: "query", task: false },
  {
    icon: <LayersIcon />,
    label: "Earlier messages",
    prefix: "context management",
    task: false,
  },
  {
    icon: <ListFilterIcon />,
    label: "Retrieval agent",
    prefix: "retrieval agent",
    task: false,
  },
  {
    icon: <BookOpenIcon />,
    label: "Retrieval",
    prefix: "knowledge base",
    task: true,
  },
  {
    icon: <MessageSquareTextIcon />,
    label: "Text generation",
    prefix: "answer",
    task: true,
  },
  {
    icon: <NetworkIcon />,
    label: "Image generation",
    prefix: "diagram",
    task: true,
  },
  { icon: <ImageIcon />, label: "Graphviz", prefix: "graphviz", task: false },
  { icon: <CaptionsIcon />, label: "Caption", prefix: "caption", task: false },
  {
    icon: <BrainIcon />,
    label: "Memory update",
    prefix: "memory update",
    task: false,
  },
];

const MODEL_NAMES = new Map(
  [...chatModels, ...visionModels].map((model) => [model.id, model.name])
);

function describeStep(name: string) {
  const known = STEPS.find((step) => name.startsWith(step.prefix));

  if (!known) {
    return { icon: <SignpostIcon />, label: name, task: false };
  }

  // "vision description 2" is the second attached image
  const number = name.slice(known.prefix.length).trim();
  return { ...known, label: number ? `${known.label} ${number}` : known.label };
}

function formatMs(ms?: number) {
  if (typeof ms !== "number") {
    return "";
  }
  return ms >= 1000 ? `${(ms / 1000).toFixed(1)} s` : `${ms} ms`;
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
      <div className="mb-0.5 text-[11px] text-muted-foreground">{label}</div>
      <div className="max-h-64 overflow-auto whitespace-pre-wrap break-words rounded-md border border-border/40 bg-background/60 p-2 text-[11.5px] text-foreground/80 leading-relaxed">
        {toText(value)}
      </div>
    </div>
  );
}

function StepRow({ step }: { step: TraceStep }) {
  const [open, setOpen] = useState(false);
  const toggle = useCallback(() => setOpen((value) => !value), []);
  const { icon, label, task } = describeStep(step.name);
  const model = step.model ? (MODEL_NAMES.get(step.model) ?? step.model) : "";
  const failed = Boolean(step.error) && !step.fallback;
  const result = failed ? step.error : toText(step.output ?? "");
  const modelDetails = [
    model,
    step.source === "self-hosted" && "self-hosted",
    step.json_mode === false && "no JSON mode",
  ]
    .filter(Boolean)
    .join(" · ");

  return (
    <li>
      <button
        aria-expanded={open}
        className="grid w-full grid-cols-[1fr_auto] items-start gap-x-3 gap-y-0.5 rounded-md px-2 py-1.5 text-left transition-colors hover:bg-foreground/5 sm:grid-cols-[9.5rem_1fr_auto]"
        onClick={toggle}
        type="button"
      >
        <span className="flex items-center gap-2 text-muted-foreground">
          <span
            className={cn(
              "shrink-0 [&_svg]:size-4",
              task ? "text-brand dark:text-brand-light" : ""
            )}
          >
            {icon}
          </span>
          {label}
        </span>
        <span
          className={cn(
            "col-span-2 row-start-2 break-words text-foreground/85 sm:col-span-1 sm:col-start-2 sm:row-start-1",
            failed && "text-red-400",
            step.fallback && "text-amber-500 dark:text-amber-400"
          )}
        >
          {result}
          {step.name === "answer" && model ? (
            <span className="text-muted-foreground"> · {model}</span>
          ) : null}
        </span>
        <span className="col-start-2 row-start-1 text-[11px] text-muted-foreground/70 tabular-nums sm:col-start-3">
          {formatMs(step.ms)}
        </span>
      </button>

      {open ? (
        <div className="mx-2 mt-1 mb-2 space-y-2 border-brand-light/40 border-l-2 pl-3">
          {step.error ? <div className="text-red-400">{step.error}</div> : null}
          <Value label="Model" value={modelDetails} />
          <Value label="Input" value={step.input} />
          <Value label="Reply" value={step.raw_output} />
        </div>
      ) : null}
    </li>
  );
}

// Each step that ran, with its result; click one for the exact input and reply
export function DebugPanel({ data }: { data: unknown }) {
  const trace = data as PipelineTrace | undefined;
  const steps = Array.isArray(trace?.steps)
    ? trace.steps.filter((step) => !step.skipped)
    : [];

  if (steps.length === 0) {
    return null;
  }

  return (
    <ul className="w-[min(100%,620px)] rounded-lg border border-border/50 bg-muted/30 p-1.5 text-[12.5px]">
      {steps.map((step) => (
        <StepRow key={step.name} step={step} />
      ))}
    </ul>
  );
}
