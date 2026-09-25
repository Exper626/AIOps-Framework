import { memo, useCallback } from "react";
import { toast } from "sonner";
import { useCopyToClipboard } from "usehooks-ts";
import type { ChatMessage } from "@/lib/types";
import {
  MessageAction as Action,
  MessageActions as Actions,
} from "../ai-elements/message";
import { CopyIcon, PencilEditIcon, UndoIcon } from "./icons";

export function PureMessageActions({
  message,
  isLoading,
  onEdit,
  onRetry,
}: {
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
    // Only the latest answer has "Try again", so it moves when a new one arrives
    if (Boolean(prevProps.onRetry) !== Boolean(nextProps.onRetry)) {
      return false;
    }

    return true;
  }
);
