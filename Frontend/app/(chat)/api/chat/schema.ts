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

export const diagramSchema = z.object({
  devices: z
    .array(
      z.object({
        // An icon picked in the diagram editor (lib/network-icons.json)
        icon: z.string().max(80).optional(),
        id: z.string().min(1).max(100),
        model: z.string().max(100).optional(),
        name: z.string().max(100),
        type: z.string().min(1).max(40),
        x: z.number().nullable().optional(),
        y: z.number().nullable().optional(),
      })
    )
    .max(200),
  links: z
    .array(
      z.object({
        source: z.string().min(1).max(100),
        target: z.string().min(1).max(100),
      })
    )
    .max(500),
});

// A network diagram the user drew and sent with the message
const diagramPartSchema = z.object({
  data: diagramSchema,
  id: z.string().min(1).max(100),
  type: z.enum(["data-diagram"]),
});

const partSchema = z.union([textPartSchema, filePartSchema, diagramPartSchema]);

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
  modelId: z.string().min(1).max(200),
  source: z.enum(["api", "self-hosted"]),
});

export const postRequestBodySchema = z.object({
  // Settings → Knowledge: chunks the answer is written from
  chunkCount: z.number().int().min(1).max(20).optional(),
  // Settings → Knowledge: keyword + vector search, or vector only
  hybridSearch: z.boolean().optional(),
  id: z.uuid(),
  // Settings → Memory: use and update what the assistant remembers
  memory: z.boolean().optional(),
  message: userMessageSchema.optional(),
  messages: z.array(toolApprovalMessageSchema).optional(),
  // One model per pipeline step; any may be missing, e.g. when a tab still
  // runs an older version of the app
  modelChoices: z
    .object({
      answer: modelChoiceSchema,
      contextManagement: modelChoiceSchema,
      retrieval: modelChoiceSchema,
      router: modelChoiceSchema,
      visionDescription: modelChoiceSchema,
    })
    .partial()
    .optional(),
  // Settings → Knowledge: re-order search results before answering
  reranker: z.boolean().optional(),
  selectedVisibilityType: z.enum(["public", "private"]),
});

export type PostRequestBody = z.infer<typeof postRequestBodySchema>;
