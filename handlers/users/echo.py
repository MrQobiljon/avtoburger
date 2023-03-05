from data.loader import bot, db
from telebot.types import Message
from texts import send_text


@bot.message_handler(content_types=['text'])
def echo(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.select_lang(from_user_id)[0]
    text = send_text(lang)
    bot.send_message(chat_id, text[125])


# @bot.message_handler(content_types=['photo'])
# def echo(message: Message):
#     photo = message.photo[-1].file_id
#     print(photo)