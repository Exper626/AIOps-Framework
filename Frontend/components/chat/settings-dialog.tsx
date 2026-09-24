"use client";

import {
  BookOpenIcon,
  BotIcon,
  CheckIcon,
  EyeIcon,
  MessageSquareTextIcon,
  SearchIcon,
  XIcon,
} from "lucide-react";
import { type ReactNode, useEffect, useMemo, useState } from "react";
import useSWR from "swr";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  type ChatModel,
  chatModels,
  type GatewayModelWithCapabilities,
  visionModels,
} from "@/lib/ai/models";
import {
  AGENTS,
  type AgentId,
  type AgentSettings,
  getAgentSettings,
  getDiagramGenerationEnabled,
  getModelChoice,
  type ModelChoice,
  type ModelSettingKind,
  type ModelSource,
  setAgentSettings,
  setDiagramGenerationEnabled,
  setModelChoice,
} from "@/lib/model-settings";
import { cn } from "@/lib/utils";

type Tab = ModelSettingKind | "agents" | "knowledge";

const TABS: { id: Tab; label: string; icon: ReactNode }[] = [
  { icon: <MessageSquareTextIcon />, id: "text", label: "Text" },
  { icon: <EyeIcon />, id: "vision", label: "Vision" },
  { icon: <BotIcon />, id: "agents", label: "Agents" },
  { icon: <BookOpenIcon />, id: "knowledge", label: "Knowledge Base" },
];

const SLOTS: Record<
  ModelSettingKind,
  { label: string; description: string; recommended: ChatModel[] }
> = {
  text: {
    description: "Answers network questions and troubleshooting requests.",
    label: "Text",
    recommended: chatModels,
  },
  vision: {
    description: "Reads topology images and screenshots you attach.",
    label: "Vision",
    recommended: visionModels,
  },
};

type CapabilityFilter = "vision" | "tools" | "reasoning";

const CAPABILITY_FILTERS: { id: CapabilityFilter; label: string }[] = [
  { id: "vision", label: "Vision" },
  { id: "tools", label: "Tools" },
  { id: "reasoning", label: "Reasoning" },
];

// Mirrors the vendor folders in the repo's "Knowledge Base" directory
const KNOWLEDGE_SOURCES: { vendor: string; categories: string[] }[] = [
  { categories: ["Routers", "Switches", "Access points"], vendor: "Cisco" },
  { categories: ["Routers", "Switches", "Access points"], vendor: "Juniper" },
];

const MAX_RESULTS = 50;

function SectionHeader({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="font-medium text-sm">{title}</span>
      <span className="text-muted-foreground text-xs">{description}</span>
    </div>
  );
}

function SourceTag({ source }: { source: ModelSource }) {
  return (
    <span className="shrink-0 rounded-md bg-foreground/10 px-1.5 py-0.5 text-[11px] text-muted-foreground">
      {source === "api" ? "API" : "Self-hosted"}
    </span>
  );
}

// ---------- Models: current choice ----------

function CurrentModelCard({
  choice,
  displayName,
}: {
  choice: ModelChoice;
  displayName: string;
}) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-xl border border-foreground/20 bg-foreground/5 px-4 py-3">
      <div className="flex min-w-0 flex-col gap-0.5">
        <div className="flex min-w-0 items-center gap-2">
          <span className="truncate text-sm">{displayName}</span>
          <SourceTag source={choice.source} />
        </div>
        <span className="truncate text-muted-foreground text-xs">
          {choice.source === "self-hosted" ? choice.baseUrl : choice.modelId}
        </span>
      </div>
      <CheckIcon className="size-4 shrink-0 text-foreground" />
    </div>
  );
}

// ---------- Models: browser ----------

function SourceSwitch({
  value,
  onChange,
}: {
  value: ModelSource;
  onChange: (source: ModelSource) => void;
}) {
  return (
    <div className="inline-flex w-fit rounded-lg bg-foreground/10 p-0.5">
      {(["api", "self-hosted"] as const).map((source) => (
        <button
          className={cn(
            "rounded-md px-3 py-1.5 text-sm transition-colors",
            value === source
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          )}
          key={source}
          onClick={() => onChange(source)}
          type="button"
        >
          {source === "api" ? "API provider" : "Self-hosted"}
        </button>
      ))}
    </div>
  );
}

