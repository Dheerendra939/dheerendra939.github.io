import json
import random
import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8040418147:AAFSuJCnUASdUUvlRI8Q9Uf91vawe3I6N7o"  # Replace after regenerating

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# Start command
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(
        "Tap the button below to watch the rewarded ad.",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                text="Open Mini App",
                web_app=types.WebAppInfo(url="https://dheerendra939.github.io")
            )
        )
    )


# Receive data from Mini App
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        number = data.get("random_number")

        if number:
            await message.answer(f"🎉 Your random number: {number}")
        else:
            await message.answer("No number received.")
    except Exception as e:
        await message.answer(f"Error reading data: {e}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
