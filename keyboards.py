from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

start = KeyboardButton('Start! 💰')
startMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(start)