import { ipAddress } from "@vercel/functions";
import {
  createUIMessageStream,
  createUIMessageStreamResponse,
  generateId,
} from "ai";
import { checkBotId } from "botid/server";
import { after } from "next/server";
import { createResumableStreamContext } from "resumable-stream";
import { auth, type UserType } from "@/app/(auth)/auth";
import { entitlementsByUserType } from "@/lib/ai/entitlements";
import {
  allowedModelIds,
  allowedVisionModelIds,
  isAllowedModelId,
} from "@/lib/ai/models";
import {
  type BackendImage,
  callBackend,
  type HistoryMessage,
} from "@/lib/backend";
import {
  createStreamId,
  deleteChatById,
  getChatById,
  getMessageCountByUserId,
  getMessagesByChatId,
  saveChat,
  saveMessages,
  updateChatTitleById,
  updateMessage,
} from "@/lib/db/queries";
import type { DBMessage } from "@/lib/db/schema";
import type { NetworkDiagram } from "@/lib/diagram";
import { ChatbotError } from "@/lib/errors";
import type { ModelChoice } from "@/lib/model-settings";
import { checkIpRateLimit } from "@/lib/ratelimit";
import type { ChatMessage } from "@/lib/types";
import { convertToUIMessages, generateUUID } from "@/lib/utils";
import { generateTitleFromUserMessage } from "../../actions";
import { type PostRequestBody, postRequestBodySchema } from "./schema";

export const maxDuration = 60;

function describeError(error: unknown) {
  if (!(error instanceof Error)) {
    return String(error);
  }

  const cause = error.cause instanceof Error ? ` | Cause: ${error.cause.message}` : "";

  return `${error.name}: ${error.message}${cause}`;
}

function getMessageText(message?: ChatMessage) {
  return (
    message?.parts
      ?.filter((part) => part.type === "text")
      .map((part) => part.text)
      .join(" ")
      .trim() ?? ""
  );
}

// Images attached to a message, which are kept in it as base64 data URLs
function getMessageImages(message?: ChatMessage): BackendImage[] {
  return (
    message?.parts?.flatMap((part) =>
      part.type === "file" &&
      part.mediaType.startsWith("image/") &&
      part.url.startsWith("data:")
        ? [
            {
              mediaType: part.mediaType,
              name:
                (part as { name?: string }).name ?? part.filename ?? "image",
              url: part.url,
            },
          ]
        : []
    ) ?? []
  );
}

// The latest version of the diagram in a message, as edits are saved into it
function getMessageDiagram(message?: ChatMessage): NetworkDiagram | undefined {
  return message?.parts?.findLast((part) => part.type === "data-diagram")?.data;
}

function getLatestUserMessageText(messages: ChatMessage[]) {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    const currentMessage = messages[index];

    if (currentMessage.role !== "user") {
      continue;
    }

    const text = getMessageText(currentMessage);

    if (text) {
      return text;
    }
  }

  return "";
}

// The pipeline trace is shown once under the answer and never saved
function withoutTrace(parts: ChatMessage["parts"]) {
  return parts.filter((part) => part.type !== "data-debug");
}

function getStreamContext() {
  try {
    return createResumableStreamContext({ waitUntil: after });
  } catch {
    return null;
  }
}

export { getStreamContext };

