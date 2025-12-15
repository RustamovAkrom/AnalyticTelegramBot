# src/ai_parser.py
import asyncio
from openai import AsyncOpenAI, RateLimitError
from src.metrics import generate_context
from .config import settings

MODEL = "google/gemini-2.5-flash"  # бесплатная LLM, подходящая для небольших промптов

# Базовый промпт для LLM
BASE_PROMPT = """
У тебя есть статистика по видео-креаторам.
Таблица videos:
- id: идентификатор видео
- creator_id: идентификатор креатора
- video_created_at: дата публикации
- views_count, likes_count, comments_count, reports_count: финальные показатели

Таблица video_snapshots:
- video_id: ссылка на видео
- views_count, likes_count, comments_count, reports_count
- delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count
- created_at: время замера

Используй эти данные для ответа на запрос, всегда возвращай **одно число**.
"""

# создаем асинхронного клиента
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

# Основная функция генерации ответа от LLM
async def ai_generation(prompt: str) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        extra_body={},
        max_tokens=100
    )
    return response.choices[0].message.content

# Безопасная обертка с повторной попыткой при rate-limit
async def safe_ai_generation(prompt: str) -> str:
    for attempt in range(5):
        try:
            return await ai_generation(prompt)
        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limit, retrying in {wait}s...")
            await asyncio.sleep(wait)
    raise Exception("Rate limit persists after retries")

# Функция для получения ответа на пользовательский вопрос
async def ask_ai_about_videos(session, user_question: str) -> str:
    # Получаем агрегированную статистику из базы
    context = await generate_context(session)

    # Формируем итоговый промпт
    prompt = f"""
{BASE_PROMPT}

Вот текущая агрегированная статистика:
{context}

Вопрос пользователя: {user_question}
"""
    # Отправляем на LLM и получаем ответ
    answer = await safe_ai_generation(prompt)

    # Оставляем только число в ответе
    return "".join(filter(str.isdigit, answer))
