from openai import OpenAI
from config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

response = client.chat.completions.create(
    model="deepseek/deepseek-v3.2",
    messages=[
        {"role": "system", "content": "Выбирай функцию и аргументы из доступного интерфейса функций."},
        {"role": "user", "content": "Сколько видео набрали больше 100000 просмотров?"}
    ],
    # Если модель поддерживает reasoning + tool use:
    extra_body={"reasoning": {"enabled": True}}
)

message = response.choices[0].message
print(message.content)
