import { z } from "zod";
import { auth } from "@/app/(auth)/auth";
import { drawDiagramImage } from "@/lib/backend";
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
  // Also redraw the picture with Graphviz, when an answer's diagram was edited
  draw: z.boolean().optional(),
  partId: z.string().min(1).max(100),
});

type Part = { type?: string; id?: string };

const isDiagramPart = (part: Part, partId: string) =>
  part.type === "data-diagram" && part.id === partId;

// Saves an edited diagram into the message it came with, so the chat shows it
// as it was left and later questions are answered with it. With "draw", the
// backend redraws its picture first and the reply carries it
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

  let image: string | undefined;

  if (body.draw) {
    try {
      image = await drawDiagramImage(body.diagram);
    } catch (error) {
      const reason = error instanceof Error ? error.message : "unknown error";
      return Response.json(
        { error: `Couldn't redraw the picture: ${reason}` },
        { status: 502 }
      );
    }
  }

  const data = image ? { ...body.diagram, image } : body.diagram;

  await updateMessage({
    id: message.id,
    parts: (message.parts as Part[]).map((part) =>
      isDiagramPart(part, body.partId) ? { ...part, data } : part
    ),
  });

  return Response.json({ image, saved: true }, { status: 200 });
}
