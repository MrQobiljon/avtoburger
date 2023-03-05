'''CALLBACKLARNI ILADIGAN HANDLERLAR'''
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from data.loader import bot, db
from states.states import CardState
from texts import send_text
from keyboards.default import *
from keyboards.inline import *
from handlers.users.text_handlers import contact, data, reaction_to_settings
from geopy.geocoders import Nominatim
from config import ADMINS
from .yordamchi_fayl import send_telegram_id_all_users

nominatim = Nominatim(user_agent='admin')




# -----------------------------------------------------------------------------------------------
# Bosh sahifa --->


@bot.callback_query_handler(func=lambda call: call.data == 'buyurtma_berish')
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    data[from_user_id] = {}
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text[124], reply_markup=delivery(lang))



@bot.callback_query_handler(func=lambda call: call.data == 'sozlamalar')
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text[102], reply_markup=send_buttons_settings(lang, from_user_id))



# @bot.callback_query_handler(func=lambda call: call.data == 'mening_buyurtmalarim')
# def reaction_to_order(call: CallbackQuery):
#     chat_id = call.message.chat.id
#     from_user_id = call.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)



@bot.callback_query_handler(func=lambda call: call.data == 'izoh_qoldirish')
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    msg = bot.send_message(chat_id, text[130], reply_markup=send_cancel(lang))
    bot.register_next_step_handler(msg, send_comment)


def send_comment(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    if message.text in ["❌ Bekor qilish", "❌ Отмена"]:
        bot.send_message(chat_id, text[119], reply_markup=ReplyKeyboardRemove())
        # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))
    else:
        from datetime import datetime
        data_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        full_name = message.from_user.full_name
        comment = message.text
        text_comment = f"#comment\n" \
                       f"<b>Kommentariya qoldirildi.</b>\n" \
                       f"{comment}\n\n" \
                       f"<b>Komentariya qoldirdi:</b>\n" \
                       f"{full_name}\n" \
                       f"<b>Vaqti: {data_now}</b>"

        try:
            users = send_telegram_id_all_users()
            # print(users)
            for admin in ADMINS:
                if admin in users:
                    bot.send_message(admin, text_comment)
            bot.send_message(chat_id, text[131], reply_markup=ReplyKeyboardRemove())
            # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
            photo_id = db.select_photo_from_photo_main()
            bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))
        except:
            bot.send_message(chat_id, text[138], reply_markup=ReplyKeyboardRemove())
            # bot.send_message(chat_id,  text[16], reply_markup=inline_main_menu(lang, from_user_id))
            photo_id = db.select_photo_from_photo_main()
            bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))



@bot.callback_query_handler(func=lambda call: call.data == 'boglanish')
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    phones = db.select_phone_nums_from_feedback()
    text_info = ''
    if lang == 'uz':
        text_info += f"Operatorga bog'lanish telfon raqamlari\n\n"
    elif lang == 'ru':
        text_info += f"Контактные телефоны оператора\n"
    for phone in phones:
        text_info += f"👉 +{phone[0]}\n"

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text_info, reply_markup=send_back(lang))



@bot.callback_query_handler(func=lambda call: call.data == 'admin_panel')
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, f"<b>{text[136]}</b>", reply_markup=command_buttons_for_admin())

# <---
# -----------------------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------------------
# Sozlamar qismi bosilganda chiqadigan buttondan qaytgan call lar

@bot.callback_query_handler(func=lambda call: call.data == 'name')
def reaction_to_name(call: CallbackQuery):
    data = get_user_info(call=call)
    bot.delete_message(data['chat_id'], call.message.message_id)
    msg = bot.send_message(data['chat_id'], data['text'][104], reply_markup=back(data['lang']))
    bot.register_next_step_handler(msg, save_user_name)

