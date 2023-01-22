import glob
import os

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from tg_bot_parser import search_data

API_TOKEN = config('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('Привет!\nЯ буду отправлять тебе инструкции к твоей электронике\nВведи название электроники')


@dp.message_handler()
async def send_instruction(message: types.Message):
    product_title = message.text
    await message.reply('Подожди, идет поиск инструкции...')
    search_data(product_title)
    try:
        path_to_pdf = glob.glob(f'{os.getcwd()}/pdf_files/*.pdf')[0]
        doc = open(path_to_pdf, 'rb')
        os.remove(path_to_pdf)
        await message.reply_document(doc)
    except IndexError:
        await message.reply('Неправильно введено название, либо нет инструкции к этой электронике')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
