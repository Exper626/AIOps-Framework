"use client";

import {
  BookOpenIcon,
  BotIcon,
  CheckIcon,
  EyeIcon,
  LayersIcon,
  MessageSquareTextIcon,
  SearchIcon,
  TextSearchIcon,
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
  getRerankerEnabled,
  MODEL_TASKS,
  type ModelChoice,
  type ModelKind,
  type ModelSource,
  type ModelTask,
  setAgentSettings,
  setDiagramGenerationEnabled,
  setModelChoice,
  setRerankerEnabled,
} from "@/lib/model-settings";
import { cn } from "@/lib/utils";

type Tab = ModelTask | "agents" | "knowledge";

const MODEL_TAB_ICONS: Record<ModelTask, ReactNode> = {
  answer: <MessageSquareTextIcon />,
  contextManagement: <LayersIcon />,
  query: <TextSearchIcon />,
  visionDescription: <EyeIcon />,
};

const OTHER_TABS: { id: Tab; label: string; icon: ReactNode }[] = [
  { icon: <BotIcon />, id: "agents", label: "Agents" },
  { icon: <BookOpenIcon />, id: "knowledge", label: "Knowledge Base" },
];

const SOURCE_OPTIONS: { id: ModelSource; label: string }[] = [
  { id: "api", label: "API provider" },
  { id: "self-hosted", label: "Self-hosted" },
];

// Self-hosted models come from the backend (GET /models), never from the browser
type SelfHostedModel = { id: string; name: string };

type SelfHostedResponse = Record<ModelKind, SelfHostedModel[]>;

type ModelChoices = Record<ModelTask, ModelChoice>;

// Shown in the API list before you search
const RECOMMENDED: Record<ModelKind, ChatModel[]> = {
  text: chatModels,
  vision: visionModels,
};

function readModelChoices(): ModelChoices {
  return Object.fromEntries(
    MODEL_TASKS.map((task) => [task.id, getModelChoice(task.id)])
  ) as ModelChoices;
}

function sameChoice(a: ModelChoice, b: ModelChoice) {
  return a.source === b.source && a.modelId === b.modelId;
}

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
          {choice.modelId}
        </span>
      </div>
      <CheckIcon className="size-4 shrink-0 text-foreground" />
    </div>
  );
}

// ---------- Models: browser ----------

