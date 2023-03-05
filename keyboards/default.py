'''
SIZ BU YERDA ODDIY KNOPKALAR YARATA OLASIZ
'''

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from texts import send_text
from data.loader import db
from config import ADMINS


def main_menu(lang, chat_id=None):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(text[0])
    btn2 = KeyboardButton(text[1])
    btn3 = KeyboardButton(text[2])
    btn4 = KeyboardButton(text[3])
    btn5 = KeyboardButton(text[4])

    btn6 = KeyboardButton('Admin chun')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    if chat_id != None:
        if chat_id in ADMINS:
            markup.add(btn6)
    return markup


def send_language():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_uz = KeyboardButton("🇺🇿O'zbekcha")
    btn_ru = KeyboardButton("🇷🇺Русский")
    markup.add(btn_uz, btn_ru)
    return markup


def get_phone_number(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    text = send_text(lang)
    phone = KeyboardButton(text[9], request_contact=True)
    back = KeyboardButton(text[11])
    markup.add(phone, back, row_width=1)
    return markup


def back(lang):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text[11])
    btn2 = KeyboardButton(text[101])
    markup.add(btn, btn2, row_width=2)
    return markup


def default_category_for_admin(categories, lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    text = send_text(lang)
    for category in categories:
        btn = KeyboardButton(category[1])
        markup.row(btn)

    back = KeyboardButton(text[11])
    markup.add(back)
    return markup


def yes_no(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes = KeyboardButton(send_text(lang)[14])
    no = KeyboardButton(send_text(lang)[15])
    markup.add(yes, no)
    return markup


def send_all_products(products, lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    text = send_text(lang)
    for product in products:
        btn = KeyboardButton(product[0])
        markup.add(btn)
    home = KeyboardButton(text[16])
    back = KeyboardButton(text[11])
    markup.add(home, back)
    return markup


def location(lang):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(text[19], request_location=True)
    btn2 = KeyboardButton(text[20])
    # btn3 = KeyboardButton('tasdiq')
    btn4 = KeyboardButton(text[11])

    markup.row(btn1)
    markup.add(btn2, btn4)
    return markup


def send_info_location(info, lang):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in info:
        print(i)
        btn = KeyboardButton(i[0])
        markup.add(btn)
    btn_back = KeyboardButton(text[11])
    markup.add(btn_back)
    return markup


def send_location_for_admin(lang):
    '''Admin o'z lokatsiyasini yuborishi uchun funksiya'''
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = KeyboardButton(text[19], request_location=True)
    btn_back = KeyboardButton(text[11])
    markup.add(btn, btn_back)
    return markup


def markup_for_delete_address(locations_info, lang):
    '''Bu funsiya o'chirish uchun bazadan olingan kategoriyalardan button yasab beradi'''
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    text = send_text(lang)
    for loc_info in locations_info:
        btn = KeyboardButton(loc_info[0])
        markup.add(btn)
    btn_back = KeyboardButton(text[21])
    markup.add(btn_back)
    return markup

#
# def send_location_for_foot(locations_info, lang):
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     text = send_text(lang)
#     for location_info in locations_info:
#         btn = KeyboardButton(location_info[0])
#         markup.add(btn)
#     btn_back = KeyboardButton(text[11])
#     markup.add(btn_back)
#     return markup



def send_back(lang):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text[11])
    markup.add(btn)
    return markup


def send_cancel(lang):
    text = send_text(lang)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text[21])
    markup.add(btn)
    return markup


def command_buttons_for_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('/add_category')
    btn2 = KeyboardButton('/delete_category')
    btn3 = KeyboardButton('/add_product')
    btn4 = KeyboardButton('/delete_product')
    btn5 = KeyboardButton('/add_photo')
    btn7 = KeyboardButton('/add_photo_for_categories')
    btn8 = KeyboardButton('/add_phone_number')
    btn9 = KeyboardButton('/delete_phone_number')

    btn = KeyboardButton("Bosh sahifa")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn7, btn8, btn9, btn)
    return markup


def show_phone_nums(phones, lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    text = send_text(lang)
    for phone in phones:
        btn = KeyboardButton(phone[0])
        markup.add(btn)
    back_admin = KeyboardButton(text[11])
    markup.add(back_admin)
    return markup