'''KOMANDALARNI ILADIGAN HANDLERLAR'''

from telebot.types import Message
from data.loader import bot, db
from keyboards.default import main_menu, send_language
from keyboards.inline import category_for_admin, inline_main_menu
from texts import send_text


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    # print(message)
    chat_id = message.chat.id
    try:
        db.insert_telegram_id(telegram_id=chat_id)
    except:
        pass
    full_name = message.from_user.full_name
    user = db.select_user(telegram_id=chat_id)
    if None in user:
        sent_text_to_user = f"<b>🇺🇿Assalomu alaykum {full_name}. <i>AvtoBurger</i> botiga xush kelibsiz!\n" \
                            f"Davom etish uchun tilni tanlang\n\n" \
                            f"🇷🇺Здравствуйте {full_name}. Добро пожаловать в бот <i>AutoBurger</i>!\n" \
                            f"Выберите язык, чтобы продолжить</b>"
        bot.send_message(chat_id, sent_text_to_user, reply_markup=send_language())
    else:
        lang = db.select_lang(chat_id)[0]
        text = send_text(lang)
        photo_id = db.select_photo_from_photo_main()
        # bot.send_message(chat_id, text[101], reply_markup=inline_main_menu(lang, chat_id))
        photo_id = db.select_photo_from_photo_main()
        bot.send_photo(chat_id, photo_id, text[101], reply_markup=inline_main_menu(lang, chat_id))

