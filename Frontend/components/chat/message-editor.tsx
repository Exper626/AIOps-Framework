"use client";

import type { UseChatHelpers } from "@ai-sdk/react";
import { deleteTrailingMessages } from "@/app/(chat)/actions";
import type { ChatMessage } from "@/lib/types";

export async function submitEditedMessage({
  message,
  text,
  setMessages,
  regenerate,
}: {
  message: ChatMessage;
  text: string;
  setMessages: UseChatHelpers<ChatMessage>["setMessages"];
  regenerate: UseChatHelpers<ChatMessage>["regenerate"];
}) {
  await deleteTrailingMessages({ id: message.id });

  setMessages((messages) => {
    const index = messages.findIndex((m) => m.id === message.id);
    if (index === -1) {
      return messages;
    }

    return [
      ...messages.slice(0, index),
      // Attached images and diagrams stay with the edited question
      {
        ...message,
        parts: [
          ...message.parts.filter(
            (part) => part.type === "file" || part.type === "data-diagram"
          ),
          { text, type: "text" as const },
        ],
      },
    ];
  });

  regenerate();
}

// Throws away an answer and asks the question before it again
export async function retryAssistantMessage({
  message,
  messages,
  setMessages,
  regenerate,
}: {
  message: ChatMessage;
  messages: ChatMessage[];
  setMessages: UseChatHelpers<ChatMessage>["setMessages"];
  regenerate: UseChatHelpers<ChatMessage>["regenerate"];
}) {
  const index = messages.findIndex((m) => m.id === message.id);
  const question = messages.slice(0, index).findLast((m) => m.role === "user");

  if (index === -1 || !question) {
    return;
  }

  // The question is deleted too because the chat route saves it again when
  // it is re-sent
  await deleteTrailingMessages({ id: question.id });

  setMessages(messages.slice(0, messages.indexOf(question) + 1));

  regenerate();
}
