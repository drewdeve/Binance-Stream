import logging
import time

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
import keyboards as kb
from utils import MenuState
from binanceStreamer import Binance
from dbWorker import Database

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(HOSTNAME, DATABASE, USERNANE, PWD, PORT)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hello, {0.first_name}! \nI can to stream changes to any coin you want!\nYou only need to add me to the group!'.format(message.from_user), reply_markup=kb.startMenu)

@dp.message_handler(commands=['stop'])
async def process_stop_command(message: types.Message):
    try:
        await bot.leave_chat(message.chat.id)
        title_group = message['chat']['title']
        await bot.send_message(message.from_user.id, f'You stopped me from {title_group}! 🥺', reply_markup=kb.startMenu)
    except:
        await message.answer("You don't add me to the group!")

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def check_group(message: types.Message):
    await MenuState.coin_and_interval.set()
    title_group = message['chat']['title']
    await message.answer(f'Nice! You added me to {title_group}!\nReply this message by entering a coin and an interval!\nFor example: BTCUSDT, 1m')

@dp.message_handler(state=MenuState.coin_and_interval)
async def process_coin_and_interval(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Good! Stream started!')
    db.create_table()
    try:
        Binance()
    except:
        await message.answer('The bot needs to restarted, so please reply to this message again with a coin and an interval!\nFor example: BTCUSDT, 1m\nWait 60 seconds for the process!')
        time.sleep(60)
        Binance()

@dp.message_handler(content_types=['text'])
async def process_start(message: types.Message):
    if message.text == 'Start! 💰':
        await message.answer('To get started, add me to the group and reply to my message where enter the coin and interval(1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M) ⏲ there!')
        await message.answer('To stop me, all you have to do is enter /stop in the group!', reply_markup=types.ReplyKeyboardRemove(True))
  
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)