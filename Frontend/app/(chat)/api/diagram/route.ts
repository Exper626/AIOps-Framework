import { z } from "zod";
import { auth } from "@/app/(auth)/auth";
import {
  getChatById,
  getMessagesByChatId,
  updateMessage,
} from "@/lib/db/queries";
import { ChatbotError } from "@/lib/errors";
import { diagramSchema } from "../chat/schema";

const saveDiagramSchema = z.object({
  chatId: z.uuid(),
  diagram: diagramSchema,
  partId: z.string().min(1).max(100),
});

type Part = { type?: string; id?: string };

const isDiagramPart = (part: Part, partId: string) =>
  part.type === "data-diagram" && part.id === partId;

// Saves an edited diagram into the message it came with, so the chat shows it
// as it was left and later questions are answered with it
export async function POST(request: Request) {
  let body: z.infer<typeof saveDiagramSchema>;

  try {
    body = saveDiagramSchema.parse(await request.json());
  } catch {
    return new ChatbotError(
      "bad_request:api",
      "Parameters chatId, partId and diagram are required."
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
  const message = messages.find((currentMessage) =>
    (currentMessage.parts as Part[]).some((part) =>
      isDiagramPart(part, body.partId)
    )
  );

  if (!message) {
    return new ChatbotError("not_found:chat").toResponse();
  }

  await updateMessage({
    id: message.id,
    parts: (message.parts as Part[]).map((part) =>
      isDiagramPart(part, body.partId) ? { ...part, data: body.diagram } : part
    ),
  });

  return Response.json({ saved: true }, { status: 200 });
}
