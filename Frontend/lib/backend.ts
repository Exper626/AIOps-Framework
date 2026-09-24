export type BackendChatResult = {
  message: string;
  debug?: unknown;
};

export type BackendProgressEvent = {
  phase: "context" | "query" | "router" | "vector" | "sql" | "answer";
  message: string;
  modelId?: string;
  modelName?: string;
};

// One piece of the answer as the model writes it
type BackendDeltaEvent = {
  phase: "delta";
  delta: string;
};

type BackendDoneEvent = {
  phase: "done";
  message: string;
  debug?: unknown;
};

type BackendErrorEvent = {
  phase: "error";
  error: string;
  status?: number;
};

type BackendStreamEvent =
  | BackendProgressEvent
  | BackendDeltaEvent
  | BackendDoneEvent
  | BackendErrorEvent;

export type HistoryMessage = {
  role: "user" | "assistant";
  content: string;
};

export async function callBackend(
  message: string,
  model: string,
  onProgress?: (event: BackendProgressEvent) => void,
  history: HistoryMessage[] = [],
  sessionId?: string,
  options: {
    visionModel?: string;
    agents?: Record<string, boolean>;
    diagramGeneration?: boolean;
    textSource?: "api" | "self-hosted";
    textBaseUrl?: string;
    visionSource?: "api" | "self-hosted";
    visionBaseUrl?: string;
    onDelta?: (delta: string) => void;
  } = {},
): Promise<BackendChatResult> {
  const backendUrl = process.env.BACKEND_URL;

  if (!backendUrl) {
    throw new Error("BACKEND_URL is not configured");
  }

  const response = await fetch(`${backendUrl}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      model,
      history,
      session_id: sessionId ?? null,
      vision_model: options.visionModel ?? null,
      agents: options.agents ?? {},
      diagram_generation: options.diagramGeneration ?? true,
      // "api" = call through the Vercel AI Gateway, "self-hosted" = call the
      // OpenAI-compatible server at *_base_url
      text_source: options.textSource ?? "api",
      text_base_url: options.textBaseUrl ?? null,
      vision_source: options.visionSource ?? "api",
      vision_base_url: options.visionBaseUrl ?? null,
    }),
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(
      `Backend request failed: ${response.status} ${errorText}`
    );
  }

  if (!response.body) {
    throw new Error("Backend response had no body to stream");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalResult: BackendChatResult | null = null;

  const handleLine = (line: string) => {
    const trimmed = line.trim();
    if (!trimmed) {
      return;
    }

    const event = JSON.parse(trimmed) as BackendStreamEvent;

    if (event.phase === "error") {
      throw new Error(event.error);
    }

    if (event.phase === "delta") {
      options.onDelta?.(event.delta);
      return;
    }

    if (event.phase === "done") {
      finalResult = { debug: event.debug, message: event.message };
      return;
    }

    onProgress?.(event);
  };

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        handleLine(line);
      }
    }

    buffer += decoder.decode();
    if (buffer.trim()) {
      handleLine(buffer);
    }
  } finally {
    reader.releaseLock();
  }

  if (!finalResult) {
    throw new Error("Backend stream ended without a final response");
  }

  return finalResult;
}