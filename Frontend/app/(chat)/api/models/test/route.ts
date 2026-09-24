import { auth } from "@/app/(auth)/auth";

// Checks a self-hosted, OpenAI-compatible server (Ollama, vLLM, LM Studio...)
// by calling its /models endpoint, and returns the model names it offers.
// The server's API key, if it needs one, comes from SELF_HOSTED_API_KEY.
export async function POST(request: Request) {
  const session = await auth();
  if (!session?.user) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  let baseUrl: URL;
  try {
    const body = (await request.json()) as { baseUrl?: string };
    baseUrl = new URL(body.baseUrl ?? "");
  } catch {
    return Response.json(
      { error: "Enter a valid URL, e.g. http://10.0.0.5:11434/v1" },
      { status: 400 }
    );
  }

  if (baseUrl.protocol !== "http:" && baseUrl.protocol !== "https:") {
    return Response.json(
      { error: "The URL must start with http:// or https://" },
      { status: 400 }
    );
  }

  const apiKey = process.env.SELF_HOSTED_API_KEY;

  try {
    const res = await fetch(`${baseUrl.href.replace(/\/$/, "")}/models`, {
      cache: "no-store",
      headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : undefined,
      signal: AbortSignal.timeout(5000),
    });

    if (!res.ok) {
      return Response.json(
        { error: `The server answered with status ${res.status}` },
        { status: 502 }
      );
    }

    const json = (await res.json()) as { data?: { id?: string }[] };
    const models = (json.data ?? [])
      .map((m) => m.id)
      .filter((id): id is string => Boolean(id));

    return Response.json({ models });
  } catch {
    return Response.json(
      { error: "Couldn't reach the server. Check the URL and your network." },
      { status: 502 }
    );
  }
}
