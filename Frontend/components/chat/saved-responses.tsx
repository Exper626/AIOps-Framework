"use client";

import {
  ArrowLeftIcon,
  BookmarkIcon,
  CopyIcon,
  MessageSquareIcon,
  NetworkIcon,
  PanelLeftIcon,
  Trash2Icon,
} from "lucide-react";
import Link from "next/link";
import { useCallback, useState } from "react";
import { toast } from "sonner";
import { useCopyToClipboard } from "usehooks-ts";
import {
  type SavedResponseItem,
  useSavedResponses,
} from "@/hooks/use-saved-responses";
import { sanitizeText } from "@/lib/utils";
import { MessageContent, MessageResponse } from "../ai-elements/message";
import { Button } from "../ui/button";
import { useSidebar } from "../ui/sidebar";
import { Skeleton } from "../ui/skeleton";
import { NetworkDiagramEditor } from "./network-diagram";

const MARKDOWN_MARKS = /[#*_`>|[\]-]+/g;
const SPACES = /\s+/g;

function answerText(item: SavedResponseItem) {
  return item.parts
    .filter((part) => part.type === "text")
    .map((part) => part.text)
    .join("\n\n")
    .trim();
}

function hasDiagram(item: SavedResponseItem) {
  return item.parts.some((part) => part.type === "data-diagram");
}

function preview(item: SavedResponseItem) {
  return answerText(item)
    .replace(MARKDOWN_MARKS, " ")
    .replace(SPACES, " ")
    .trim()
    .slice(0, 240);
}

function savedOn(item: SavedResponseItem) {
  return new Date(item.createdAt).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function SavedCard({
  item,
  onOpen,
}: {
  item: SavedResponseItem;
  onOpen: (id: string) => void;
}) {
  const handleClick = useCallback(() => onOpen(item.id), [item.id, onOpen]);

  return (
    <button
      className="flex w-full flex-col gap-1.5 rounded-xl border border-border/60 bg-card px-4 py-3 text-left transition-colors hover:bg-muted/60"
      data-testid="saved-response-card"
      onClick={handleClick}
      type="button"
    >
      <div className="flex items-start justify-between gap-3">
        <span className="line-clamp-2 font-medium text-[15px] leading-snug">
          {item.question}
        </span>
        <span className="shrink-0 pt-0.5 text-muted-foreground text-xs">
          {savedOn(item)}
        </span>
      </div>
      {preview(item) ? (
        <p className="line-clamp-2 text-muted-foreground text-sm leading-relaxed">
          {preview(item)}
        </p>
      ) : null}
      {hasDiagram(item) ? (
        <span className="inline-flex items-center gap-1 text-muted-foreground text-xs">
          <NetworkIcon className="size-3" />
          Includes a diagram
        </span>
      ) : null}
    </button>
  );
}

function SavedResponseView({
  item,
  onBack,
}: {
  item: SavedResponseItem;
  onBack: () => void;
}) {
  const { remove } = useSavedResponses();
  const [_, copyToClipboard] = useCopyToClipboard();

  const handleCopy = useCallback(async () => {
    await copyToClipboard(answerText(item));
    toast.success("Copied to clipboard!");
  }, [copyToClipboard, item]);

  const handleRemove = useCallback(async () => {
    try {
      await remove(item.messageId);
      toast.success("Removed from saved responses");
      onBack();
    } catch {
      toast.error("Couldn't remove it. Please try again.");
    }
  }, [item.messageId, onBack, remove]);

  return (
    <article className="flex flex-col gap-5" data-testid="saved-response">
      <button
        className="inline-flex w-fit items-center gap-1.5 text-muted-foreground text-sm transition-colors hover:text-foreground"
        onClick={onBack}
        type="button"
      >
        <ArrowLeftIcon className="size-4" />
        Saved responses
      </button>

      <header className="flex flex-col gap-2">
        <h1 className="font-semibold text-xl leading-snug">{item.question}</h1>
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-muted-foreground text-xs">
          <span>Saved {savedOn(item)}</span>
          {item.chatTitle ? (
            <Link
              className="inline-flex items-center gap-1 hover:text-foreground"
              href={`/chat/${item.chatId}`}
            >
              <MessageSquareIcon className="size-3" />
              Open chat
            </Link>
          ) : (
            <span>The chat was deleted</span>
          )}
        </div>
      </header>

      <div className="flex flex-col gap-4">
        {item.parts.map((part, index) => {
          const key = `${item.id}-${index}`;

          if (part.type === "text") {
            return (
              <MessageContent className="text-[15px] leading-[1.65]" key={key}>
                <MessageResponse>{sanitizeText(part.text)}</MessageResponse>
              </MessageContent>
            );
          }

          if (part.type === "data-diagram") {
            return (
              <NetworkDiagramEditor diagram={part.data} key={key} readOnly />
            );
          }

          return null;
        })}
      </div>

      <div className="flex gap-2 border-border/60 border-t pt-4">
        <Button onClick={handleCopy} size="sm" variant="outline">
          <CopyIcon className="size-3.5" />
          Copy
        </Button>
        <Button
          data-testid="saved-remove"
          onClick={handleRemove}
          size="sm"
          variant="outline"
        >
          <Trash2Icon className="size-3.5" />
          Remove from saved
        </Button>
      </div>
    </article>
  );
}

export function SavedResponses() {
  const { isLoading, responses } = useSavedResponses();
  const { toggleSidebar } = useSidebar();
  const [openId, setOpenId] = useState<string | null>(null);
  const open = responses.find((item) => item.id === openId);
  const closeResponse = useCallback(() => setOpenId(null), []);

  return (
    <div className="flex h-dvh w-full flex-col overflow-hidden bg-sidebar">
      <header className="flex h-14 items-center gap-2 px-3 md:hidden">
        <Button onClick={toggleSidebar} size="icon-sm" variant="ghost">
          <PanelLeftIcon className="size-4" />
        </Button>
      </header>

      <div className="relative min-h-0 flex-1 overflow-y-auto bg-background md:rounded-tl-[12px] md:border-border/40 md:border-t md:border-l">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8 md:px-6">
          {open ? (
            <SavedResponseView item={open} onBack={closeResponse} />
          ) : (
            <>
              <div className="flex flex-col gap-1">
                <h1 className="font-semibold text-xl">Saved responses</h1>
                <p className="text-muted-foreground text-sm">
                  Answers you saved from your chats.
                </p>
              </div>

              {isLoading ? (
                <div className="flex flex-col gap-3">
                  <Skeleton className="h-20 w-full rounded-xl" />
                  <Skeleton className="h-20 w-full rounded-xl" />
                  <Skeleton className="h-20 w-full rounded-xl" />
                </div>
              ) : null}

              {!isLoading && responses.length === 0 ? (
                <div
                  className="flex flex-col items-center gap-2 rounded-xl border border-border/60 border-dashed px-6 py-12 text-center"
                  data-testid="saved-empty"
                >
                  <BookmarkIcon className="size-6 text-muted-foreground" />
                  <p className="font-medium text-sm">No saved responses yet</p>
                  <p className="max-w-sm text-muted-foreground text-sm">
                    Hover over an answer and click the bookmark to keep it here.
                  </p>
                </div>
              ) : null}

              <div className="flex flex-col gap-3">
                {responses.map((item) => (
                  <SavedCard item={item} key={item.id} onOpen={setOpenId} />
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
