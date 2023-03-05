'''
BOTNI ISHGA TUSHIRISH UCHUN KERAK BO'LADIGAN NARSALARNI KIRG'IZING
'''
from telebot import TeleBot
from config import TOKEN
from database.database import Database
# db = DataBase()
db = Database()

bot = TeleBot(TOKEN, parse_mode='html', use_class_middlewares=True)

