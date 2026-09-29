import { auth } from "@/app/(auth)/auth";
import { deleteAllMemories, deleteMemory, listMemories } from "@/lib/backend";
import { ChatbotError } from "@/lib/errors";

// Settings → Memory: the signed-in user's memories, which the backend keeps
// with Mem0. The user id always comes from the session, never the browser.

function failed(action: string, error: unknown) {
  const reason = error instanceof Error ? error.message : "unknown error";
  return Response.json(
    { error: `Couldn't ${action} the memories: ${reason}` },
    { status: 502 }
  );
}

export async function GET() {
  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  try {
    return Response.json({ memories: await listMemories(session.user.id) });
  } catch (error) {
    return failed("load", error);
  }
}

// ?id=... deletes one memory; without it, all of them
export async function DELETE(request: Request) {
  const session = await auth();

  if (!session?.user) {
    return new ChatbotError("unauthorized:chat").toResponse();
  }

  const id = new URL(request.url).searchParams.get("id");

  try {
    if (id) {
      await deleteMemory(session.user.id, id);
    } else {
      await deleteAllMemories(session.user.id);
    }
  } catch (error) {
    return failed("delete", error);
  }

  return Response.json({ deleted: true });
}