def save_user_name(message: Message):
    data = get_user_info(message=message)
    from_user_id = message.from_user.id
    if message.text in ["⬅️Ortga", "⬅️Назад"]:
        reaction_to_settings(message)
    elif message.text in ["Asosiy menyu", "Главное меню"]:
        bot.send_message(data['chat_id'], message.text, reply_markup=ReplyKeyboardRemove())
        # bot.send_message(data['chat_id'], data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(data['chat_id'], photo_id, data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
    else:
        # bot.send_message(data['chat_id'], data['text'][105], reply_markup=inline_main_menu(data['lang'], from_user_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(data['chat_id'], photo_id, data['text'][105], reply_markup=inline_main_menu(data['lang'], from_user_id))
        db.save_name(message.text, data['user_id'])



@bot.callback_query_handler(func=lambda call: call.data == 'phone')
def reaction_to_name(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    data = get_user_info(call=call)
    msg = bot.send_message(data['chat_id'], data['text'][103], reply_markup=get_phone_number(data['lang']))
    bot.register_next_step_handler(msg, save_phone_number)

def save_phone_number(message: Message):
    contact(message, send_buttons_settings)



@bot.callback_query_handler(func=lambda call: call.data == 'lang')
def reaction_to_name(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    data = get_user_info(call=call)
    msg = bot.send_message(data['chat_id'], data['text'][5], reply_markup=send_language())
    bot.register_next_step_handler(msg, save_language)

def save_language(message: Message):
    from_user_id = message.from_user.id
    if message.text == "🇺🇿O'zbekcha":
        lang = 'uz'
    elif message.text == "🇷🇺Русский":
        lang = 'ru'
    db.update_lang(lang, message.from_user.id)
    data = get_user_info(message=message)
    bot.send_message(from_user_id, message.text, reply_markup=ReplyKeyboardRemove())
    # bot.send_message(data['chat_id'], data['text'][107], reply_markup=inline_main_menu(data['lang'], from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(data['chat_id'], photo_id, data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))



@bot.callback_query_handler(func=lambda call: call.data == 'b_date')
def reaction_to_name(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    get_birth_date(call=call)

def save_birth_date(message: Message):
    data = get_user_info(message=message)
    from_user_id = message.from_user.id
    if message.text in ["⬅️Ortga", "⬅️Назад"]:
        reaction_to_settings(message)
    elif message.text in ["Asosiy menyu", "Главное меню"]:
        bot.send_message(data['chat_id'], message.text, reply_markup=ReplyKeyboardRemove())
        # bot.send_message(data['chat_id'], data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(data['chat_id'], photo_id, data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
    elif '/' in message.text:
        if ''.join(message.text.split('/')).isdigit():
            try:
                db.save_birth_date(message.text, data['user_id'])
            except:
                get_birth_date(message=message)
            # bot.send_message(data['chat_id'], data['text'][109], reply_markup=inline_main_menu(data['lang'], from_user_id))
            photo_id = db.select_photo_from_photo_main()
            bot.send_photo(data['chat_id'], photo_id, data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
        else:
            get_birth_date(message=message)
    else:
        get_birth_date(message=message)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def go_back(call: CallbackQuery):
    from_user_id = call.from_user.id
    data = get_user_info(call=call)
    bot.delete_message(from_user_id, call.message.message_id)
    # bot.send_message(data['chat_id'], data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(data['chat_id'], photo_id, data['text'][101], reply_markup=inline_main_menu(data['lang'], from_user_id))
    # bot.delete_message(data['chat_id'], call.message.message_id)
    # bot.delete_message(data['chat_id'], call.message.message_id)



def get_user_info(call=None, message=None):
    if call:
        chat_id = call.message.chat.id
        from_user_id = call.from_user.id
    elif message:
        chat_id = message.chat.id
        from_user_id = message.from_user.id

    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    try:
        data = {
            'chat_id': chat_id,
            'user_id': from_user_id,
            'lang': lang,
            'text': text
        }
        return data
    except:
        if lang == 'uz':
            text_info = 'Tilni tanlang'
        elif lang == 'ru':
            text_info = 'Выберите язык'
        bot.send_message(chat_id, text_info, send_language())



def get_birth_date(call=None, message=None):
    if call:
        data = get_user_info(call=call)
    elif message:
        data = get_user_info(message=message)
    msg = bot.send_message(data['chat_id'], data['text'][108], reply_markup=back(data['lang']))
    bot.register_next_step_handler(msg, save_birth_date)


# <---
# -----------------------------------------------------------------------------------------------





# -----------------------------------------------------------------------------------------------
# Yetkazib berish turlari buttonidan qaytagigan call lar

@bot.callback_query_handler(func=lambda call: call.data == 'car')
def reaction_to_delivery_car(call: CallbackQuery):
    '''Bu funskiya yetkazib berish uchun'''
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    bot.set_state(from_user_id, CardState.card, chat_id)
    bot.send_message(chat_id, text[19], reply_markup=location(lang))


@bot.callback_query_handler(func=lambda call: call.data == 'foot')
def reaction_to_delivery_car(call: CallbackQuery):
    '''Mijoz o'z mahsulotini olib ketishi uchun'''
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    long = 0
    lat = 0
    # coordinates = f"{lat}, {long}"
    try:
        # location_info1 = nominatim.reverse(coordinates)
        # location_info = f"{location_info1}"[0:90]
        bot.set_state(from_user_id, CardState.card, chat_id)
        with bot.retrieve_data(from_user_id, chat_id) as data:
            if data.get('location'):
                data['location']['lat'] = lat
                data['location']['long'] = long
            else:
                data['location'] = {
                    'lat': lat,
                    'long': long,
                    'text_loc': 'admin'
                }

        try:
            categories = db.select_categories(lang)
            if lang == 'uz':
                text_location = "Lokatsiya qabul qilindi!"
            elif lang == 'ru':
                text_location = 'Место принято!'
            bot.send_message(chat_id, f"<b>{text_location}</b>", reply_markup=ReplyKeyboardRemove())
            try:
                photo = db.select_photo()[-1][0]
            except:
                photo = ''
            if photo:
                bot.send_photo(chat_id, photo=photo, caption=text[120],
                               reply_markup=category_for_admin(categories, lang))
            else:
                bot.send_message(chat_id, text[120], reply_markup=category_for_admin(categories, lang))
        except:
            if lang == 'uz':
                text_error = "Botda hozzircha hech qanday mahsulot yo'q"
            elif lang == 'ru':
                text_error = 'В настоящее время в боте нет товаров'
            bot.send_message(chat_id, text_error, reply_markup=ReplyKeyboardRemove())


        # db.insert_lat_long(long=long, lat=lat, info=f"{location_info}", telegram_id=from_user_id)
    except:
        bot.send_message(chat_id, text[19], reply_markup=delivery(lang))




    # locations_info = db.select_location_info_for_auto_burger(lang)
    #
    # markup = send_location_for_foot(locations_info, lang)
    # bot.delete_message(chat_id, call.message.message_id)
    # bot.send_message(chat_id, 'test', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def from_delivery_to_main_menu(call: CallbackQuery):
    '''Dostavka menyusidan bosh sahifaga qaytish'''
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))


# <---
# -----------------------------------------------------------------------------------------------


'''Lokatsiya bilan ishlash'''
@bot.message_handler(content_types=['location'])
def get_test_location(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    long = message.location.longitude
    lat = message.location.latitude
    # print(lat, 'lat')
    # print(long, 'long')

    coordinates = f"{lat}, {long}"
    try:
        location_info1 = nominatim.reverse(coordinates)
        # print(location_info1)
        location_info = f"{location_info1}"[0:90]

        with bot.retrieve_data(from_user_id, chat_id) as data:
            if data.get('location'):
                data['location']['lat'] = lat
                data['location']['long'] = long
            else:
                data['location'] = {
                    'lat': lat,
                    'long': long,
                    'text_loc': location_info
                }

        db.insert_lat_long(long=long, lat=lat, info=f"{location_info}", telegram_id=from_user_id)
    except:
        bot.send_message(chat_id, text[19], reply_markup=location(lang))


    # bot.send_sticker(chat_id, "CAACAgEAAxkBAAIJf2PgWgbqSiAwngLXMfDLOPld6HHbAAItAgACpyMhRD1AMMntg7S2LgQ",
    #                  reply_markup=ReplyKeyboardRemove())
    # bot.delete_message(chat_id, message.message_id + 2)
    try:
        categories = db.select_categories(lang)
        if lang == 'uz':
            text_location = "Lokatsiya qabul qilindi!"
        elif lang == 'ru':
            text_location = 'Место принято!'
        bot.send_message(chat_id, f"<b>{text_location}</b>", reply_markup=ReplyKeyboardRemove())
        try:
            photo = db.select_photo()[-1][0]
        except:
            photo = ''
        if photo:
            bot.send_photo(chat_id, photo=photo, caption=text[120], reply_markup=category_for_admin(categories, lang))
        else:
            bot.send_message(chat_id, text[120], reply_markup=category_for_admin(categories, lang))
    except:
        if lang == 'uz':
            text_error = "Botda hozzircha hech qanday mahsulot yo'q"
        elif lang == 'ru':
            text_error = 'В настоящее время в боте нет товаров'
        bot.send_message(chat_id, text_error, reply_markup=ReplyKeyboardRemove())



@bot.message_handler(func=lambda message: message.text in ['🧾Мои адреса', "🧾Mening manzillarim"])
def send_info_locations(message: Message):
    '''Bu funksiya ma'lumotlar bazasidamavjudbo'lgan lokatsiyani yuboradi.'''
    # print(message)
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    try:
        info = db.select_info_in_location(from_user_id)
        msg = bot.send_message(chat_id, text[113], reply_markup=send_info_location(info, lang))
        bot.register_next_step_handler(msg, mavjud_lokatsiyani_yuborish)
    except:
        bot.send_message(chat_id, text[19], reply_markup=location(lang))

def mavjud_lokatsiyani_yuborish(message: Message):
    '''Bu funksiya ma'lumotlar bazasidamavjudbo'lgan lokatsiyani yuboradi.'''
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    text_location = message.text
    if text_location in ["⬅️Ortga", "⬅️Назад"]:
        bot.send_message(chat_id, text[19], reply_markup=location(lang))
    try:
        lat_long = db.select_by_text(text_location)
        lat = lat_long[0]
        long = lat_long[1]
        with bot.retrieve_data(from_user_id, chat_id) as data:
            if data.get('location'):
                data['location']['lat'] = lat
                data['location']['long'] = long
            else:
                data['location'] = {
                    'lat': lat,
                    'long': long,
                    'text_loc': text_location
                }
        bot.send_location(chat_id, latitude=lat, longitude=long)


        categories = db.select_categories(lang)
        bot.send_sticker(chat_id, "CAACAgEAAxkBAAIJf2PgWgbqSiAwngLXMfDLOPld6HHbAAItAgACpyMhRD1AMMntg7S2LgQ", reply_markup=ReplyKeyboardRemove())
        bot.delete_message(chat_id, message.message_id + 2)

        try:
            photo = db.select_photo()[-1][0]
        except:
            photo = ''
        if photo:
            bot.send_photo(chat_id, photo=photo, caption=text[120], reply_markup=category_for_admin(categories, lang))
        else:
            bot.send_message(chat_id, text[120], reply_markup=category_for_admin(categories, lang))
    except:
        bot.send_message(chat_id, text[19], reply_markup=location(lang))









# def get_location(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text in ["⬅️Ortga", "⬅️Назад"]:
#         bot.send_sticker(chat_id, 'CAACAgEAAxkBAAIJf2PgWgbqSiAwngLXMfDLOPld6HHbAAItAgACpyMhRD1AMMntg7S2LgQ', reply_markup=ReplyKeyboardRemove())
#         bot.send_message(chat_id, text[112], reply_markup=delivery(lang))
#         bot.delete_message(chat_id, message.message_id + 1)
#     elif message.text in ["🧾Mening manzillarim", "🧾Мои адреса"]:
#         try:
#             info = db.select_info_in_location(from_user_id)
#             msg = bot.send_message(chat_id, text[113], reply_markup=send_info_location(info))
#             bot.register_next_step_handler(msg, mavjud_lokatsiyani_yuborish)
#         except:
#             pass
#     elif message.location:
#         long = message.location.longitude
#         lat = message.location.latitude
#
#         coordinates = f"{lat}, {long}"
#         try:
#             location = nominatim.reverse(coordinates)
#             location_info = f"{location}"[0:90]
#
#             with bot.retrieve_data(from_user_id, chat_id) as data:
#                 if data.get('location'):
#                     data['location']['lat'] = lat
#                     data['location']['long'] = long
#                 else:
#                     data['location'] = {
#                         'lat': lat,
#                         'long': long,
#                         'text_loc': location_info
#                     }
#
#             db.insert_lat_long(long=long, lat=lat, info=f"{location_info}", telegram_id=from_user_id)
#         except:
#             pass
#
#         categoriyani_yuborish(chat_id, from_user_id, lang, lat, long)
#
#
# def mavjud_lokatsiyani_yuborish(message: Message):
#     '''Bu funksiya ma'lumotlar bazasidamavjudbo'lgan lokatsiyani yuboradi.'''
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text_location = message.text
#     try:
#         lat_long = db.select_by_text(text_location)
#         lat = lat_long[0]
#         long = lat_long[1]
#         # text_location = lat_long[2]
#         with bot.retrieve_data(from_user_id, chat_id) as data:
#             if data.get('location'):
#                 data['location']['lat'] = lat
#                 data['location']['long'] = long
#             else:
#                 data['location'] = {
#                     'lat': lat,
#                     'long': long,
#                     'text_loc': text_location
#                 }
#         # with bot.retrieve_data(from_user_id, chat_id) as data:
#         #     data['location']['lat'] = lat
#         #     data['location']['long'] = long
#         bot.send_location(chat_id, latitude=lat, longitude=long)
#         categoriyani_yuborish(chat_id, from_user_id, lang, lat, long)
#     except:
#         pass



# def categoriyani_yuborish(chat_id, from_user_id, lang, lat, long):
#     '''Bu funksiya lokatsiya tanlangandan so'ng kategoriyani yuborish uchun ishlatilinadi.'''
#     categories = db.select_categories(lang)
#     print(categories)
#     text = send_text(lang)
#     bot.send_message(chat_id, text[111], reply_markup=ReplyKeyboardRemove())
#
#     data[from_user_id]['long'] = long
#     data[from_user_id]['lat'] = lat
#     try:
#         photo = db.select_photo()[-1][0]
#     except:
#         photo = ''
#     if photo:
#         bot.send_photo(chat_id, photo=photo, caption=text[120], reply_markup=category_for_admin(categories, lang))
#     else:
#         bot.send_message(chat_id, text[120], reply_markup=category_for_admin(categories, lang))







@bot.callback_query_handler(func=lambda call: "address|" in call.data)
def reaction_to_delivery_car(call: CallbackQuery):
    '''Mijoz o'z mahsulotini olib ketishi uchun'''
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    address_id = int(call.data.split('|')[1])

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'salom')




@bot.callback_query_handler(func=lambda call: call.data == 'back_main_menu')
def from_category_to_main_menu(call: CallbackQuery):
    '''Category menusidan bosh sahifaga qaytish'''
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    # bot.send_message(chat_id, text[16], reply_markup=main_menu(lang))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))


# ----------------------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: "category|" in call.data)
def reaction_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    category_id = call.data.split('|')[1]
    # products = db.select_products_by_category_id(category_id)

    bot.delete_message(chat_id, call.message.message_id)
    # bot.delete_message(chat_id, call.message.message_id - 1)
    bot.send_message(chat_id, text[121], reply_markup=get_products_by_pagination(category_id, lang))


@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    categories = db.select_categories(lang)

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text[120], reply_markup=category_for_admin(categories, lang))


@bot.callback_query_handler(func=lambda call: "next_page|" in call.data)
def reaction_to_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    elements = call.message.reply_markup.keyboard[-2]
    category_id = int(call.data.split('|')[1])
    page = None
    for element in elements:
        # print(element)
        if element.callback_data == 'current_page':
            page = int(element.text)
    page += 1
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text[121], reply_markup=get_products_by_pagination(category_id, lang, page))


