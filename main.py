import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from dotenv import load_dotenv

from songDown import polucatel, zaqruzator

load_dotenv()
okno = False
pesenki = {}

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv('token'))
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Введи название или исполнителя песни: ")


@dp.message()
async def send_answer(message: types.Message):
    global okno
    global pesenki
    mess = message.text
    if not okno or not mess.isdigit():
        okno = True
        spisok = zaqruzator(mess)
        pesenki = spisok
        pesni = {}
        for index in spisok:
            pesni[index] = (
                f"{spisok.get(index).get('artist')} - {spisok.get(index).get('title')}"
            )
        dict_string = "\n".join([f"{key}. {value}" for key, value in pesni.items()])
        await message.reply(dict_string)
        await bot.send_message(message.from_user.id, "Введите номер песни: ")

    elif okno and mess.isdigit() and int(mess) <= 19 and int(mess) >= 0:
        songAbout = polucatel(mess, pesenki)

        if songAbout:
            song = FSInputFile(songAbout)
            await bot.send_document(message.from_user.id, song)
            okno = False
        else:
            await bot.send_message(message.from_user.id, "NASOS")


#    await message.reply("Введите номер песни: ")
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
