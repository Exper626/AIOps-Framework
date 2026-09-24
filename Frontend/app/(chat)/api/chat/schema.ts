import { z } from "zod";

const textPartSchema = z.object({
  text: z.string().min(1).max(2000),
  type: z.enum(["text"]),
});

const filePartSchema = z.object({
  mediaType: z.enum(["image/jpeg", "image/png"]),
  name: z.string().min(1).max(100),
  type: z.enum(["file"]),
  url: z.url(),
});

const partSchema = z.union([textPartSchema, filePartSchema]);

const userMessageSchema = z.object({
  id: z.uuid(),
  parts: z.array(partSchema),
  role: z.enum(["user"]),
});

const toolApprovalMessageSchema = z.object({
  id: z.string(),
  parts: z.array(z.record(z.string(), z.unknown())),
  role: z.enum(["user", "assistant"]),
});

const modelChoiceSchema = z.object({
  baseUrl: z.url().optional(),
  modelId: z.string().min(1).max(200),
  source: z.enum(["api", "self-hosted"]),
});

export const postRequestBodySchema = z.object({
  agents: z.record(z.string(), z.boolean()).optional(),
  diagramGeneration: z.boolean().optional(),
  id: z.uuid(),
  message: userMessageSchema.optional(),
  messages: z.array(toolApprovalMessageSchema).optional(),
  modelChoices: z
    .object({ text: modelChoiceSchema, vision: modelChoiceSchema })
    .optional(),
  selectedChatModel: z.string(),
  selectedVisibilityType: z.enum(["public", "private"]),
  selectedVisionModel: z.string().optional(),
});

export type PostRequestBody = z.infer<typeof postRequestBodySchema>;