@bot.callback_query_handler(func=lambda call: "previous_page|" in call.data)
def reaction_to_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    elements = call.message.reply_markup.keyboard[-2]
    category_id = int(call.data.split("|")[1])

    page = None
    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)
    page -= 1

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text[121], reply_markup=get_products_by_pagination(category_id, lang, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page')
def reaction_to_current_page(call: CallbackQuery):
    elements = call.message.reply_markup.keyboard[-2]
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    page = None
    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)
    if lang == 'uz':
        text_info = f"Siz {page} - sahifadasiz!"
    elif lang == 'ru':
        text_info = f"Вы находитесь на странице {page}!"

    bot.answer_callback_query(call.id, text_info, show_alert=True)


@bot.callback_query_handler(func=lambda call: "product|" in call.data)
def reaction_to_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    product_id = int(call.data.split('|')[1])
    product = db.get_product_by_id(product_id)
    '''product_name, image, content, price, category_id'''
    title, image, content, price, cat_id = product
    # print(cat_id)

    bot.delete_message(chat_id, call.message.message_id)

    if lang == 'uz':
        text_info = f"<b>{title}</b>\nNarhi: <i>{price}</i>\nBatafsil ma'lumot: {content}"
    elif lang == 'ru':
        text_info = f"<b>{title}</b>\nЦена: <i>{price}</i>\nУзнать больше: {content}"

    try:
        bot.send_photo(chat_id, image, caption=text_info, reply_markup=get_product_control_buttons(cat_id, product_id, lang))
    except Exception as e:
        bot.send_message(chat_id, text_info, parse_mode='html', reply_markup=get_product_control_buttons(cat_id, product_id, lang))


