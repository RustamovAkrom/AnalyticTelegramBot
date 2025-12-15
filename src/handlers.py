from aiogram import Router
from aiogram import Bot, Dispatcher, html

from aiogram.types import Message
from aiogram.filters import CommandStart
from src.ai_parser import ask_ai_about_videos
from src.database import async_session

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: Message) -> None:
    async with async_session() as session:
        response = await ask_ai_about_videos(session, message.text)
    await message.answer(str(response))
