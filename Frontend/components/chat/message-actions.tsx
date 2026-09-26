import { BookmarkIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { memo, useCallback, useState } from "react";
import { toast } from "sonner";
import { useCopyToClipboard } from "usehooks-ts";
import { useSavedResponses } from "@/hooks/use-saved-responses";
import type { ChatMessage } from "@/lib/types";
import { cn } from "@/lib/utils";
import {
  MessageAction as Action,
  MessageActions as Actions,
} from "../ai-elements/message";
import { CopyIcon, PencilEditIcon, UndoIcon } from "./icons";

// Saves the answer to "Saved responses", or takes it out again
function SaveResponseAction({
  chatId,
  messageId,
}: {
  chatId: string;
  messageId: string;
}) {
  const router = useRouter();
  const { remove, save, savedIds } = useSavedResponses();
  const [busy, setBusy] = useState(false);
  const isSaved = savedIds.has(messageId);

  const handleClick = useCallback(async () => {
    setBusy(true);

    try {
      if (isSaved) {
        await remove(messageId);
        toast.success("Removed from saved responses");
      } else {
        await save(chatId, messageId);
        toast.success("Response saved", {
          action: { label: "View", onClick: () => router.push("/saved") },
        });
      }
    } catch {
      toast.error("Couldn't update your saved responses. Please try again.");
    } finally {
      setBusy(false);
    }
  }, [chatId, isSaved, messageId, remove, router, save]);

  return (
    <Action
      aria-pressed={isSaved}
      className={cn(
        "text-muted-foreground/50 hover:text-foreground",
        isSaved && "text-foreground"
      )}
      data-testid="message-save"
      disabled={busy}
      onClick={handleClick}
      tooltip={isSaved ? "Remove from saved" : "Save response"}
    >
      <BookmarkIcon className={cn(isSaved && "fill-current")} />
    </Action>
  );
}

export function PureMessageActions({
  chatId,
  message,
  isLoading,
  onEdit,
  onRetry,
}: {
  chatId: string;
  message: ChatMessage;
  isLoading: boolean;
  onEdit?: () => void;
  onRetry?: () => Promise<void>;
}) {
  const [_, copyToClipboard] = useCopyToClipboard();

  const textFromParts = message.parts
    ?.filter((part) => part.type === "text")
    .map((part) => part.text)
    .join("\n")
    .trim();

  const handleCopy = useCallback(async () => {
    if (!textFromParts) {
      toast.error("There's no text to copy!");
      return;
    }

    await copyToClipboard(textFromParts);
    toast.success("Copied to clipboard!");
  }, [copyToClipboard, textFromParts]);

  const handleRetry = useCallback(async () => {
    try {
      await onRetry?.();
    } catch {
      toast.error("Couldn't retry this response. Please try again.");
    }
  }, [onRetry]);

  if (isLoading) {
    return null;
  }

  if (message.role === "user") {
    return (
      <Actions className="-mr-0.5 justify-end opacity-0 transition-opacity duration-150 group-hover/message:opacity-100">
        <div className="flex items-center gap-0.5">
          {onEdit ? (
            <Action
              className="size-7 text-muted-foreground/50 hover:text-foreground"
              data-testid="message-edit-button"
              onClick={onEdit}
              tooltip="Edit"
            >
              <PencilEditIcon />
            </Action>
          ) : null}
          <Action
            className="size-7 text-muted-foreground/50 hover:text-foreground"
            onClick={handleCopy}
            tooltip="Copy"
          >
            <CopyIcon />
          </Action>
        </div>
      </Actions>
    );
  }

  return (
    <Actions className="-ml-0.5 opacity-0 transition-opacity duration-150 group-hover/message:opacity-100">
      <Action
        className="text-muted-foreground/50 hover:text-foreground"
        onClick={handleCopy}
        tooltip="Copy"
      >
        <CopyIcon />
      </Action>

      <SaveResponseAction chatId={chatId} messageId={message.id} />

      {onRetry ? (
        <Action
          className="text-muted-foreground/50 hover:text-foreground"
          data-testid="message-retry"
          onClick={handleRetry}
          tooltip="Try again"
        >
          <UndoIcon />
        </Action>
      ) : null}
    </Actions>
  );
}

export const MessageActions = memo(
  PureMessageActions,
  (prevProps, nextProps) => {
    if (prevProps.isLoading !== nextProps.isLoading) {
      return false;
    }
    if (prevProps.message.id !== nextProps.message.id) {
      return false;
    }
    // Only the latest answer has "Try again", so it moves when a new one arrives
    if (Boolean(prevProps.onRetry) !== Boolean(nextProps.onRetry)) {
      return false;
    }

    return true;
  }
);