@bot.callback_query_handler(func=lambda call: call.data in ['plus', 'minus'])
def reaction_to_plus_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    bot.answer_callback_query(call.id, cache_time=1)

    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    category_id = int(call.message.reply_markup.keyboard[2][0].callback_data.split('|')[1])
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split('|')[1]

    if call.data == 'plus':
        quantity += 1
        bot.edit_message_reply_markup(chat_id, call.message.message_id, call.id,
                                      reply_markup=get_product_control_buttons(category_id, product_id, lang, quantity))
    else:
        if quantity > 1:
            quantity -= 1
            bot.edit_message_reply_markup(chat_id, call.message.message_id, call.id,
                                          reply_markup=get_product_control_buttons(category_id, product_id, lang, quantity))


@bot.callback_query_handler(func=lambda call: call.data == "quantity")
def reaction_to_quantity(call: CallbackQuery):
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    quantity = call.message.reply_markup.keyboard[0][1].text
    if lang == 'uz':
        text_info = f"Jami: {quantity} ta"
    elif lang == 'ru':
        text_info = f"Всего: {quantity}"
    bot.answer_callback_query(call.id, text_info)







@bot.callback_query_handler(func=lambda call: 'add|' in call.data)
def reaction_to_add_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    product_id = call.data.split('|')[1]
    product = db.get_product_by_id(product_id)
    product_name = product[0]
    product_price = product[3]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)


    with bot.retrieve_data(from_user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name] = {
                'product_id': product_id,
                'quantity': quantity,
                'price': product_price
            }
        else:
            data['card'] = {
                product_name: {
                    'product_id': product_id,
                    'quantity': quantity,
                    'price': product_price
                }
            }
        bot.answer_callback_query(call.id, text[122])



