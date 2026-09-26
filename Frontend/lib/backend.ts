import type { NetworkDiagram } from "@/lib/diagram";
import type { ModelChoice } from "@/lib/model-settings";

export type BackendChatResult = {
  message: string;
  debug?: unknown;
};

export type BackendProgressEvent = {
  phase:
    | "vision"
    | "context"
    | "query"
    | "router"
    | "vector"
    | "sql"
    | "answer";
  message: string;
  modelId?: string;
  modelName?: string;
};

// One piece of the answer as the model writes it
type BackendDeltaEvent = {
  phase: "delta";
  delta: string;
};

// A network diagram the backend drew for the answer
type BackendDiagramEvent = {
  phase: "diagram";
  diagram: NetworkDiagram;
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
  debug?: unknown;
};

type BackendStreamEvent =
  | BackendProgressEvent
  | BackendDeltaEvent
  | BackendDiagramEvent
  | BackendDoneEvent
  | BackendErrorEvent;

export type BackendImage = {
  name: string;
  mediaType: string;
  url: string;
};

export type HistoryMessage = {
  role: "user" | "assistant";
  content: string;
  diagram?: NetworkDiagram;
};

const TRAILING_SLASHES = /\/+$/;

function toBackendModel(choice?: ModelChoice) {
  return choice ? { id: choice.modelId, source: choice.source } : null;
}

// BACKEND_URL without trailing slashes, which would turn /chat into //chat (a 404)
export function getBackendUrl(): string | undefined {
  return process.env.BACKEND_URL?.trim().replace(TRAILING_SLASHES, "") || undefined;
}

// FastAPI puts the reason in "detail": a string, or a list of validation errors
function readErrorDetail(body: string) {
  try {
    const { detail } = JSON.parse(body) as { detail?: unknown };

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item: { loc?: unknown[]; msg?: string }) => {
          const field = item.loc?.join(".") ?? "request";
          return `${field}: ${item.msg ?? "invalid value"}`;
        })
        .join("; ");
    }
  } catch {
    // Not JSON, so the raw text is used below
  }

  return body.trim().slice(0, 300) || "no details were returned";
}

// Turns a failed /chat response into a message that says what to fix
function describeBackendFailure(url: string, status: number, body: string) {
  const detail = readErrorDetail(body);

  if (status === 404) {
    return `The backend at ${url} has no /chat endpoint (404). Either the deployed backend is still running old code (redeploy it), or BACKEND_URL points to the wrong service.`;
  }

  if (status === 400 || status === 422) {
    return `The backend rejected the request (${status}): ${detail}`;
  }

  if (status === 502 || status === 503 || status === 504) {
    return `The backend at ${url} is down or still starting (${status}). Check its deployment logs.`;
  }

  if (status >= 500) {
    const reason = detail.endsWith(".") ? detail : `${detail}.`;
    return `The backend at ${url} failed (${status}): ${reason} Check the backend logs for details.`;
  }

  return `The backend at ${url} returned an error (${status}): ${detail}`;
}

export async function callBackend(
  message: string,
  // Models picked in Settings; a missing one means the backend's default
  answerModel: ModelChoice | undefined,
  onProgress?: (event: BackendProgressEvent) => void,
  history: HistoryMessage[] = [],
  sessionId?: string,
  options: {
    visionModel?: ModelChoice;
    // A diagram the user drew and sent with this message
    diagram?: NetworkDiagram;
    reranker?: boolean;
    hybridSearch?: boolean;
    chunkCount?: number;
    // Images attached to this message, as base64 data URLs
    images?: BackendImage[];
    routerModel?: ModelChoice;
    queryModel?: ModelChoice;
    contextModel?: ModelChoice;
    onDelta?: (delta: string) => void;
    onDiagram?: (diagram: NetworkDiagram) => void;
    onErrorDebug?: (debug: unknown) => void;
  } = {},
): Promise<BackendChatResult> {
  const backendUrl = getBackendUrl();

  if (!backendUrl) {
    throw new Error(
      "BACKEND_URL is not configured. Set it in the frontend's environment to the backend's base URL, e.g. https://your-backend.up.railway.app"
    );
  }

  const chatUrl = `${backendUrl}/chat`;
  let response: Response;

  try {
    response = await fetch(chatUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        history,
        session_id: sessionId ?? null,
        diagram: options.diagram ?? null,
        reranker: options.reranker ?? true,
        hybrid_search: options.hybridSearch,
        chunk_count: options.chunkCount,
        images: (options.images ?? []).map((image) => ({
          data_url: image.url,
          media_type: image.mediaType,
          name: image.name,
        })),
        router_model: toBackendModel(options.routerModel),
        answer_model: toBackendModel(answerModel),
        query_model: toBackendModel(options.queryModel),
        context_model: toBackendModel(options.contextModel),
        vision_model: toBackendModel(options.visionModel),
      }),
      cache: "no-store",
    });
  } catch (error) {
    // fetch hides the real reason (DNS, refused connection, TLS) in `cause`
    const reason =
      error instanceof Error && error.cause instanceof Error
        ? error.cause.message
        : String(error);

    throw new Error(
      `Could not connect to the backend at ${chatUrl} (${reason}). Check that the backend is running and that BACKEND_URL is correct.`,
      { cause: error }
    );
  }

  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(
      describeBackendFailure(chatUrl, response.status, errorText)
    );
  }

  if (!response.body) {
    throw new Error(`The backend at ${chatUrl} sent an empty response`);
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

    let event: BackendStreamEvent;

    try {
      event = JSON.parse(trimmed) as BackendStreamEvent;
    } catch (error) {
      throw new Error(
        `The backend sent something that isn't a JSON line: ${trimmed.slice(0, 200)}`,
        { cause: error }
      );
    }

    if (event.phase === "error") {
      // The trace says which step failed, so it is handed over before the error
      if (event.debug !== undefined) {
        options.onErrorDebug?.(event.debug);
      }
      throw new Error(event.error);
    }

    if (event.phase === "delta") {
      options.onDelta?.(event.delta);
      return;
    }

    if (event.phase === "diagram") {
      options.onDiagram?.(event.diagram);
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
    throw new Error(
      'The backend finished without sending an answer (no "done" event). If it replies with a single JSON object instead of streamed JSON lines, it is running old code.'
    );
  }

  return finalResult;
}