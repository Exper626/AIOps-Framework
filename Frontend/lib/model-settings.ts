import {
  DEFAULT_CHAT_MODEL,
  DEFAULT_CONTEXT_MODEL,
  DEFAULT_QUERY_MODEL,
  DEFAULT_VISION_MODEL,
} from "@/lib/ai/models";

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
      "Rewrites your message as clear questions and splits multi-part messages. A small, fast model is enough.",
    id: "query",
    kind: "text",
    label: "Query",
  },
  {
    description:
      "Decides which earlier messages each question needs. A small, fast model is enough.",
    id: "contextManagement",
    kind: "text",
    label: "Context management",
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
    label: "Vision description",
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

const MODEL_DEFAULTS: Record<ModelTask, string> = {
  answer: DEFAULT_CHAT_MODEL,
  contextManagement: DEFAULT_CONTEXT_MODEL,
  query: DEFAULT_QUERY_MODEL,
  visionDescription: DEFAULT_VISION_MODEL,
};

const AGENTS_COOKIE = "agent-settings";
const DIAGRAM_COOKIE = "diagram-generation";
const RERANKER_COOKIE = "reranker";

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

export function getModelChoice(task: ModelTask): ModelChoice {
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
  return { modelId: plainModelId ?? MODEL_DEFAULTS[task], source: "api" };
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