@bot.callback_query_handler(func=lambda call: call.data =="show_card")
def reaction_to_show_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    try:
        with bot.retrieve_data(from_user_id, chat_id) as data:
            result = get_text_reply_markup(data, lang, from_user_id)

        text = result['text']
        markup = result['markup']

        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, text, reply_markup=markup)
    except:
        bot.answer_callback_query(call.id, text[132])




@bot.callback_query_handler(func=lambda call: call.data == "mening_buyurtmalarim")
def reaction_to_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text_info = send_text(lang)
    try:
        with bot.retrieve_data(from_user_id, chat_id) as data:
            result = get_text_reply_markup(data, lang, from_user_id)

        text = result['text']
        markup = result['markup']

        bot.send_message(chat_id, text, reply_markup=markup)
    except:
        bot.answer_callback_query(call.id, text_info[129])
        # bot.delete_message(chat_id, call.message.message_id)
        # bot.send_message(chat_id, f"<b>{text_info[132]}</b>", reply_markup=inline_main_menu(lang, from_user_id))
        # photo_id = db.select_photo_from_photo_main()
        # bot.send_photo(chat_id, photo_id, f"<b>{text_info[132]}</b>", reply_markup=inline_main_menu(lang, from_user_id))



# @bot.message_handler(func=lambda message: message.text in ["📋Mening buyurtmalarim", "📋Мои заказы"])
# def reaction_to_order(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text_info = send_text(lang)
#     try:
#         with bot.retrieve_data(from_user_id, chat_id) as data:
#             result = get_text_reply_markup(data, lang)
#
#         text = result['text']
#         markup = result['markup']
#
#         bot.send_message(chat_id, text, reply_markup=markup)
#     except:
#         bot.send_message(chat_id, f"<b>{text_info[132]}</b>")



