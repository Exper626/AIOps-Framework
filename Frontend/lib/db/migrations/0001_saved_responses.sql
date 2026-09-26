CREATE TABLE IF NOT EXISTS "SavedResponse" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "userId" uuid NOT NULL REFERENCES "User"("id"),
  "chatId" uuid NOT NULL,
  "messageId" uuid NOT NULL,
  "question" text NOT NULL,
  "parts" json NOT NULL,
  "createdAt" timestamp NOT NULL,
  CONSTRAINT "SavedResponse_userId_messageId_unique" UNIQUE ("userId", "messageId")
);
