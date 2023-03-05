from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from config import ADMINS
from keyboards.default import send_language, yes_no, send_all_products, send_location_for_admin, \
    markup_for_delete_address, get_phone_number, send_back, main_menu, default_category_for_admin, \
    command_buttons_for_admin, show_phone_nums
from keyboards.inline import category_for_admin
from texts import send_text

from geopy.geocoders import Nominatim



nominatim = Nominatim(user_agent='admin')


data = {}

@bot.message_handler(commands=['add_category'])
def add_category(message: Message):
    # print(message)
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, f"<b>🇺🇿Kategoriyani qaysi tilda kiritmoqchisiz? / 🇷🇺Выберите язык, чтобы введить категорию</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, category_lang)

def category_lang(message: Message, lang='uz'):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    data[from_user_id] = {}
    if message.text == "🇺🇿O'zbekcha":
        lang = 'uz'
    elif message.text == "🇷🇺Русский":
        lang = 'ru'

    data[from_user_id]['lang'] = lang

    if message.text in ["Yo'q", "Нет"]:
        text = send_text(lang)
        bot.send_message(chat_id, f"<b>{text[204]}</b>", reply_markup=command_buttons_for_admin())
        del data[from_user_id]
    else:
        cat = f"<b>{send_text(data[from_user_id]['lang'])[200]}</b>\n\n"
        categories = db.select_categories(lang)
        for i in categories:
            cat += f"👉 {i[1]}\n"
        bot.send_message(chat_id, cat, reply_markup=ReplyKeyboardRemove())
        msg = bot.send_message(chat_id, f"<b>{send_text(lang)[201]}</b>")
        bot.register_next_step_handler(msg, save_category)