@bot.callback_query_handler(func=lambda call: "remove|" in call.data)
def reaction_to_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    product_id = call.data.split('|')[1]


    with bot.retrieve_data(from_user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]
        for key in keys:
            if data['card'][key]['product_id'] == product_id:
                del data['card'][key]

    result = get_text_reply_markup(data, lang, from_user_id)
    text = result['text']
    markup = result['markup']
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=markup)


def get_text_reply_markup(data, lang, from_user_id):
    if lang == 'uz':
        text = '<b>Savat:</b>\n'
        narx = "<b>Narxi</b>"
        sum_uz = "so'm"
    elif lang == 'ru':
        text = '<b>Корзина</b>\n'
        narx = "<b>Расходы</b>"
        sum_uz = "сум"
    total_price = 0
    for product_name, item in data['card'].items():
        product_price = item['price']
        quantity = item['quantity']
        price = quantity * int(product_price)
        total_price += price
        text += f'''<b>{product_name}</b> \n{narx}: {quantity} * {product_price} = {price} {sum_uz}\n'''

    if total_price == 0:
        if lang == 'uz':
            text = "Sizning savatingiz bo'sh!"
        elif lang == 'ru':
            text = "Ваша корзина пуста!"
        markup = inline_main_menu(lang, from_user_id)
    else:
        if lang == 'uz':
            text += f"<b>Umumiy narx:</b> <i>{total_price}</i> so'm"
        elif text == 'ru':
            text += f"<b>Общая стоимость:</b> <i>{total_price}</i> сум"
        markup = show_card_buttons(data['card'], lang)

    return {'markup': markup, 'text': text, 'total_price': total_price}


