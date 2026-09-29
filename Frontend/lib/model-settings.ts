// Choices from the Settings dialog, stored in cookies so both the sidebar
// (settings) and the chat (sending messages) can read them.

// Each step of the answering pipeline can use its own model
export type ModelTask =
  | "router"
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
    description: "Reads each message first and plans which steps it needs.",
    id: "router",
    kind: "text",
    label: "Router",
  },
  {
    description:
      "Rewrites your message as one clear question when it needs it.",
    id: "query",
    kind: "text",
    label: "Query",
  },
  {
    description: "Decides which earlier messages the answer needs.",
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

// The steps each message goes through, in order, shown in Settings → Agents.
// The router plans which of the four tasks run: image description, retrieval,
// text generation and image generation.
export type AgentId =
  | "router"
  | "vision"
  | "query"
  | "context"
  | "retrievalAgent"
  | "knowledgeBase"
  | "answer"
  | "diagram"
  | "memory";

export const AGENTS: { id: AgentId; name: string; description: string }[] = [
  {
    description:
      "Reads each message first and plans its tasks: image description when you attach an image, retrieval for questions about specific devices, text generation for every reply, and image generation for network diagrams.",
    id: "router",
    name: "Router",
  },
  {
    description:
      "Image description: reads the topology images and screenshots you attach, so the later steps can use them. Runs whenever a message has an image.",
    id: "vision",
    name: "Vision",
  },
  {
    description:
      'Rewrites your message as one clear question, so short follow-ups like "and the second switch?" make sense on their own.',
    id: "query",
    name: "Query",
  },
  {
    description:
      "Picks the earlier messages the answer needs, so long conversations stay focused. Only runs once there are earlier messages.",
    id: "context",
    name: "Context",
  },
  {
    description:
      "Knows how the knowledge base is organised (vendors, device types, folders and every device name) and turns your question into a search: which devices to fetch, which filters to use and what to search for. Runs before retrieval, with the Query model.",
    id: "retrievalAgent",
    name: "Retrieval agent",
  },
  {
    description:
      "Retrieval: searches the device knowledge base for the devices you asked about or that appear in your image. Runs when the router plans it.",
    id: "knowledgeBase",
    name: "Knowledge base search",
  },
  {
    description:
      "Text generation: writes the reply you see, from your question, the earlier messages it needs, your image and any passages found.",
    id: "answer",
    name: "Answer",
  },
  {
    description:
      "Image generation: works out the network (devices and cables) from the answer, your image or drawing, and the devices found, and Graphviz draws it as a picture. When you only asked for a picture, it gets a one or two sentence caption instead of an answer.",
    id: "diagram",
    name: "Diagram",
  },
  {
    description:
      "Remembers you across chats with Mem0: before each message it looks up what it knows about you (your name, preferences and networks), and after the answer it saves new facts, replaces ones you changed and forgets what you ask it to. Runs with the Context model; see and delete the memories in Settings → Memory.",
    id: "memory",
    name: "Memory",
  },
];

// Plain model ids from before models were picked per step; the chat still
// reads "chat-model" on load
const MODEL_COOKIES: Partial<Record<ModelTask, string>> = {
  answer: "chat-model",
  visionDescription: "vision-model",
};

const RERANKER_COOKIE = "reranker";
const HYBRID_SEARCH_COOKIE = "hybrid-search";
const CHUNK_COUNT_COOKIE = "chunk-count";
const MEMORY_COOKIE = "memory";

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
  router: "router-model-choice",
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

// Whether chats use and update what the assistant remembers about the user
export function getMemoryEnabled(): boolean {
  return readCookie(MEMORY_COOKIE) !== "false";
}

export function setMemoryEnabled(enabled: boolean) {
  writeCookie(MEMORY_COOKIE, String(enabled));
}