function ApiModelBrowser({
  kind,
  current,
  gatewayModels,
  onPick,
}: {
  kind: ModelSettingKind;
  current: ModelChoice;
  gatewayModels: GatewayModelWithCapabilities[];
  onPick: (modelId: string) => void;
}) {
  const [query, setQuery] = useState("");
  const [provider, setProvider] = useState("all");
  // Vision slot only ever shows vision-capable models
  const [filters, setFilters] = useState<Set<CapabilityFilter>>(
    () => new Set(kind === "vision" ? ["vision"] : [])
  );

  const providers = useMemo(
    () => [...new Set(gatewayModels.map((m) => m.provider))].sort(),
    [gatewayModels]
  );

  // Vision's locked chip doesn't count; any other chip means "show results"
  const defaultFilterCount = kind === "vision" ? 1 : 0;
  const isFiltering =
    query.trim() !== "" ||
    provider !== "all" ||
    filters.size > defaultFilterCount;

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    return gatewayModels
      .filter((m) => [...filters].every((f) => m.capabilities[f]))
      .filter((m) => provider === "all" || m.provider === provider)
      .filter(
        (m) =>
          !q ||
          m.id.toLowerCase().includes(q) ||
          m.name.toLowerCase().includes(q)
      )
      .slice(0, MAX_RESULTS);
  }, [filters, gatewayModels, provider, query]);

  const toggleFilter = (id: CapabilityFilter) => {
    if (kind === "vision" && id === "vision") {
      return;
    }
    setFilters((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  // With no search or provider chosen, show our short recommended list
  const list: ChatModel[] = isFiltering ? results : SLOTS[kind].recommended;

  return (
    <div className="flex flex-col gap-3">
      <div className="relative">
        <SearchIcon className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          className="h-10 w-full rounded-xl border border-border/60 bg-transparent pr-3 pl-9 text-sm outline-none placeholder:text-muted-foreground/70 focus:border-foreground/30"
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search models, e.g. claude, gpt, llama"
          type="text"
          value={query}
        />
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {CAPABILITY_FILTERS.map((f) => {
          const active = filters.has(f.id);
          const locked = kind === "vision" && f.id === "vision";
          return (
            <button
              aria-pressed={active}
              className={cn(
                "rounded-full border px-3 py-1 text-xs transition-colors",
                active
                  ? "border-foreground/30 bg-foreground/10 text-foreground"
                  : "border-border/60 text-muted-foreground hover:text-foreground",
                locked && "cursor-default"
              )}
              key={f.id}
              onClick={() => toggleFilter(f.id)}
              title={locked ? "Vision models only" : undefined}
              type="button"
            >
              {f.label}
            </button>
          );
        })}
        <select
          className="ml-auto h-7 rounded-full border border-border/60 bg-background px-3 text-muted-foreground text-xs outline-none"
          onChange={(e) => setProvider(e.target.value)}
          value={provider}
        >
          <option value="all">All providers</option>
          {providers.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>

      <span className="text-muted-foreground text-xs">
        {isFiltering ? `${results.length} results` : "Recommended"}
      </span>

      <div className="flex flex-col gap-1">
        {list.map((model) => {
          const selected =
            current.source === "api" && current.modelId === model.id;
          return (
            <button
              className={cn(
                "flex items-center justify-between gap-3 rounded-lg px-3 py-2 text-left transition-colors hover:bg-foreground/10",
                selected && "bg-foreground/5"
              )}
              key={model.id}
              onClick={() => onPick(model.id)}
              type="button"
            >
              <div className="flex min-w-0 flex-col">
                <span className="truncate text-sm">{model.name}</span>
                <span className="truncate text-muted-foreground text-xs">
                  {model.id}
                </span>
              </div>
              {selected ? (
                <CheckIcon className="size-4 shrink-0 text-foreground" />
              ) : null}
            </button>
          );
        })}
        {isFiltering && results.length === 0 ? (
          <div className="px-3 py-6 text-center text-muted-foreground text-sm">
            {gatewayModels.length === 0
              ? "Couldn't load the model list. Try again later."
              : "No models match these filters."}
          </div>
        ) : null}
      </div>
    </div>
  );
}

function SelfHostedForm({
  current,
  onSave,
}: {
  current: ModelChoice;
  onSave: (baseUrl: string, modelId: string) => void;
}) {
  const [baseUrl, setBaseUrl] = useState(
    current.source === "self-hosted" ? (current.baseUrl ?? "") : ""
  );
  const [modelId, setModelId] = useState(
    current.source === "self-hosted" ? current.modelId : ""
  );
  const [status, setStatus] = useState<
    | { state: "idle" }
    | { state: "testing" }
    | { state: "ok"; models: string[] }
    | { state: "error"; message: string }
  >({ state: "idle" });

  const testConnection = async () => {
    setStatus({ state: "testing" });
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/models/test`,
        {
          body: JSON.stringify({ baseUrl }),
          headers: { "Content-Type": "application/json" },
          method: "POST",
        }
      );
      const data = (await res.json()) as { models?: string[]; error?: string };
      if (!res.ok) {
        setStatus({
          message: data.error ?? "Connection failed",
          state: "error",
        });
        return;
      }
      const models = data.models ?? [];
      setStatus({ models, state: "ok" });
      if (!modelId && models.length > 0) {
        setModelId(models[0]);
      }
    } catch {
      setStatus({ message: "Connection failed", state: "error" });
    }
  };

  const inputClass =
    "h-10 w-full rounded-xl border border-border/60 bg-transparent px-3 text-sm outline-none placeholder:text-muted-foreground/70 focus:border-foreground/30";

  return (
    <div className="flex flex-col gap-4">
      <label className="flex flex-col gap-1.5">
        <span className="text-xs">Server URL</span>
        <input
          className={inputClass}
          onChange={(e) => {
            setBaseUrl(e.target.value);
            setStatus({ state: "idle" });
          }}
          placeholder="http://10.0.0.5:11434/v1"
          type="url"
          value={baseUrl}
        />
        <span className="text-muted-foreground text-xs">
          Any OpenAI-compatible server, such as Ollama, vLLM or LM Studio.
        </span>
      </label>

      <div className="flex items-center gap-3">
        <Button
          disabled={!baseUrl || status.state === "testing"}
          onClick={testConnection}
          size="sm"
          variant="outline"
        >
          {status.state === "testing" ? "Testing..." : "Test connection"}
        </Button>
        {status.state === "ok" ? (
          <span className="text-muted-foreground text-xs">
            Connected · {status.models.length} models found
          </span>
        ) : null}
        {status.state === "error" ? (
          <span className="text-destructive text-xs">{status.message}</span>
        ) : null}
      </div>

      <label className="flex flex-col gap-1.5">
        <span className="text-xs">Model name</span>
        <input
          className={inputClass}
          list="self-hosted-models"
          onChange={(e) => setModelId(e.target.value)}
          placeholder="e.g. llama3.1:8b"
          type="text"
          value={modelId}
        />
        {status.state === "ok" ? (
          <datalist id="self-hosted-models">
            {status.models.map((m) => (
              <option key={m} value={m} />
            ))}
          </datalist>
        ) : null}
      </label>

      <p className="text-muted-foreground text-xs">
        If the server needs an API key, set SELF_HOSTED_API_KEY in the
        server&apos;s environment. Keys are never stored in the browser.
      </p>

      <Button
        className="w-fit"
        disabled={!baseUrl || !modelId.trim()}
        onClick={() => onSave(baseUrl.trim(), modelId.trim())}
        size="sm"
      >
        Use this model
      </Button>
    </div>
  );
}

function ModelTab({
  kind,
  current,
  gatewayModels,
  onChoose,
}: {
  kind: ModelSettingKind;
  current: ModelChoice;
  gatewayModels: GatewayModelWithCapabilities[];
  onChoose: (choice: ModelChoice) => void;
}) {
  // Which source you're browsing; starts on the one currently in use
  const [source, setSource] = useState<ModelSource>(current.source);

  const displayName =
    current.source === "self-hosted"
      ? current.modelId
      : (SLOTS[kind].recommended.find((m) => m.id === current.modelId)?.name ??
        gatewayModels.find((m) => m.id === current.modelId)?.name ??
        current.modelId);

  return (
    <div className="flex flex-col gap-4 py-3">
      <SectionHeader
        description={SLOTS[kind].description}
        title={`${SLOTS[kind].label} model`}
      />

      <div className="flex flex-col gap-1.5">
        <span className="text-muted-foreground text-xs">Current model</span>
        <CurrentModelCard choice={current} displayName={displayName} />
      </div>

      <div className="flex flex-col gap-3 border-border/60 border-t pt-4">
        <SourceSwitch onChange={setSource} value={source} />

        {source === "api" ? (
          <ApiModelBrowser
            current={current}
            gatewayModels={gatewayModels}
            kind={kind}
            onPick={(modelId) => onChoose({ modelId, source: "api" })}
          />
        ) : (
          <SelfHostedForm
            current={current}
            onSave={(baseUrl, modelId) =>
              onChoose({ baseUrl, modelId, source: "self-hosted" })
            }
          />
        )}
      </div>
    </div>
  );
}

// ---------- Agents ----------

function Toggle({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
}) {
  return (
    <button
      aria-checked={checked}
      aria-label={label}
      className={cn(
        "relative inline-flex h-6 w-10 shrink-0 items-center rounded-full transition-colors",
        checked ? "bg-foreground" : "bg-foreground/20"
      )}
      onClick={() => onChange(!checked)}
      role="switch"
      type="button"
    >
      <span
        className={cn(
          "inline-block size-5 rounded-full bg-background shadow-sm transition-transform",
          checked ? "translate-x-[18px]" : "translate-x-0.5"
        )}
      />
    </button>
  );
}

function ToggleRow({
  title,
  description,
  checked,
  onChange,
}: {
  title: string;
  description: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl border border-border/60 px-4 py-3">
      <div className="flex min-w-0 flex-col gap-0.5">
        <span className="text-sm">{title}</span>
        <span className="text-muted-foreground text-xs">{description}</span>
      </div>
      <Toggle checked={checked} label={title} onChange={onChange} />
    </div>
  );
}

function AgentsPanel({
  settings,
  onChange,
  diagramGeneration,
  onDiagramChange,
}: {
  settings: AgentSettings;
  onChange: (id: AgentId, enabled: boolean) => void;
  diagramGeneration: boolean;
  onDiagramChange: (enabled: boolean) => void;
}) {
  return (
    <div className="flex flex-col gap-3 py-3">
      <SectionHeader
        description="Turn individual steps of the answering pipeline on or off."
        title="Agents"
      />
      <div className="flex flex-col gap-1.5">
        {AGENTS.map((agent) => (
          <ToggleRow
            checked={settings[agent.id]}
            description={agent.description}
            key={agent.id}
            onChange={(enabled) => onChange(agent.id, enabled)}
            title={agent.name}
          />
        ))}
        <ToggleRow
          checked={diagramGeneration}
          description="Draws a network topology diagram when you ask for one."
          onChange={onDiagramChange}
          title="Diagram generation"
        />
      </div>
    </div>
  );
}

// ---------- Knowledge Base ----------

function KnowledgeBasePanel() {
  return (
    <div className="flex flex-col gap-3 py-3">
      <SectionHeader
        description="Vendor documentation the assistant searches when answering."
        title="Knowledge Base"
      />
      <div className="flex flex-col gap-1.5">
        {KNOWLEDGE_SOURCES.map((source) => (
          <div
            className="flex flex-col gap-0.5 rounded-xl border border-border/60 px-4 py-3"
            key={source.vendor}
          >
            <span className="text-sm">{source.vendor}</span>
            <span className="text-muted-foreground text-xs">
              {source.categories.join(" · ")}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---------- Dialog ----------

export function SettingsDialog({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const [tab, setTab] = useState<Tab>("text");
  const [choices, setChoices] = useState<Record<ModelSettingKind, ModelChoice>>(
    () => ({ text: getModelChoice("text"), vision: getModelChoice("vision") })
  );
  const [agentSettings, setAgentSettingsState] =
    useState<AgentSettings>(getAgentSettings);
  const [diagramGeneration, setDiagramGeneration] = useState(true);

  // Read the saved choices each time the dialog opens
  useEffect(() => {
    if (open) {
      setChoices({
        text: getModelChoice("text"),
        vision: getModelChoice("vision"),
      });
      setAgentSettingsState(getAgentSettings());
      setDiagramGeneration(getDiagramGenerationEnabled());
    }
  }, [open]);

  // Full AI Gateway catalogue, only fetched once the dialog is opened
  const { data: modelsResponse } = useSWR<{
    models: GatewayModelWithCapabilities[];
  }>(
    // ?v=2 skips any old cached copy of the previous empty response
    open ? `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/models?v=2` : null,
    (url: string) => fetch(url, { cache: "no-store" }).then((r) => r.json()),
    { revalidateOnFocus: false }
  );
  const gatewayModels = modelsResponse?.models ?? [];

  const handleChoose = (kind: ModelSettingKind, choice: ModelChoice) => {
    setModelChoice(kind, choice);
    setChoices((prev) => ({ ...prev, [kind]: choice }));
  };

  const handleAgentChange = (id: AgentId, enabled: boolean) => {
    const next = { ...agentSettings, [id]: enabled };
    setAgentSettings(next);
    setAgentSettingsState(next);
  };

  const handleDiagramChange = (enabled: boolean) => {
    setDiagramGenerationEnabled(enabled);
    setDiagramGeneration(enabled);
  };

  return (
    <Dialog onOpenChange={onOpenChange} open={open}>
      <DialogContent
        className="flex h-[min(600px,85dvh)] flex-col gap-0 overflow-hidden rounded-2xl p-0 sm:max-w-[680px]"
        showCloseButton={false}
      >
        <div className="flex items-center justify-between border-b border-border/60 px-5 py-4">
          <DialogTitle className="font-semibold text-lg">Settings</DialogTitle>
          <DialogClose asChild>
            <Button aria-label="Close" size="icon-sm" variant="ghost">
              <XIcon />
            </Button>
          </DialogClose>
        </div>
        <DialogDescription className="sr-only">
          Choose models, agents and knowledge sources.
        </DialogDescription>

        <div className="flex min-h-0 flex-1 flex-col md:flex-row">
          <nav className="flex shrink-0 gap-1 overflow-x-auto border-b border-border/60 p-2 md:w-48 md:flex-col md:border-r md:border-b-0 md:p-3">
            {TABS.map((t) => (
              <button
                className={cn(
                  "flex items-center gap-2.5 whitespace-nowrap rounded-lg px-3 py-2 text-left text-sm transition-colors [&_svg]:size-4",
                  tab === t.id
                    ? "bg-muted text-foreground"
                    : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
                )}
                key={t.id}
                onClick={() => setTab(t.id)}
                type="button"
              >
                {t.icon}
                {t.label}
              </button>
            ))}
          </nav>

          <div className="min-h-0 flex-1 overflow-y-auto px-5 py-2">
            {tab === "text" || tab === "vision" ? (
              <ModelTab
                current={choices[tab]}
                gatewayModels={gatewayModels}
                key={tab}
                kind={tab}
                onChoose={(choice) => handleChoose(tab, choice)}
              />
            ) : null}
            {tab === "agents" ? (
              <AgentsPanel
                diagramGeneration={diagramGeneration}
                onChange={handleAgentChange}
                onDiagramChange={handleDiagramChange}
                settings={agentSettings}
              />
            ) : null}
            {tab === "knowledge" ? <KnowledgeBasePanel /> : null}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