def save_category(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        data[from_user_id]['category'] = message.text

        category = data[from_user_id]['category']
        lang = data[from_user_id]['lang']
        text = send_text(lang)
        try:
            db.insert_category(category, lang)
            bot.send_message(chat_id, f"<b>{text[202]}</b>")
        except:
            bot.send_message(chat_id, f"<b>{text[218]}</b>")
        text = send_text(lang)
        msg = bot.send_message(chat_id, f"<b>{text[205]}</b>", reply_markup=yes_no(lang))
        bot.register_next_step_handler(msg, category_lang, lang=lang)





@bot.message_handler(commands=['delete_category'])
def send_lang_for_category_del(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "<b>🇺🇿Qaysi tildagi kategoriyani o'chirmoqchisiz? / 🇷🇺Какую языковую категорию вы хотите удалить?</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, confirm_lang_for_category_del)

def confirm_lang_for_category_del(message: Message, lang='uz'):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "🇺🇿O'zbekcha":
        lang = 'uz'
    elif message.text == "🇷🇺Русский":
        lang = 'ru'

    text = send_text(lang)

    if message.text in ["Нет", "Yo'q"]:
        del data[from_user_id]
        bot.send_message(chat_id, f"<b>{text[204]}</b>", reply_markup=command_buttons_for_admin())
    else:
        data[from_user_id] = {}
        data[from_user_id]['lang'] = lang

        categories = db.select_categories(lang)
        msg = bot.send_message(chat_id, f"<b>{text[206]}</b>", reply_markup=default_category_for_admin(categories, lang))
        bot.register_next_step_handler(msg, confirm_category_del)


def confirm_category_del(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = data[from_user_id]['lang']
    text = send_text(lang)
    category = message.text
    if category in ["⬅️Назад", "⬅️Ortga"]:
        msg = bot.send_message(chat_id,
                               "<b>🇺🇿Qaysi tildagi kategoriyani o'chirmoqchisiz? / 🇷🇺Какую языковую категорию вы хотите удалить?</b>",
                               reply_markup=send_language())
    else:
        db.delete_category(category)
        bot.send_message(chat_id, f"<b>{text[207]}</b>")
        msg = bot.send_message(chat_id, f"<b>{text[208]}</b>", reply_markup=yes_no(lang))
    bot.register_next_step_handler(msg, confirm_lang_for_category_del, lang=lang)






@bot.message_handler(commands=['add_product'])
def add_product(message: Message):
    # print(message)
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "<b>🇺🇿Mahsulotni qaysi til uchun kiritmoqchisiz? / 🇷🇺Для какого языка вы хотите добавить продукт?</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, confirm_language_for_product)

def confirm_language_for_product(message: Message, lang='uz'):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    try:
        if message.text == "🇺🇿O'zbekcha":
            lang = 'uz'
        elif message.text == "🇷🇺Русский":
            lang = 'ru'

        data[from_user_id] = {}
        data[from_user_id]['lang'] = lang
        text = send_text(lang)

        if message.text in ["Нет", "Yo'q"]:
            del data[from_user_id]
            bot.send_message(chat_id, text[204], reply_markup=command_buttons_for_admin())
        else:
            categories = db.select_categories(lang)
            msg = bot.send_message(chat_id, f"<b>{text[209]}</b>", reply_markup=default_category_for_admin(categories, lang))
            bot.register_next_step_handler(msg, name_product)
    except:
        bot.send_message(chat_id, "Admin panel", reply_markup=command_buttons_for_admin())

def name_product(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text in ["⬅️Назад", "⬅️Ortga"]:
        msg = bot.send_message(chat_id, "<b>🇺🇿Mahsulotni qaysi til uchun kiritmoqchisiz? / 🇷🇺Для какого языка вы хотите добавить продукт?</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, confirm_language_for_product)
    else:
        category_id = db.select_category_id(message.text)[0]
        data[from_user_id]['category_id'] = category_id
        lang = data[from_user_id]['lang']
        text = send_text(lang)
        msg = bot.send_message(chat_id, f"<b>{text[211]}</b>", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, image_product)

def image_product(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    data[from_user_id]['name'] = message.text
    lang = data[from_user_id]['lang']
    text = send_text(lang)
    msg = bot.send_message(chat_id, f"<b>{text[212]}</b>")
    bot.register_next_step_handler(msg, context_product)

def context_product(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    photo = message.photo[-1].file_id
    data[from_user_id]['photo'] = photo

    lang = data[from_user_id]['lang']
    text = send_text(lang)
    msg = bot.send_message(chat_id, f"<b>{text[213]}</b>")
    bot.register_next_step_handler(msg, price_product)


def price_product(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    data[from_user_id]['content'] = message.text

    lang = data[from_user_id]['lang']
    text = send_text(lang)
    msg = bot.send_message(chat_id, f"<b>{text[214]}</b>")
    bot.register_next_step_handler(msg, confirmation)


def confirmation(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    try:
        data[from_user_id]['price'] = int(message.text)
    except:
        data[from_user_id]['price'] = 'NULL'

    lang = data[from_user_id]['lang']
    category_id = data[from_user_id]['category_id']
    product_name = data[from_user_id]['name']
    image = data[from_user_id]['photo']
    content = data[from_user_id]['content']
    price = data[from_user_id]['price']

    text = send_text(lang)
    bot.send_photo(chat_id, image, caption=f"<b>Nomi: {product_name}</b>\n\n<b>Tavsifi:</b> {content}\n\n<b>Narxi:</b> {price}")
    msg = bot.send_message(chat_id, f"<b>{text[210]}</b>", reply_markup=yes_no(lang))
    bot.register_next_step_handler(msg, save_product_in_db)

def save_product_in_db(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = data[from_user_id]['lang']
    text = send_text(lang)
    if message.text in ["Нет", "Yo'q"]:
        del data[from_user_id]
        bot.send_message(chat_id, f"<b>{text[215]}</b>", reply_markup=ReplyKeyboardRemove())
    elif message.text in ["Xa", "Да"]:

        lang = data[from_user_id]['lang']
        product_name = data[from_user_id]['name']
        image = data[from_user_id]['photo']
        content = data[from_user_id]['content']
        price = data[from_user_id]['price']
        category_id = data[from_user_id]['category_id']
        try:
            db.add_product(product_name, image, content, price, lang, category_id)
            bot.send_message(chat_id, f"<b>{text[216]}</b>")
        except:
            bot.send_message(chat_id, f"<b>{text[217]}</b>")
        msg = bot.send_message(chat_id, f"<b>{text['216a']}</b>", reply_markup=yes_no(lang))
        bot.register_next_step_handler(msg, confirm_language_for_product, lang=lang)





@bot.message_handler(commands=['delete_product'])
def send_lang_for_product_del(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "<b>🇺🇿Qaysi tildagi mahsulotni o'chirmoqchisiz? / 🇷🇺Какой языковой продукт вы хотите удалить?</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, send_products_for_del)

def send_products_for_del(message: Message, lang='uz'):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "🇺🇿O'zbekcha":
        lang = 'uz'
    elif message.text == "🇷🇺Русский":
        lang = 'ru'

    data[from_user_id] = {}
    data[from_user_id]['lang'] = lang
    text = send_text(lang)

    if message.text in ["Нет", "Yo'q"]:
        del data[from_user_id]['lang']
        bot.send_message(chat_id, f"<b>{text[215]}</b>", reply_markup=command_buttons_for_admin())
    else:
        products = db.select_all_products(lang)
        msg = bot.send_message(chat_id, f"<b>{text[219]}</b>", reply_markup=send_all_products(products, lang))
        bot.register_next_step_handler(msg, confirm_delete_product)

def confirm_delete_product(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = data[from_user_id]['lang']
    text = send_text(lang)
    product = message.text
    if product in ["⬅️Назад", "⬅️Ortga"]:
        msg = bot.send_message(chat_id, "<b>🇺🇿Qaysi tildagi mahsulotni o'chirmoqchisiz? / 🇷🇺Какой языковой продукт вы хотите удалить?</b>", reply_markup=send_language())
        bot.register_next_step_handler(msg, send_products_for_del)
    else:
        try:
            db.delete_product(product)
            bot.send_message(chat_id, f"<b>{text[220]}</b>")
        except:
            bot.send_message(chat_id, f"<b>{text[221]}</b>")
        msg = bot.send_message(chat_id, f"<b>{text[222]}</b>", reply_markup=yes_no(lang))
        bot.register_next_step_handler(msg, send_products_for_del, lang=lang)

data_address = {}
# @bot.message_handler(commands=['add_address'])
# def add_address(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     data_address[from_user_id] = {}
#     if from_user_id in ADMINS:
#         msg = bot.send_message(chat_id, text[127], reply_markup=send_language())
#         bot.register_next_step_handler(msg, add_language)
#
# def add_language(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text == "🇺🇿O'zbekcha":
#         language = 'uz'
#     elif message.text == "🇷🇺Русский":
#         language = 'ru'
#     data_address[from_user_id]['language'] = language
#     msg = bot.send_message(chat_id, text[126], reply_markup=send_back(lang))
#     bot.register_next_step_handler(msg, add_name_address)
#
# def add_name_address(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     name_address = message.text
#     if name_address in ["⬅️Ortga", "⬅️Назад"]:
#         bot.send_message(chat_id, text[16], reply_markup=command_buttons_for_admin())
#     else:
#         data_address[from_user_id]['name_address'] = name_address
#         msg = bot.send_message(chat_id, text[103], reply_markup=get_phone_number(lang))
#         bot.register_next_step_handler(msg, add_phone_number)
#
# def add_phone_number(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text in ["⬅️Ortga", "⬅️Назад"]:
#         bot.send_message(chat_id, text[16], reply_markup=command_buttons_for_admin())
#     else:
#         phone_number = message.contact.phone_number
#         data_address[from_user_id]['phone_number'] = phone_number
#         msg = bot.send_message(chat_id, text[114], reply_markup=send_location_for_admin(lang))
#         bot.register_next_step_handler(msg, save_location_for_admin)
#
# def save_location_for_admin(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text in ["⬅️Ortga", "⬅️Назад"]:
#         bot.send_message(chat_id, text[16], reply_markup=main_menu(lang))
#     elif message.location:
#         name_address = data_address[from_user_id]['name_address']
#         phone_number = data_address[from_user_id]['phone_number']
#         language = data_address[from_user_id]['language']
#         long = message.location.longitude
#         lat = message.location.latitude
#
#         coordinates = f"{lat}, {long}"
#         try:
#             location = nominatim.reverse(coordinates)
#             location_info = f"{location}"[0:90]
#             db.insert_loc_auto_burger(location_info, lat, long, name_address, phone_number, language)
#             text_info = text[115]
#         except:
#             text_info = text[116]
#         bot.send_message(chat_id, text_info, reply_markup=command_buttons_for_admin())
#
#
# @bot.message_handler(commands=['delete_address'])
# def delete_address(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if from_user_id in ADMINS:
#         msg = bot.send_message(chat_id, text[128], reply_markup=send_language())
#         bot.register_next_step_handler(msg, select_by_lang)
#
# def select_by_lang(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text == "🇺🇿O'zbekcha":
#         language = 'uz'
#     elif message.text == "🇷🇺Русский":
#         language = 'ru'
#
#     locations_info = db.select_location_info_for_auto_burger(language)
#     markup = markup_for_delete_address(locations_info, lang)
#     msg = bot.send_message(chat_id, text[118], reply_markup=markup)
#     bot.register_next_step_handler(msg, confirmation_delete_address)
#
# def confirmation_delete_address(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     address_info = message.text
#     if address_info in ["❌ Bekor qilish", "❌ Отмена"]:
#         bot.send_message(chat_id, text[119], reply_markup=main_menu(lang))
#     else:
#         try:
#             db.delete_location_for_auto_burger_by_name_address(address_info)
#             text_info = text[117]
#         except:
#             text_info = text[116]
#         bot.send_message(chat_id, text_info, reply_markup=main_menu(lang))



@bot.message_handler(commands=['add_photo_for_categories'])
def get_photo(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        try:
            lang = db.select_lang(from_user_id)[0]
            text = send_text(lang)
            msg = bot.send_message(chat_id, text[135], reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, save_photo)
        except:
            pass


def save_photo(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    try:
        lang = db.select_lang(from_user_id)[0]
        text = send_text(lang)
        photo = message.photo[-1].file_id
        if chat_id in ADMINS:
            try:
                db.insert_photo(photo)
                bot.send_message(chat_id, text[134], reply_markup=command_buttons_for_admin())
            except:
                bot.send_message(chat_id, text[133], reply_markup=command_buttons_for_admin())
    except:
        pass


@bot.message_handler(commands=['add_phone_number'])
def add_phone_number(message: Message):
    '''Operator tel nomerini qo'shish'''
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, text[103], reply_markup=get_phone_number(lang))
        bot.register_next_step_handler(msg, admin_save_phone_number)

def admin_save_phone_number(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if message.text in ['⬅️Ortga', "⬅️Назад"]:
        text_info = message.text
    else:
        try:
            phone = message.contact.phone_number.split('+')
            # print(phone)
            if len(phone) == 2:
                db.insert_phone_from_feedback(phone[1])

            elif len(phone) == 1:
                db.insert_phone_from_feedback(phone[0])
            text_info = text[137]
        except:
            text_info = text[133]
    bot.send_message(chat_id, text_info, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text[139], reply_markup=command_buttons_for_admin())


@bot.message_handler(commands=['delete_phone_number'])
def delete_phone_number(message: Message):
    '''Operator tel nomerini qo'shish'''
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if from_user_id in ADMINS:
        phones = db.select_phone_nums_from_feedback()
        msg = bot.send_message(chat_id, text[140], reply_markup=show_phone_nums(phones, lang))
        bot.register_next_step_handler(msg, admin__commit_delete_phone_number)

def admin__commit_delete_phone_number(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if message.text in ['⬅️Ortga', "⬅️Назад"]:
        text_info = message.text
    else:
        phone_num = message.text
        try:
            db.delete_phone_num_from_feedback(phone_num)
            text_info = text[141]
        except:
            text_info = text[133]
    bot.send_message(chat_id, text_info, reply_markup=command_buttons_for_admin())



@bot.message_handler(commands=['add_photo'])
def add_photo_to_main_menu(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, text[135], reply_markup=send_back(lang))
        bot.register_next_step_handler(msg, commit_add_photo_to_main_menu)

def commit_add_photo_to_main_menu(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if message.text in ['⬅️Ortga', "⬅️Назад"]:
        text_clear = message.text
    else:
        try:
            photo = message.photo[-1].file_id
            # print(photo)
            db.update_photo_for_id_from_photo_main(photo)
            text_clear = text[134]
        except:
            text_clear = text[133]

    bot.send_message(chat_id, text_clear, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text[139], reply_markup=command_buttons_for_admin())
