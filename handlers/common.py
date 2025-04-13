from aiogram import Router, types
from aiogram.filters import Command

from constants import BOT_START_MESSAGE
from keyboards import upload_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        BOT_START_MESSAGE,
        reply_markup=upload_keyboard,
    )
