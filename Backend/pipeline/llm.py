from openai import OpenAI

from config import settings

AI_GATEWAY_BASE_URL = "https://ai-gateway.vercel.sh/v1"

gateway_client = OpenAI(api_key=settings.ai_gateway_api_key, base_url=AI_GATEWAY_BASE_URL)
