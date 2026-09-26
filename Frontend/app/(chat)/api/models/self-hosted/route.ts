import { auth } from "@/app/(auth)/auth";
import { getBackendUrl } from "@/lib/backend";

type SelfHostedModel = { id: string; name: string };

// The self-hosted models the backend is set up with, for Settings → Models,
// and the model it uses for a step when none is picked.
// The backend keeps the server addresses; the browser only sees ids and names.
export async function GET() {
  const session = await auth();
  if (!session?.user) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  const empty = {
    text: [] as SelfHostedModel[],
    vision: [] as SelfHostedModel[],
  };
  const backendUrl = getBackendUrl();

  if (!backendUrl) {
    return Response.json(
      { ...empty, error: "BACKEND_URL is not configured on the frontend." },
      { status: 500 }
    );
  }

  try {
    const res = await fetch(`${backendUrl}/models`, { cache: "no-store" });

    if (!res.ok) {
      return Response.json(
        {
          ...empty,
          error: `The backend answered ${res.status} for /models. It may be running old code.`,
        },
        { status: 502 }
      );
    }

    const data = (await res.json()) as Partial<typeof empty> & {
      default_model?: string;
      error?: string;
      servers?: number;
    };

    return Response.json({
      defaultModel: data.default_model,
      error: data.error,
      servers: data.servers,
      text: data.text ?? [],
      vision: data.vision ?? [],
    });
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    return Response.json(
      { ...empty, error: `Could not reach the backend: ${reason}` },
      { status: 502 }
    );
  }
}
