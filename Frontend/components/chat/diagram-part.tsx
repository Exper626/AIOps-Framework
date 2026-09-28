"use client";

import type { UseChatHelpers } from "@ai-sdk/react";
import { DownloadIcon, PencilIcon } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { diagramData, type NetworkDiagram } from "@/lib/diagram";
import type { ChatMessage } from "@/lib/types";
import { Button } from "../ui/button";
import { NetworkDiagramEditor } from "./network-diagram";

const SAVE_DELAY_MS = 800;
const DIAGRAM_API = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/diagram`;

// An answer's diagram as the backend drew it with Graphviz
export function DiagramImage({ diagram }: { diagram: NetworkDiagram }) {
  return (
    <picture className="block w-fit max-w-full overflow-hidden rounded-xl border border-border/50 bg-white">
      <img
        alt={`Network diagram: ${diagram.devices.map((device) => device.name).join(", ")}`}
        className="block h-auto max-h-[600px] max-w-full object-contain"
        src={diagram.image}
      />
    </picture>
  );
}

// A diagram in a message. An answer's picture opens in the editor with Edit
// and is redrawn with Done; changes are saved with the chat a moment after the
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
  const editable = !readOnly && Boolean(partId);
  const [editing, setEditing] = useState(false);
  const [drawing, setDrawing] = useState(false);
  const pending = useRef<NetworkDiagram | null>(null);
  // The last edit since Edit was clicked, redrawn on Done
  const edited = useRef<NetworkDiagram | null>(null);
  const saving = useRef<Promise<unknown>>(Promise.resolve());
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);

  const showInChat = useCallback(
    (next: NetworkDiagram) =>
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
      ),
    [messageId, partId, setMessages]
  );

  const persist = async (next: NetworkDiagram) => {
    showInChat(next);

    const request = fetch(DIAGRAM_API, {
      body: JSON.stringify({ chatId, diagram: next, partId }),
      headers: { "Content-Type": "application/json" },
      method: "POST",
    }).catch(() => null);
    saving.current = request;
    const response = await request;

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
      edited.current = next;
      clearTimeout(timer.current);
      timer.current = setTimeout(flush, SAVE_DELAY_MS);
    },
    [flush]
  );

  // An edit made just before leaving the chat is still saved
  useEffect(() => flush, [flush]);

  const startEditing = useCallback(() => {
    edited.current = null;
    setEditing(true);
  }, []);

  // Redraws the picture with the edits and saves both; without edits the
  // picture stays as it was
  const finishEditing = useCallback(async () => {
    const next = edited.current;

    if (!next) {
      setEditing(false);
      return;
    }

    clearTimeout(timer.current);
    pending.current = null;
    setDrawing(true);

    // A save still on its way (without the picture) must not land after this one
    await saving.current;

    const response = await fetch(DIAGRAM_API, {
      body: JSON.stringify({
        chatId,
        diagram: diagramData(next),
        draw: true,
        partId,
      }),
      headers: { "Content-Type": "application/json" },
      method: "POST",
    }).catch(() => null);
    const result = (await response?.json().catch(() => null)) as {
      error?: string;
      image?: string;
    } | null;

    setDrawing(false);

    if (!(response?.ok && result?.image)) {
      toast.error(
        result?.error ?? "Couldn't redraw the picture. Please try again."
      );
      return;
    }

    edited.current = null;
    showInChat({ ...diagramData(next), image: result.image });
    setEditing(false);
  }, [chatId, partId, showInChat]);

  if (diagram.image && !(editing && editable)) {
    return (
      <div className="flex flex-col items-start gap-1">
        <DiagramImage diagram={diagram} />
        <div className="flex gap-0.5">
          {editable ? (
            <Button
              className="h-7 gap-1 px-2 text-muted-foreground text-xs"
              data-testid="diagram-edit"
              onClick={startEditing}
              size="sm"
              variant="ghost"
            >
              <PencilIcon className="size-3.5" />
              Edit
            </Button>
          ) : null}
          <Button
            asChild
            className="h-7 gap-1 px-2 text-muted-foreground text-xs"
            size="sm"
            variant="ghost"
          >
            <a download="network-diagram.png" href={diagram.image}>
              <DownloadIcon className="size-3.5" />
              Download
            </a>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <NetworkDiagramEditor
      diagram={diagram}
      drawing={drawing}
      onChange={save}
      onDone={editing && editable ? finishEditing : undefined}
      readOnly={!editable}
    />
  );
}
