import asyncio
from openai import AsyncOpenAI, RateLimitError

from .config import settings

MODEL = "google/gemini-2.5-flash"

# создаем асинхронный клиент
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

async def ai_generation(prompt: str) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_body={},  # сюда можно передать дополнительные параметры
        max_tokens=1000
    )
    # корректный доступ к содержимому
    return response.choices[0].message.content

async def safe_ai_generation(prompt: str):
    for attempt in range(5):
        try:
            return await ai_generation(prompt)
        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limit, retrying in {wait}s...")
            await asyncio.sleep(wait)
    raise Exception("Rate limit persists after retries")
