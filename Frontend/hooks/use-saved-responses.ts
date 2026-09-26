"use client";

import { useCallback, useMemo } from "react";
import useSWR from "swr";
import type { ChatMessage } from "@/lib/types";
import { fetcher } from "@/lib/utils";

export type SavedResponseItem = {
  id: string;
  chatId: string;
  // null once the chat has been deleted; the saved copy stays
  chatTitle: string | null;
  messageId: string;
  question: string;
  parts: ChatMessage["parts"];
  createdAt: string;
};

const SAVED_URL = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/api/saved`;

async function send(url: string, init: RequestInit) {
  const response = await fetch(url, init);

  if (!response.ok) {
    throw new Error("The saved responses couldn't be updated");
  }
}

// One list shared by the bookmark buttons and the Saved responses page
export function useSavedResponses() {
  const { data, isLoading, mutate } = useSWR<SavedResponseItem[]>(
    SAVED_URL,
    fetcher,
    { revalidateOnFocus: false }
  );

  const savedIds = useMemo(
    () => new Set((data ?? []).map((item) => item.messageId)),
    [data]
  );

  const save = useCallback(
    async (chatId: string, messageId: string) => {
      await send(SAVED_URL, {
        body: JSON.stringify({ chatId, messageId }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      await mutate();
    },
    [mutate]
  );

  const remove = useCallback(
    async (messageId: string) => {
      await mutate(
        async (current) => {
          await send(`${SAVED_URL}?messageId=${messageId}`, {
            method: "DELETE",
          });
          return (current ?? []).filter((item) => item.messageId !== messageId);
        },
        {
          optimisticData: (current) =>
            (current ?? []).filter((item) => item.messageId !== messageId),
          revalidate: false,
          rollbackOnError: true,
        }
      );
    },
    [mutate]
  );

  return { isLoading, remove, responses: data ?? [], save, savedIds };
}
