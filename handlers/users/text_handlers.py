'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove

from config import ADMINS
from data.loader import bot, db
from keyboards.default import get_phone_number, main_menu, send_language, send_info_location, send_cancel
from keyboards.inline import category_for_admin
from texts import send_text
from keyboards.inline import send_buttons_settings, delivery, inline_main_menu
from states.states import CardState


data = {}


@bot.message_handler(func=lambda message: message.text in ["🇺🇿O'zbekcha", "🇷🇺Русский"], chat_types='private')
def get_language(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "🇺🇿O'zbekcha":
        lang = 'uz'
    elif message.text == "🇷🇺Русский":
        lang = 'ru'

    db.update_lang(lang=lang, telegram_id=from_user_id)

    user = db.select_user(telegram_id=from_user_id)

    if None in user:
        lang = db.select_lang(from_user_id)[0]
        text = send_text(lang)

        msg = bot.send_message(chat_id, f"<b>{text[103]}</b>", reply_markup=get_phone_number(lang))
        bot.register_next_step_handler(msg, save_contact)

    else:
        """Bu yerda asosiy markupni yuboramiz."""
        lang = db.select_lang(from_user_id)[0]
        text = send_text(lang)
        # bot.send_message(chat_id, f"<b>{text[101]}</b>", reply_markup=main_menu(lang))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(chat_id, photo_id, f"<b>{text[101]}</b>", reply_markup=inline_main_menu(lang, chat_id))


def save_contact(message: Message):
    contact(message)


@bot.message_handler(func=lambda message: message.text in ["🛍Buyurtma berish", "🛍 Заказать"])
def reaction_to_order(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    data[from_user_id] = {}
    # bot.send_message(chat_id, "Yetkazib berish usulini tanlang", reply_markup=ReplyKeyboardRemove())
    bot.send_sticker(chat_id, 'CAACAgEAAxkBAAIJf2PgWgbqSiAwngLXMfDLOPld6HHbAAItAgACpyMhRD1AMMntg7S2LgQ',
                     reply_markup=ReplyKeyboardRemove())
    bot.delete_message(chat_id, message.message_id + 1)
    bot.send_message(chat_id, text[124], reply_markup=delivery(lang))
    # bot.delete_message(chat_id, message.message_id)
    # bot.register_next_step_handler(msg, get_location)



# @bot.message_handler(func=lambda message: message.text in ["✍️ Izoh qoldirish", "✍️ Оставить отзыв"])
# def reaction_to_comment(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     msg = bot.send_message(chat_id, text[130], reply_markup=send_cancel(lang))
#     bot.register_next_step_handler(msg, send_comment)

#
# def send_comment(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id
#     lang = db.select_lang(from_user_id)[0]
#     text = send_text(lang)
#     if message.text in ["❌ Bekor qilish", "❌ Отмена"]:
#         bot.send_message(chat_id, text[119])
#     else:
#         from datetime import datetime
#         data_now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
#         full_name = message.from_user.full_name
#         comment = message.text
#         text_comment = f"#comment\n" \
#                        f"<b>Kommentariya qoldirildi.</b>\n" \
#                        f"{comment}\n\n" \
#                        f"<b>Komentariya qoldirdi:</b>\n" \
#                        f"{full_name}\n" \
#                        f"<b>Vaqti: {data_now}</b>"
#         for admin in ADMINS:
#             try:
#                 bot.send_message(admin, text_comment)
#             except:
#                 pass
#         bot.send_message(chat_id, text[131], reply_markup=main_menu(lang))





# @bot.message_handler(func=lambda message: message.text in ["☎️Bog'lanish", "☎️Обратная связь"])
# def reaction_to_order(message: Message):
#     chat_id = message.chat.id
#     from_user_id = message.from_user.id


@bot.message_handler(func=lambda message: message.text in ["⚙️Sozlamalar", "⚙️ Настройки"], chat_types='private')
def reaction_to_settings(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.delete_message(chat_id, message.message_id - 1)
    bot.send_message(chat_id, text[102], reply_markup=send_buttons_settings(lang, from_user_id))




def contact(message, func=None):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)

    if func:
        markup = func(lang, from_user_id)
        text1 = text[1]
        text2 = text[106]
    else:
        markup = send_language()
        text1 = text[5]
        text2 = text[101]

    try:
        contact = message.contact.phone_number
        db.save_contact(contact, from_user_id)
        bot.send_message(chat_id, f"<b>{text[137]}</b>", reply_markup=ReplyKeyboardRemove())
        # bot.send_message(chat_id, text2, reply_markup=inline_main_menu(lang, from_user_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(chat_id, photo_id, text2, reply_markup=inline_main_menu(lang, chat_id))
    except:
        if message.text:
            if message.text in ["⬅️Ortga", "⬅️Назад"]:
                bot.delete_message(chat_id, message.message_id - 1)
                bot.send_message(chat_id, text1, reply_markup=markup)
            else:
                msg = bot.send_message(chat_id, f"<b>{text[103]}</b>", reply_markup=get_phone_number(lang))
                bot.register_next_step_handler(msg, save_contact)
        else:
            msg = bot.send_message(chat_id, f"<b>{text[103]}</b>", reply_markup=get_phone_number(lang))
            bot.register_next_step_handler(msg, save_contact)




# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


@bot.message_handler(func=lambda message: message.text in ["⬅️Ortga", "⬅️Назад"])
def go_back(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.send_message(chat_id, message.text, reply_markup=ReplyKeyboardRemove())
    # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))


@bot.message_handler(func=lambda message: message.text in ["Asosiy menyu", "Главное меню", "Bosh sahifa"])
def go_main_menu(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.send_message(chat_id, message.text, reply_markup=ReplyKeyboardRemove())
    # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))


@bot.message_handler(func=lambda message: message.text in ["❌ Bekor qilish", "❌ Отмена"])
def go_to_main_menu_from_comment(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.send_message(chat_id, message.text, reply_markup=ReplyKeyboardRemove())
    # bot.send_message(chat_id, text[16], reply_markup=inline_main_menu(lang, from_user_id))
    photo_id = db.select_photo_from_photo_main()
    bot.send_photo(chat_id, photo_id, text[16], reply_markup=inline_main_menu(lang, chat_id))