export async function POST(request: Request) {
  let requestBody: PostRequestBody;

  console.log("ENV CHECK:", {
    BACKEND_URL: process.env.BACKEND_URL?.substring(0, 20),
    POSTGRES_URL: process.env.POSTGRES_URL ? "SET" : "MISSING",
    REDIS_URL: process.env.REDIS_URL ? "SET" : "MISSING",
  });



  try {
    const json = await request.json();
    requestBody = postRequestBodySchema.parse(json);
  } catch (error) {
    console.error("REQUEST PARSING ERROR:", error);
    return new ChatbotError("bad_request:api").toResponse();
  }

  try {
    const {
      id,
      message,
      messages,
      agents,
      chunkCount,
      diagramGeneration,
      hybridSearch,
      modelChoices,
      reranker,
      selectedVisibilityType,
    } = requestBody;

    const [botIdResult, session] = await Promise.all([
      checkBotId().catch(() => null),
      auth(),
    ]);

    if (botIdResult?.isBot) {
      return new ChatbotError("forbidden:api").toResponse();
    }

    if (!session?.user) {
      return new ChatbotError("unauthorized:chat").toResponse();
    }

    // Models picked in Settings. Self-hosted ones are checked by the backend
    // against its own list; API ones must exist on the AI Gateway. A step with
    // no usable pick is left out, and the backend uses its default model.
    const pickModel = async (
      choice: ModelChoice | undefined,
      allowed: Set<string>
    ) => {
      if (!choice || choice.source === "self-hosted") {
        return choice;
      }
      return (await isAllowedModelId(choice.modelId, allowed))
        ? choice
        : undefined;
    };
    const [answerModel, queryModel, contextModel, visionModel] =
      await Promise.all([
        pickModel(modelChoices?.answer, allowedModelIds),
        pickModel(modelChoices?.query, allowedModelIds),
        pickModel(modelChoices?.contextManagement, allowedModelIds),
        pickModel(modelChoices?.visionDescription, allowedVisionModelIds),
      ]);

    await checkIpRateLimit(ipAddress(request));

    const userType: UserType = session.user.type;

    const messageCount = await getMessageCountByUserId({
      differenceInHours: 1,
      id: session.user.id,
    });

    if (messageCount > entitlementsByUserType[userType].maxMessagesPerHour) {
      return new ChatbotError("rate_limit:chat").toResponse();
    }

    const isToolApprovalFlow = Boolean(messages);

    const chat = await getChatById({ id });
    let messagesFromDb: DBMessage[] = [];
    let titlePromise: Promise<string> | null = null;

    if (chat) {
      if (chat.userId !== session.user.id) {
        return new ChatbotError("forbidden:chat").toResponse();
      }

      messagesFromDb = await getMessagesByChatId({ id });
    } else if (message?.role === "user") {
      await saveChat({
        id,
        title: "New chat",
        userId: session.user.id,
        visibility: selectedVisibilityType,
      });

      titlePromise = generateTitleFromUserMessage({ message });
    }

    let uiMessages: ChatMessage[];

    if (isToolApprovalFlow && messages) {
      const dbMessages = convertToUIMessages(messagesFromDb);
      const approvalStates = new Map(
        messages.flatMap(
          (currentMessage) =>
            currentMessage.parts
              ?.filter(
                (part: Record<string, unknown>) =>
                  part.state === "approval-responded" ||
                  part.state === "output-denied"
              )
              .map((part: Record<string, unknown>) => [
                String(part.toolCallId ?? ""),
                part,
              ]) ?? []
        )
      );

      uiMessages = dbMessages.map((currentMessage) => ({
        ...currentMessage,
        parts: currentMessage.parts.map((part) => {
          if ("toolCallId" in part && approvalStates.has(String(part.toolCallId))) {
            return { ...part, ...approvalStates.get(String(part.toolCallId)) };
          }

          return part;
        }),
      })) as ChatMessage[];
    } else {
      uiMessages = [
        ...convertToUIMessages(messagesFromDb),
        message as ChatMessage,
      ];
    }

    if (message?.role === "user") {
      await saveMessages({
        messages: [
          {
            attachments: [],
            chatId: id,
            createdAt: new Date(),
            id: message.id,
            parts: message.parts,
            role: "user",
          },
        ],
      });
    }

    const stream = createUIMessageStream({
      execute: async ({ writer: dataStream }) => {
        // Gives the answer the id it is saved under, so the browser and the
        // database agree on it (saving a response looks it up by this id)
        dataStream.write({ type: "start" });

        const images = getMessageImages(message as ChatMessage | undefined);
        const drawnDiagram = getMessageDiagram(message as ChatMessage | undefined);
        // A message can be just an image or a diagram; the backend still
        // needs a question
        const userMessage =
          getMessageText(message as ChatMessage | undefined) ||
          (images.length > 0
            ? "Describe the network topology in the attached image."
            : drawnDiagram
              ? "Explain the network in the diagram I drew."
              : getLatestUserMessageText(uiMessages));

        if (!userMessage) {
          throw new Error("No user message was found to send to the backend");
        }

        console.log("RENDER REQUEST:", {
          message: userMessage,
          model: answerModel?.modelId ?? "backend default",
        });

        // Full history of this chat (excluding the current message), with
        // the diagrams as the user left them
        const history: HistoryMessage[] = uiMessages
          .slice(0, -1) // drop the current user message
          .flatMap((m) => {
            const text = getMessageText(m);
            const diagram = getMessageDiagram(m);
            if (!(text || diagram)) {
              return [];
            }
            return [
              {
                content: text,
                role: m.role as "user" | "assistant",
                ...(diagram ? { diagram } : {}),
              },
            ];
          });

        // The answer is shown piece by piece as the backend streams it
        const textId = generateUUID();
        let textStarted = false;
        let answerDiagram: NetworkDiagram | undefined;
        const writeDelta = (delta: string) => {
          if (!textStarted) {
            dataStream.write({ id: textId, type: "text-start" });
            textStarted = true;
          }
          dataStream.write({ delta, id: textId, type: "text-delta" });
        };

        const backendResponse = await callBackend(
          userMessage,
          answerModel,
          (event) => {
            dataStream.write({
              data: {
                message: event.message,
                modelId: event.modelId ?? "",
                modelName: event.modelName ?? "",
                phase: event.phase,
              },
              id: "pipeline-status",
              transient: true,
              type: "data-waiting-status",
            });
          },
          history,
          session?.user?.id,
          {
            agents: agents ?? {},
            diagramGeneration: diagramGeneration ?? true,
            contextModel,
            diagram: drawnDiagram,
            images,
            onDelta: writeDelta,
            onDiagram: (diagram) => {
              answerDiagram = diagram;
            },
            onErrorDebug: (debug) => {
              if (textStarted) {
                dataStream.write({ id: textId, type: "text-end" });
              }
              dataStream.write({
                data: debug,
                id: `debug-${textId}`,
                type: "data-debug",
              });
            },
            chunkCount,
            hybridSearch,
            queryModel,
            reranker: reranker ?? true,
            visionModel,
          },
        );

        console.log("RENDER RESPONSE:", backendResponse);

        if (
          !backendResponse ||
          typeof backendResponse.message !== "string" ||
          !backendResponse.message.trim()
        ) {
          throw new Error(
            "Backend returned an invalid response. Expected { message: string }"
          );
        }

        // A backend that doesn't stream sends the whole answer at the end
        if (!textStarted) {
          writeDelta(backendResponse.message);
        }

        dataStream.write({
          type: "text-end",
          id: textId,
        });

        // Saved with the answer; its id is how edits find it later
        if (answerDiagram) {
          dataStream.write({
            data: answerDiagram,
            id: `diagram-${textId}`,
            type: "data-diagram",
          });
        }

        if (backendResponse.debug) {
          dataStream.write({
            type: "data-debug",
            id: `debug-${textId}`,
            data: backendResponse.debug,
          });
        }

        if (titlePromise) {
          try {
            const title = await titlePromise;

            dataStream.write({
              data: title,
              type: "data-chat-title",
            });

            await updateChatTitleById({ chatId: id, title });
          } catch (error) {
            console.error("CHAT TITLE ERROR:", error);
          }
        }
      },
      generateId: generateUUID,
      onEnd: async ({ messages: finishedMessages }) => {
        if (isToolApprovalFlow) {
          await Promise.all(
            finishedMessages.map(async (finishedMessage) => {
              const existingMessage = uiMessages.find(
                (currentMessage) => currentMessage.id === finishedMessage.id
              );

              if (existingMessage) {
                await updateMessage({
                  id: finishedMessage.id,
                  parts: withoutTrace(finishedMessage.parts),
                });
                return;
              }

              await saveMessages({
                messages: [
                  {
                    attachments: [],
                    chatId: id,
                    createdAt: new Date(),
                    id: finishedMessage.id,
                    parts: withoutTrace(finishedMessage.parts),
                    role: finishedMessage.role,
                  },
                ],
              });
            })
          );
        } else if (finishedMessages.length > 0) {
          await saveMessages({
            messages: finishedMessages.map((currentMessage) => ({
              attachments: [],
              chatId: id,
              createdAt: new Date(),
              id: currentMessage.id,
              parts: withoutTrace(currentMessage.parts),
              role: currentMessage.role,
            })),
          });
        }
      },
      onError: (error) => {
        const message = describeError(error);

        console.error("CHAT STREAM ERROR:", error);
        console.error("CHAT STREAM ERROR DESCRIPTION:", message);

        return message;
      },
      originalMessages: isToolApprovalFlow ? uiMessages : undefined,
    });

    return createUIMessageStreamResponse({
      async consumeSseStream({ stream: sseStream }) {
        if (!process.env.REDIS_URL) {
          return;
        }

        try {
          const streamContext = getStreamContext();

          if (streamContext) {
            const streamId = generateId();

            await createStreamId({
              chatId: id,
              streamId,
            });

            await streamContext.createNewResumableStream(
              streamId,
              () => sseStream
            );
          }
        } catch (error) {
          console.error("RESUMABLE STREAM ERROR:", error);
        }
      },
      stream,
    });
  } catch (error) {
    const vercelId = request.headers.get("x-vercel-id");
    const message = describeError(error);

    console.error("UNHANDLED CHAT API ERROR:", error, {
      description: message,
      vercelId,
    });

    if (error instanceof ChatbotError) {
      return error.toResponse();
    }

    return new ChatbotError("offline:chat").toResponse();
  }
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get("id");

  if (!id) {
    return new ChatbotError("bad_request:api").toResponse();
  }

  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  const chat = await getChatById({ id });

  if (chat?.userId !== session.user.id) {
    return new ChatbotError("forbidden:chat").toResponse();
  }

  const deletedChat = await deleteChatById({ id });

  return Response.json(deletedChat, { status: 200 });
}