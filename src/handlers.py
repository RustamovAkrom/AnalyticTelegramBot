from aiogram import Router
from aiogram import Bot, Dispatcher, html

from aiogram.types import Message
from aiogram.filters import CommandStart
from src.ai_parser import ai_generation, safe_ai_generation

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: Message) -> None:
    response = await safe_ai_generation(message.text)
    await message.answer(response)
