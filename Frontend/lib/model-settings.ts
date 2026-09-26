// Choices from the Settings dialog, stored in cookies so both the sidebar
// (settings) and the chat (sending messages) can read them.

// Each step of the answering pipeline can use its own model
export type ModelTask =
  | "query"
  | "contextManagement"
  | "answer"
  | "visionDescription";

// Whether a step reads text or images; self-hosted models are listed by the
// backend under these kinds
export type ModelKind = "text" | "vision";

export const MODEL_TASKS: {
  id: ModelTask;
  label: string;
  description: string;
  kind: ModelKind;
}[] = [
  {
    description:
      "Rewrites your message as one clear question when it needs it. A small, fast model is enough.",
    id: "query",
    kind: "text",
    label: "Query",
  },
  {
    description:
      "Decides which earlier messages the answer needs. A small, fast model is enough.",
    id: "contextManagement",
    kind: "text",
    label: "Context",
  },
  {
    description: "Writes the answer you see in the chat.",
    id: "answer",
    kind: "text",
    label: "Answer",
  },
  {
    description: "Reads topology images and screenshots you attach.",
    id: "visionDescription",
    kind: "vision",
    label: "Vision",
  },
];

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

// Plain model ids from before models were picked per step; the chat still
// reads "chat-model" on load
const MODEL_COOKIES: Partial<Record<ModelTask, string>> = {
  answer: "chat-model",
  visionDescription: "vision-model",
};

const AGENTS_COOKIE = "agent-settings";
const DIAGRAM_COOKIE = "diagram-generation";
const RERANKER_COOKIE = "reranker";
const HYBRID_SEARCH_COOKIE = "hybrid-search";
const CHUNK_COUNT_COOKIE = "chunk-count";

// How many knowledge base chunks the answer is written from
export const CHUNK_COUNT_RANGE = { max: 20, min: 1 };
const DEFAULT_CHUNK_COUNT = 5;

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

// Where a model runs: through the AI Gateway, or on one of the self-hosted
// servers the backend is set up with (it lists those models at GET /models).
export type ModelSource = "api" | "self-hosted";

export type ModelChoice = {
  source: ModelSource;
  modelId: string;
};

// Answer and Vision description keep the cookies of the old Text and Vision
// settings, so choices made there carry over
const CHOICE_COOKIES: Record<ModelTask, string> = {
  answer: "text-model-choice",
  contextManagement: "context-model-choice",
  query: "query-model-choice",
  visionDescription: "vision-model-choice",
};

// Nothing picked yet: the backend uses its default model for that step
export function getModelChoice(task: ModelTask): ModelChoice | undefined {
  const raw = readCookie(CHOICE_COOKIES[task]);
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
  const plainCookie = MODEL_COOKIES[task];
  const plainModelId = plainCookie ? readCookie(plainCookie) : undefined;
  return plainModelId ? { modelId: plainModelId, source: "api" } : undefined;
}

export function setModelChoice(task: ModelTask, choice: ModelChoice) {
  writeCookie(CHOICE_COOKIES[task], JSON.stringify(choice));
  const plainCookie = MODEL_COOKIES[task];
  if (plainCookie && choice.source === "api") {
    writeCookie(plainCookie, choice.modelId);
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

// Whether knowledge base results are re-ordered by a reranker before answering
export function getRerankerEnabled(): boolean {
  return readCookie(RERANKER_COOKIE) !== "false";
}

export function setRerankerEnabled(enabled: boolean) {
  writeCookie(RERANKER_COOKIE, String(enabled));
}

export function getHybridSearchEnabled(): boolean {
  return readCookie(HYBRID_SEARCH_COOKIE) !== "false";
}

export function setHybridSearchEnabled(enabled: boolean) {
  writeCookie(HYBRID_SEARCH_COOKIE, String(enabled));
}

export function getChunkCount(): number {
  const count = Number(readCookie(CHUNK_COUNT_COOKIE));
  return Number.isInteger(count) &&
    count >= CHUNK_COUNT_RANGE.min &&
    count <= CHUNK_COUNT_RANGE.max
    ? count
    : DEFAULT_CHUNK_COUNT;
}

export function setChunkCount(count: number) {
  writeCookie(CHUNK_COUNT_COOKIE, String(count));
}