@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_to_clear_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.message_id)
    # bot.answer_callback_query()
    # bot.send_message(chat_id, text[123], reply_markup=inline_main_menu(lang, from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[123], reply_markup=inline_main_menu(lang, from_user_id))


@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def submit_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    from_user_id = call.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text_caption = send_text(lang)
    bot.delete_message(chat_id, call.message.message_id)
    from datetime import datetime

    users = send_telegram_id_all_users()

    with bot.retrieve_data(user_id, user_id) as data:
        customer_full_name = db.check_user_info(user_id)[0]
        phone_number = db.check_user_info(user_id)[1]
        date_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        if customer_full_name == None:
            full_name = f"{call.from_user.full_name}"
        else:
            full_name = customer_full_name
        # print(full_name, 'full_name')
        db.create_order(full_name, str(date_now), user_id)
        create_order = db.select_order(user_id)
        # print(create_order, 'test')
        text = "#buyurtma\n" \
               "<b>Mahsulotlar</b>\n"
        if lang == 'uz':
            text_to_user = "<b>Taomlar</b>\n"
        elif lang == 'ru':
            text_to_user = "<b>Блюды</b>\n"
        order_id = create_order[-1][0]
        total_price_all_products = 0
        for item in data['card']:
            product_name = item
            product_quantity = data['card'][item]['quantity']
            product_price = data['card'][item]['price']
            total_price = int(product_quantity) * int(product_price)
            total_price_all_products += total_price

            text += f"👉<b>{product_name}</b> -> {product_quantity} x {product_price} = {total_price}\n"
            text_to_user += f"👉<b>{product_name}</b> -> {product_quantity} x {product_price} = {total_price}\n"

            db.create_order_item(product_name, product_quantity, product_price, total_price, order_id)

        lat = data['location']['lat']
        long = data['location']['long']
        text_location = data['location']['text_loc']


        text += f"<b>Umumiy narx:</b> <i>{total_price_all_products}</i> so'm\n\n"
        text += f"<b>Xaridor</b>\n" \
                f"<b>Ismi:</b> {full_name}\n" \
                f"<b>Telefon:</b> {phone_number}\n" \
                f"<b>Buyurtma vaqti:</b> {date_now}\n" \
                f"<b>Manzil:</b> {text_location}\n\n"
        if lang == 'uz':
            text_to_user += f"<b>Umumiy narx:</b> <i>{total_price_all_products} so'm</i>\n\n"
        elif lang == 'ru':
            text_to_user += f"<b>Итоговая цена:</b> <i>{total_price_all_products} сум</i>\n\n"



        if int(lat) == 0 and int(long) == 0:
            lat = 41.289159
            long = 69.326543
            text_location = "Педикюр ногтей, Ko'prikli, Yashnobod Tumani, Toshkent, 100000, Oʻzbekiston"

            text_to_user += f"<b>Bizning manzil:</b> {text_location}"
            bot.send_message(chat_id, text_to_user)
            bot.send_location(chat_id, latitude=lat, longitude=long)
            # bot.send_message(chat_id, text_caption[16], reply_markup=inline_main_menu(lang, from_user_id))

            text += f"<b><i>Xaridor o'zi olib ketadi!</i></b>"
            for admin in ADMINS:
                if admin in users:
                    bot.send_message(admin, text)
        else:
            bot.send_message(chat_id, text_to_user)
            # bot.send_message(chat_id, text_caption[16], reply_markup=inline_main_menu(lang, from_user_id))

            for admin in ADMINS:
                if admin in users:
                    bot.send_message(admin, text)
                    bot.send_location(admin, latitude=lat, longitude=long)

    bot.delete_state(user_id, user_id)
    if lang == 'uz':
        text_caption = 'Buyurtmangiz qabul qilindi😊'
    elif lang == 'ru':
        text_caption = 'Ваш заказ принят😊'
    # bot.send_message(chat_id, text_caption, reply_markup=inline_main_menu(lang, chat_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text_caption, reply_markup=inline_main_menu(lang, from_user_id))










    # with bot.retrieve_data(user_id, chat_id) as data:
    #     bot.send_invoice(chat_id, **generate_product_invoice(data['card']).generate_invoice(),
    #                      invoice_payload='shop_bot')
    #



# @bot.pre_checkout_query_handler(func=lambda pre_checkout_query: True)
# def checkout(pre_checkout_query: PreCheckoutQuery):
#     user_id = pre_checkout_query.from_user.id
#     bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message='TEST')
#     bot.send_message(user_id, "Xaridingiz uchun rahmat!")
#     with bot.retrieve_data(user_id, user_id) as data:
#         customer_full_name = db.check_user_info(user_id)[0]
#         create_order = db.create_order(customer_full_name)
#         order_id = create_order[0]
#         for item in data['card']:
#             product_name = item
#             product_quantity = data['card'][item]['quantity']
#             product_price = data['card'][item]['price']
#             total_price = int(product_quantity) * int(product_price) * 100
#
#             db.create_order_item(product_name, product_quantity, product_price, total_price, order_id)
#
#     bot.delete_state(user_id, user_id)
