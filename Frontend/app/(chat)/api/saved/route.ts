import { z } from "zod";
import { auth } from "@/app/(auth)/auth";
import {
  deleteSavedResponse,
  getChatById,
  getMessagesByChatId,
  getSavedResponsesByUserId,
  saveResponse,
} from "@/lib/db/queries";
import type { DBMessage } from "@/lib/db/schema";
import { ChatbotError } from "@/lib/errors";

const saveSchema = z.object({
  chatId: z.uuid(),
  messageId: z.uuid(),
});

type Part = { type?: string; text?: string };

const QUESTION_LENGTH = 300;

// The question the answer replied to, used as the saved response's title
function questionBefore(messages: DBMessage[], index: number) {
  const asked = messages.slice(0, index).findLast((m) => m.role === "user");
  const parts = (asked?.parts ?? []) as Part[];
  const text = parts
    .filter((part) => part.type === "text")
    .map((part) => part.text ?? "")
    .join(" ")
    .trim();

  if (text) {
    return text.slice(0, QUESTION_LENGTH);
  }
  if (parts.some((part) => part.type === "data-diagram")) {
    return "Network diagram";
  }
  if (parts.some((part) => part.type === "file")) {
    return "Image";
  }
  return "Saved response";
}

export async function GET() {
  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  const saved = await getSavedResponsesByUserId({ userId: session.user.id });

  return Response.json(saved, { status: 200 });
}

export async function POST(request: Request) {
  let body: z.infer<typeof saveSchema>;

  try {
    body = saveSchema.parse(await request.json());
  } catch {
    return new ChatbotError(
      "bad_request:api",
      "Parameters chatId and messageId are required."
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  const chat = await getChatById({ id: body.chatId });

  if (!chat) {
    return new ChatbotError("not_found:chat").toResponse();
  }

  if (chat.userId !== session.user.id) {
    return new ChatbotError("forbidden:chat").toResponse();
  }

  const messages = await getMessagesByChatId({ id: body.chatId });
  const index = messages.findIndex((m) => m.id === body.messageId);

  if (index === -1 || messages[index].role !== "assistant") {
    return new ChatbotError("not_found:chat").toResponse();
  }

  await saveResponse({
    chatId: body.chatId,
    messageId: body.messageId,
    parts: (messages[index].parts as Part[]).filter(
      (part) => part.type !== "data-debug"
    ),
    question: questionBefore(messages, index),
    userId: session.user.id,
  });

  return Response.json({ saved: true }, { status: 200 });
}

export async function DELETE(request: Request) {
  const messageId = new URL(request.url).searchParams.get("messageId");

  if (!messageId) {
    return new ChatbotError(
      "bad_request:api",
      "Parameter messageId is required."
    ).toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  await deleteSavedResponse({ messageId, userId: session.user.id });

  return Response.json({ saved: false }, { status: 200 });
}
