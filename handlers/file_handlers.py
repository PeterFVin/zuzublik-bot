import os
import sqlite3
from datetime import datetime

import pandas as pd
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from config import DB_NAME
from constants import (BUTTON_UPLOAD_HELP_TEXT, BUTTON_UPLOAD_TEXT,
                       ERROR_EXTENSION_TEXT)
from keyboards import upload_keyboard
from services.parser import extract_class_from_xpath, parse_price

router = Router()


class Form(StatesGroup):
    waiting_for_file = State()


@router.message(F.text == BUTTON_UPLOAD_TEXT)
async def request_file(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        BUTTON_UPLOAD_HELP_TEXT,
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.waiting_for_file)


@router.message(Form.waiting_for_file, F.document)
async def handle_file(message: types.Message, state: FSMContext) -> None:
    bot = message.bot

    file_name = message.document.file_name
    if not (file_name.endswith(".xlsx") or file_name.endswith(".csv")):
        await message.answer(
            ERROR_EXTENSION_TEXT,
            reply_markup=upload_keyboard,
        )
        await state.clear()
        return

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file.file_path)

    temp_file = f"temp_{file_name}"
    with open(temp_file, "wb") as f:
        f.write(downloaded_file.read())

    try:
        if file_name.endswith(".xlsx"):
            df = pd.read_excel(temp_file, names=["title", "url", "xpath"])
        elif file_name.endswith(".csv"):
            df = pd.read_csv(temp_file, names=["title", "url", "xpath"])

        current_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        table_name = f"parsed_data_{current_time}"

        db_name = DB_NAME
        with sqlite3.connect(db_name) as conn:
            df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

        loaded_data = [
            f"Данные, сохраненные в таблицу {table_name}. "
            f"Всего записей - {len(df)}, показаны первые."
        ]
        parse_list = set()
        for i, row in df.iterrows():
            if i < 3:
                loaded_data.append(
                    f"{i+1}. {row['title']} || {row['url']} || {row['xpath']}"
                )
            parse_list.add(extract_class_from_xpath(row["xpath"]))

        await message.answer("\n".join(loaded_data))

        df["domain"] = df["url"].apply(lambda x: "/".join(x.split("/")[:3]))
        price_report = ["\nСредние цены по магазинам:"]

        for (product, domain), group in df.groupby(["title", "domain"]):
            prices = []
            for _, row in group.iterrows():
                price = parse_price(row["url"], row["xpath"], parse_list)
                if price:
                    prices.append(price)

            if prices:
                avg_price = sum(prices) / len(prices)
                price_str = f"{int(avg_price):,} ₽".replace(",", " ")
                count_str = f" (на основе {len(prices)} цен)"
            else:
                price_str = "не удалось получить"
                count_str = ""

            price_report.append(f"{product} в {domain} - {price_str}{count_str}")

        await message.answer("\n".join(price_report), reply_markup=upload_keyboard)

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}", reply_markup=upload_keyboard)
    finally:
        os.remove(temp_file)
        await state.clear()
