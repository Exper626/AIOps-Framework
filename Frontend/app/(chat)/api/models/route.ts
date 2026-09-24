import { getAllGatewayModels } from "@/lib/ai/models";

// Every language model on the Vercel AI Gateway, for the model search in Settings.
export async function GET() {
  const models = await getAllGatewayModels();

  return Response.json(
    { models },
    {
      headers: {
        // Browsers always re-ask; only a CDN may cache, and never an empty list
        "Cache-Control":
          models.length > 0
            ? "public, max-age=0, s-maxage=86400"
            : "no-store",
      },
    }
  );
}