function Segmented<T extends string>({
  options,
  value,
  onChange,
}: {
  options: { id: T; label: string }[];
  value: T;
  onChange: (value: T) => void;
}) {
  return (
    <div className="inline-flex w-fit rounded-lg bg-foreground/10 p-0.5">
      {options.map((option) => (
        <button
          className={cn(
            "rounded-md px-3 py-1.5 text-sm transition-colors",
            value === option.id
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          )}
          key={option.id}
          onClick={() => onChange(option.id)}
          type="button"
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

function ModelRow({
  name,
  id,
  selected,
  onPick,
}: {
  name: string;
  id: string;
  selected: boolean;
  onPick: () => void;
}) {
  return (
    <button
      className={cn(
        "flex items-center justify-between gap-3 rounded-lg px-3 py-2 text-left transition-colors hover:bg-foreground/10",
        selected && "bg-foreground/5"
      )}
      onClick={onPick}
      type="button"
    >
      <div className="flex min-w-0 flex-col">
        <span className="truncate text-sm">{name}</span>
        <span className="truncate text-muted-foreground text-xs">{id}</span>
      </div>
      {selected ? (
        <CheckIcon className="size-4 shrink-0 text-foreground" />
      ) : null}
    </button>
  );
}

function ApiModelBrowser({
  kind,
  current,
  gatewayModels,
  onPick,
}: {
  kind: ModelKind;
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
  const list: ChatModel[] = isFiltering ? results : RECOMMENDED[kind];

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
        {list.map((model) => (
          <ModelRow
            id={model.id}
            key={model.id}
            name={model.name}
            onPick={() => onPick(model.id)}
            selected={current.source === "api" && current.modelId === model.id}
          />
        ))}
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

function SelfHostedList({
  models,
  current,
  loading,
  onPick,
}: {
  models: SelfHostedModel[];
  current: ModelChoice;
  loading: boolean;
  onPick: (modelId: string) => void;
}) {
  if (loading) {
    return (
      <p className="px-3 py-6 text-center text-muted-foreground text-sm">
        Loading self-hosted models...
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {models.length === 0 ? (
        <div className="flex flex-col items-center gap-1 rounded-xl border border-border/60 border-dashed px-4 py-8 text-center">
          <span className="text-sm">No self-hosted models yet</span>
          <span className="max-w-sm text-muted-foreground text-xs">
            Self-hosted models are set up on the backend. Once they&apos;re
            added there, they show up here.
          </span>
        </div>
      ) : (
        <div className="flex flex-col gap-1">
          {models.map((model) => (
            <ModelRow
              id={model.id}
              key={model.id}
              name={model.name}
              onPick={() => onPick(model.id)}
              selected={
                current.source === "self-hosted" && current.modelId === model.id
              }
            />
          ))}
        </div>
      )}
    </div>
  );
}

function ModelSlot({
  kind,
  current,
  gatewayModels,
  selfHosted,
  selfHostedLoading,
  onPick,
}: {
  kind: ModelKind;
  current: ModelChoice;
  gatewayModels: GatewayModelWithCapabilities[];
  selfHosted: SelfHostedModel[];
  selfHostedLoading: boolean;
  onPick: (choice: ModelChoice) => void;
}) {
  // Which source you're browsing; starts on the one currently selected
  const [source, setSource] = useState<ModelSource>(current.source);

  const displayName =
    current.source === "self-hosted"
      ? (selfHosted.find((m) => m.id === current.modelId)?.name ??
        current.modelId)
      : (RECOMMENDED[kind].find((m) => m.id === current.modelId)?.name ??
        gatewayModels.find((m) => m.id === current.modelId)?.name ??
        current.modelId);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-1.5">
        <span className="text-muted-foreground text-xs">Selected model</span>
        <CurrentModelCard choice={current} displayName={displayName} />
      </div>

      <div className="flex flex-col gap-3 border-border/60 border-t pt-4">
        <Segmented
          onChange={setSource}
          options={SOURCE_OPTIONS}
          value={source}
        />

        {source === "api" ? (
          <ApiModelBrowser
            current={current}
            gatewayModels={gatewayModels}
            kind={kind}
            onPick={(modelId) => onPick({ modelId, source: "api" })}
          />
        ) : (
          <SelfHostedList
            current={current}
            loading={selfHostedLoading}
            models={selfHosted}
            onPick={(modelId) => onPick({ modelId, source: "self-hosted" })}
          />
        )}
      </div>
    </div>
  );
}

function ModelTaskPanel({
  task,
  draft,
  unsavedTasks,
  justSaved,
  gatewayModels,
  selfHosted,
  selfHostedLoading,
  onPick,
  onSave,
}: {
  task: (typeof MODEL_TASKS)[number];
  draft: ModelChoice;
  unsavedTasks: string[];
  justSaved: boolean;
  gatewayModels: GatewayModelWithCapabilities[];
  selfHosted?: SelfHostedResponse;
  selfHostedLoading: boolean;
  onPick: (choice: ModelChoice) => void;
  onSave: () => void;
}) {
  let saveStatus = "";
  if (unsavedTasks.length > 0) {
    saveStatus = `Unsaved: ${unsavedTasks.join(", ")}`;
  } else if (justSaved) {
    saveStatus = "Saved";
  }

  return (
    <div className="flex min-h-full flex-col">
      <div className="flex flex-1 flex-col gap-4 py-3">
        <SectionHeader
          description={task.description}
          title={`${task.label} model`}
        />
        <ModelSlot
          current={draft}
          gatewayModels={gatewayModels}
          key={task.id}
          kind={task.kind}
          onPick={onPick}
          selfHosted={selfHosted?.[task.kind] ?? []}
          selfHostedLoading={selfHostedLoading}
        />
      </div>

      {/* One Save for every model tab */}
      <div className="sticky -bottom-2 flex items-center justify-end gap-3 border-border/60 border-t bg-background py-3">
        <span className="truncate text-muted-foreground text-xs">
          {saveStatus}
        </span>
        <Button disabled={unsavedTasks.length === 0} onClick={onSave} size="sm">
          Save
        </Button>
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

function KnowledgeBasePanel({
  reranker,
  onRerankerChange,
}: {
  reranker: boolean;
  onRerankerChange: (enabled: boolean) => void;
}) {
  return (
    <div className="flex flex-col gap-3 py-3">
      <SectionHeader
        description="Vendor documentation the assistant searches when answering."
        title="Knowledge Base"
      />
      <ToggleRow
        checked={reranker}
        description="Re-orders the documents found for your question so the most relevant ones reach the answer. Usually more accurate, a little slower."
        onChange={onRerankerChange}
        title="Reranker"
      />
      <span className="pt-2 text-muted-foreground text-xs">Sources</span>
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
  const [tab, setTab] = useState<Tab>("answer");
  const [choices, setChoices] = useState<ModelChoices>(readModelChoices);
  // Picks stay here, across tabs, until Save; closing the dialog discards them
  const [drafts, setDrafts] = useState<ModelChoices>(readModelChoices);
  const [justSaved, setJustSaved] = useState(false);
  const [agentSettings, setAgentSettingsState] =
    useState<AgentSettings>(getAgentSettings);
  const [diagramGeneration, setDiagramGeneration] = useState(true);
  const [reranker, setReranker] = useState(true);

  // Read the saved choices each time the dialog opens
  useEffect(() => {
    if (open) {
      const saved = readModelChoices();
      setChoices(saved);
      setDrafts(saved);
      setJustSaved(false);
      setAgentSettingsState(getAgentSettings());
      setDiagramGeneration(getDiagramGenerationEnabled());
      setReranker(getRerankerEnabled());
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

  // Self-hosted models the backend offers; empty until some are set up there
  // (if they can't be loaded, the list just shows as empty)
  const { data: selfHosted, isLoading: selfHostedLoading } =
    useSWR<SelfHostedResponse>(
      open
        ? `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/models/self-hosted`
        : null,
      (url: string) => fetch(url, { cache: "no-store" }).then((r) => r.json()),
      { revalidateOnFocus: false }
    );
  const unsavedTasks = MODEL_TASKS.filter(
    (task) => !sameChoice(drafts[task.id], choices[task.id])
  );

  const handlePick = (task: ModelTask, choice: ModelChoice) => {
    setDrafts((prev) => ({ ...prev, [task]: choice }));
    setJustSaved(false);
  };

  const handleSave = () => {
    for (const task of MODEL_TASKS) {
      setModelChoice(task.id, drafts[task.id]);
    }
    setChoices(drafts);
    setJustSaved(true);
  };

  const activeTask = MODEL_TASKS.find((task) => task.id === tab);

  const tabButton = (id: Tab, label: string, icon: ReactNode) => (
    <button
      className={cn(
        "flex items-center gap-2.5 whitespace-nowrap rounded-lg px-3 py-2 text-left text-sm transition-colors [&_svg]:size-4 [&_svg]:shrink-0",
        tab === id
          ? "bg-muted text-foreground"
          : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
      )}
      key={id}
      onClick={() => setTab(id)}
      type="button"
    >
      {icon}
      <span className="truncate">{label}</span>
      {unsavedTasks.some((task) => task.id === id) ? (
        <span
          className="ml-auto size-1.5 shrink-0 rounded-full bg-foreground"
          title="Unsaved"
        />
      ) : null}
    </button>
  );

  const handleAgentChange = (id: AgentId, enabled: boolean) => {
    const next = { ...agentSettings, [id]: enabled };
    setAgentSettings(next);
    setAgentSettingsState(next);
  };

  const handleDiagramChange = (enabled: boolean) => {
    setDiagramGenerationEnabled(enabled);
    setDiagramGeneration(enabled);
  };

  const handleRerankerChange = (enabled: boolean) => {
    setRerankerEnabled(enabled);
    setReranker(enabled);
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
          <nav className="flex shrink-0 gap-1 overflow-x-auto border-b border-border/60 p-2 md:w-60 md:flex-col md:border-r md:border-b-0 md:p-3">
            <span className="hidden px-3 pt-1 pb-1 font-medium text-[11px] text-muted-foreground/70 uppercase tracking-wide md:block">
              Models
            </span>
            {MODEL_TASKS.map((task) =>
              tabButton(task.id, task.label, MODEL_TAB_ICONS[task.id])
            )}
            <div className="hidden border-border/60 border-t md:my-2 md:block" />
            {OTHER_TABS.map((t) => tabButton(t.id, t.label, t.icon))}
          </nav>

          <div className="min-h-0 flex-1 overflow-y-auto px-5 py-2">
            {activeTask ? (
              <ModelTaskPanel
                draft={drafts[activeTask.id]}
                gatewayModels={gatewayModels}
                justSaved={justSaved}
                key={activeTask.id}
                onPick={(choice) => handlePick(activeTask.id, choice)}
                onSave={handleSave}
                selfHosted={selfHosted}
                selfHostedLoading={selfHostedLoading}
                task={activeTask}
                unsavedTasks={unsavedTasks.map((task) => task.label)}
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
            {tab === "knowledge" ? (
              <KnowledgeBasePanel
                onRerankerChange={handleRerankerChange}
                reranker={reranker}
              />
            ) : null}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
