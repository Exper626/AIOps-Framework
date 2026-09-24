import { DEFAULT_CHAT_MODEL, DEFAULT_VISION_MODEL } from "@/lib/ai/models";

// Choices from the Settings dialog, stored in cookies so both the sidebar
// (settings) and the chat (sending messages) can read them.
export type ModelSettingKind = "text" | "vision";

export type AgentId = "retrieval" | "contextManagement" | "queryTransformation";

export const AGENTS: { id: AgentId; name: string; description: string }[] = [
  {
    description:
      "Searches the knowledge base for vendor docs relevant to your question.",
    id: "retrieval",
    name: "Retrieval agent",
  },
  {
    description:
      "Keeps track of the conversation so follow-up questions have context.",
    id: "contextManagement",
    name: "Context management agent",
  },
  {
    description:
      "Rewrites your question into better search queries before retrieval.",
    id: "queryTransformation",
    name: "Query transformation agent",
  },
];

export type AgentSettings = Record<AgentId, boolean>;

const DEFAULT_AGENTS: AgentSettings = {
  contextManagement: true,
  queryTransformation: true,
  retrieval: true,
};

const MODEL_COOKIES: Record<ModelSettingKind, string> = {
  text: "chat-model",
  vision: "vision-model",
};

const MODEL_DEFAULTS: Record<ModelSettingKind, string> = {
  text: DEFAULT_CHAT_MODEL,
  vision: DEFAULT_VISION_MODEL,
};

const AGENTS_COOKIE = "agent-settings";
const DIAGRAM_COOKIE = "diagram-generation";

function readCookie(name: string): string | undefined {
  if (typeof document === "undefined") {
    return;
  }
  const value = document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`))
    ?.split("=")[1];
  return value ? decodeURIComponent(value) : undefined;
}

function writeCookie(name: string, value: string) {
  // biome-ignore lint/suspicious/noDocumentCookie: simple client-side preference
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=31536000; samesite=lax`;
}

export function getModelSetting(kind: ModelSettingKind): string {
  return readCookie(MODEL_COOKIES[kind]) ?? MODEL_DEFAULTS[kind];
}

export function setModelSetting(kind: ModelSettingKind, modelId: string) {
  writeCookie(MODEL_COOKIES[kind], modelId);
}

// Where a model runs: through the AI Gateway, or on your own server
// (any OpenAI-compatible endpoint such as Ollama, vLLM or LM Studio).
export type ModelSource = "api" | "self-hosted";

export type ModelChoice = {
  source: ModelSource;
  modelId: string;
  baseUrl?: string;
};

const CHOICE_COOKIES: Record<ModelSettingKind, string> = {
  text: "text-model-choice",
  vision: "vision-model-choice",
};

export function getModelChoice(kind: ModelSettingKind): ModelChoice {
  const raw = readCookie(CHOICE_COOKIES[kind]);
  if (raw) {
    try {
      const parsed = JSON.parse(raw) as ModelChoice;
      if (parsed.modelId) {
        return parsed;
      }
    } catch {
      // fall through to the plain model ID
    }
  }
  return { modelId: getModelSetting(kind), source: "api" };
}

export function setModelChoice(kind: ModelSettingKind, choice: ModelChoice) {
  writeCookie(CHOICE_COOKIES[kind], JSON.stringify(choice));
  if (choice.source === "api") {
    setModelSetting(kind, choice.modelId);
  }
}

export function getAgentSettings(): AgentSettings {
  const raw = readCookie(AGENTS_COOKIE);
  if (!raw) {
    return DEFAULT_AGENTS;
  }
  try {
    return { ...DEFAULT_AGENTS, ...JSON.parse(raw) };
  } catch {
    return DEFAULT_AGENTS;
  }
}

export function setAgentSettings(settings: AgentSettings) {
  writeCookie(AGENTS_COOKIE, JSON.stringify(settings));
}

export function getDiagramGenerationEnabled(): boolean {
  return readCookie(DIAGRAM_COOKIE) !== "false";
}

export function setDiagramGenerationEnabled(enabled: boolean) {
  writeCookie(DIAGRAM_COOKIE, String(enabled));
}
