"use client";

import type { UseChatHelpers } from "@ai-sdk/react";
import { useCallback, useEffect, useRef } from "react";
import { toast } from "sonner";
import type { NetworkDiagram } from "@/lib/diagram";
import type { ChatMessage } from "@/lib/types";
import { NetworkDiagramEditor } from "./network-diagram";

const SAVE_DELAY_MS = 800;

// A diagram in a message; changes are saved with the chat a moment after the
// user stops editing
export function DiagramPart({
  chatId,
  diagram,
  messageId,
  partId,
  readOnly,
  setMessages,
}: {
  chatId: string;
  diagram: NetworkDiagram;
  messageId: string;
  partId?: string;
  readOnly: boolean;
  setMessages: UseChatHelpers<ChatMessage>["setMessages"];
}) {
  const pending = useRef<NetworkDiagram | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);

  const persist = async (next: NetworkDiagram) => {
    setMessages((messages) =>
      messages.map((message) =>
        message.id === messageId
          ? {
              ...message,
              parts: message.parts.map((part) =>
                part.type === "data-diagram" && part.id === partId
                  ? { ...part, data: next }
                  : part
              ),
            }
          : message
      )
    );

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/diagram`,
      {
        body: JSON.stringify({ chatId, diagram: next, partId }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      }
    ).catch(() => null);

    if (!response?.ok) {
      toast.error("Couldn't save the diagram changes. Please try again.");
    }
  };
  const persistRef = useRef(persist);
  persistRef.current = persist;

  const flush = useCallback(() => {
    clearTimeout(timer.current);
    const next = pending.current;
    pending.current = null;

    if (next) {
      persistRef.current(next);
    }
  }, []);

  const save = useCallback(
    (next: NetworkDiagram) => {
      pending.current = next;
      clearTimeout(timer.current);
      timer.current = setTimeout(flush, SAVE_DELAY_MS);
    },
    [flush]
  );

  // An edit made just before leaving the chat is still saved
  useEffect(() => flush, [flush]);

  return (
    <NetworkDiagramEditor
      diagram={diagram}
      onChange={save}
      readOnly={readOnly || !partId}
    />
  );
}
