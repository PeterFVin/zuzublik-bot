from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from constants import BUTTON_UPLOAD_TEXT

upload_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BUTTON_UPLOAD_TEXT)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
