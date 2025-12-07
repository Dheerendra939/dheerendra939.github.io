import json
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = "PUT_YOUR_NEW_REGENERATED_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Reply keyboard with 4 buttons
def main_keyboard():
    kb = [
        [types.KeyboardButton("Show Ad"), types.KeyboardButton("Option 2")],
        [types.KeyboardButton("Option 3"), types.KeyboardButton("Option 4")]
    ]
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(*kb[0]).add(*kb[1])


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(
        "Welcome! Click **Show Ad** to continue.",
        reply_markup=main_keyboard()
    )


@dp.message_handler(lambda msg: msg.text == "Show Ad")
async def show_ad_handler(message: types.Message):

    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="Open Ad Window",
            web_app=types.WebAppInfo(url="https://dheerendra939.github.io/index.html")
        )
    )

    await message.answer("Click below to open the Ad window:", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def webapp_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)

    if data.get("ad_completed") == True:
        await message.answer("🎉 You have seen ad successfully!")
    else:
        await message.answer("❗ Reward not collected.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
