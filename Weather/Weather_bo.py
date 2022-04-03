import datetime

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from WethApi import weather_token, tg_bot_token
from translate import Translator

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

inline_btn_1 = InlineKeyboardButton("Saytga O'tiish!", callback_data='button1', url='https://www.accuweather.com/uz/')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    photo = open("images/Jurnalist.jpg", "rb")
    await bot.send_photo(message.chat.id, photo)
    await message.reply("Assalom alekum Ob-havo botga Xush kelibsiz \n                "
                        "☀️🌤⛅️☁️🌦⛈🌨🌪\nBotdan foydalanish uchun Shahar nomini yozing!")


@dp.message_handler()
async def get_weather(message: types.Message):
    chatID = message.chat.id
    tranlater1 = Translator(from_lang='uz', to_lang='en')
    text = message.text
    message = tranlater1.translate(text).capitalize()

    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={message}&appid={weather_token}&units=metric"
    )
    data = r.json()
    if data:
        try:
            holat1 = ''
            p = open("images/Quyoshli.jpg", "rb")
            city = data["name"]
            holat = data["weather"][0]["main"]
            cur_weather = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            if holat == "Mist" or holat == "Haze":
                holat = "Tumanli 💨"
                p = open("images/Tuman.jpg", "rb")
                holat1 = "Ko'chada tuman \n" \
                         "Yo'lingizga qarab yuring."
            elif holat == "clear sky" or holat == "Clear":
                holat = "Quyoshli ☀️"
                p = open("images/Quyoshli.jpg", "rb")
                holat1 = "Ko'cha issiq aylanishli havo 😃"
            elif holat == "few clouds" or holat == "scattered clouds" or holat == "broken clouds":
                holat = "Bulutli 🌥"
                holat1 = "Ko'cha bulutli shamol bo'lishi mumkin\n"
                p = open("images/Bulutli.jpg", "rb")
            elif holat == "Clouds":
                holat = "Bulutli ☁️"
                p = open("images/Bulutli.jpg", "rb")
                holat1 = "Ko'cha bulutli salqin bo'lishi kutilmoqda"
            elif holat == "shower rain" or holat == "rain" or holat == "Rain" or holat == "Shower rain":
                holat = "Yomg'irli 🌧"
                p = open("images/Bulutli.jpg", "rb")
                holat1 = "Yomg'ir yog'ishi kutilmoqda\n" \
                         "Soyaboni olishdan esdan chiqarmang"
            elif holat == "thunderstorm" or holat == "Thunderstorm":
                holat = "Momaqaldiroq ⛈"
                p = open("images/cahqmoq.jpg", "rb")
                holat1 = "Ko'chada Ko'p yurmang \n" \
                         "Ko'chada chaqmoq chaqishi kutilmoqda"
            elif holat == "snow" or holat == "Snow":
                holat = "Qorli 🌨"
                p = open("images/Qor.jpg", "rb")
                holat1 = "Ko'cha sovuq issiqroq kiyinib\n" \
                         "oling"

            await bot.send_photo(chatID, p, caption=f"{holat}")

            await bot.send_message(chatID, f"{city} shahrida ob-havo\n"
                                           f"Havoharorati : {cur_weather} C°\n"
                                           f"Namgarchilik : {humidity}%\n"
                                           f"Shamol tezligi : {wind} m/sek\n"
                                           f"Quyosh botishi : {sunrise_timestamp}\n"
                                           f"{holat1}"
                                   )
            await message.reply(text="To'liq pragnozi ko'rish uchun!", reply_markup=inline_kb1)
        except Exception as i:
            print(i)


if __name__ == '__main__':
    executor.start_polling(dp)
