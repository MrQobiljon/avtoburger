'''
SIZ BU YERDA INLINE KNOPKALAR YARATA OLASIZ
'''
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import send_text
from data.loader import db
from config import ADMINS


# ------------------------------------------------------------------------------------------------

def inline_main_menu(lang, chat_id=None):
    text = send_text(lang)
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text[0], callback_data="buyurtma_berish")
    btn2 = InlineKeyboardButton(text[1], callback_data="sozlamalar")
    btn3 = InlineKeyboardButton(text[2], callback_data="mening_buyurtmalarim")
    btn4 = InlineKeyboardButton(text[3], callback_data="izoh_qoldirish")
    btn5 = InlineKeyboardButton(text[4], callback_data="boglanish")

    btn6 = InlineKeyboardButton('Admin panel', callback_data='admin_panel')

    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    if chat_id != None:
        if chat_id in ADMINS:
            markup.add(btn6)
    return markup










# ------------------------------------------------------------------------------------------------



def send_buttons_settings(lang, telegram_id):
    '''Sozlamalar qismini buttoni'''
    text = send_text(lang)
    name = db.select_name(telegram_id)[0]
    if name:
        info_name = text[7]
    else:
        info_name = text[8]
    birth_date = db.select_birth_date(telegram_id)[0]
    if birth_date:
        info_birth_name = text[13]
    else:
        info_birth_name = text[12]
    markup = InlineKeyboardMarkup()
    lang = InlineKeyboardButton(text[10] + text[5], callback_data="lang")
    p_number = InlineKeyboardButton(text[6], callback_data="phone")
    name = InlineKeyboardButton(info_name, callback_data="name")
    b_date = InlineKeyboardButton(info_birth_name, callback_data="b_date")
    back = InlineKeyboardButton(text[11], callback_data="back")
    markup.add(name, lang, b_date, p_number, row_width=2)
    markup.row(back)
    return markup


def delivery(lang):
    """Yetkazib berish turlari"""
    markup = InlineKeyboardMarkup()
    text = send_text(lang)
    car = InlineKeyboardButton(text[17], callback_data="car")
    on_foot = InlineKeyboardButton(text[18], callback_data="foot")
    back = InlineKeyboardButton(text[11], callback_data="main_menu")
    markup.add(car, on_foot)
    markup.add(back)
    return markup


def category_for_admin(categories, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    text = send_text(lang)
    print(categories)
    for category in categories:
        print(category[1], category[0])
        btn = InlineKeyboardButton(category[1], callback_data=f"category|{category[0]}")
        markup.row(btn)

    back = InlineKeyboardButton(text[11], callback_data="buyurtma_berish")
    main_menu = InlineKeyboardButton(text[16], callback_data="main_menu")
    markup.add(back, main_menu)
    return markup





# ------------------------------------------------------------------


def get_products_list_buttons(products_list, lang):
    text = send_text(lang)
    markup = InlineKeyboardMarkup(row_width=1)

    for item in products_list:
        btn = InlineKeyboardButton(item[0], callback_data=f"product|{item[1]}")
        markup.add(btn)

    back = InlineKeyboardButton(text[11], callback_data="back_categories")
    markup.add(back)

    return markup


def get_products_by_pagination(category_id, lang, page=1):
    text = send_text(lang)
    markup = InlineKeyboardMarkup()

    limit = 6
    count = db.count_products_by_category_id(category_id)
    # print(count)

    offset = 0 if page == 1 else (page - 1) * limit

    max_page = count // limit if count % limit == 0 else count // limit + 1

    products = db.select_products_by_pagination(category_id, offset, limit)
    # print(products, 'test uchun')
    for product in products:
        markup.add(InlineKeyboardButton(product[0], callback_data=f"product|{product[1]}"))


    back = InlineKeyboardButton("⏮", callback_data=f"previous_page|{category_id}")
    current_page = InlineKeyboardButton(f"{page}", callback_data="current_page")
    next = InlineKeyboardButton("⏭", callback_data=f"next_page|{category_id}")

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    elif page == max_page:
        markup.row(back, current_page)

    markup.add(InlineKeyboardButton(text[11], callback_data="back_categories"),
               InlineKeyboardButton(text[16], callback_data="main_menu"))

    return markup


def get_product_control_buttons(category_id, product_id, lang, quantity=1):
    text = send_text(lang)
    quantity_btn = [
        InlineKeyboardButton("➖", callback_data='minus'),
        InlineKeyboardButton(quantity, callback_data="quantity"),
        InlineKeyboardButton("➕", callback_data="plus")
    ]

    card = [
        InlineKeyboardButton(text[22], callback_data=f"add|{product_id}"),
        InlineKeyboardButton(text[23], callback_data=f"show_card")
    ]

    backs = [
        InlineKeyboardButton(text[11], callback_data=f"category|{category_id}"),
        InlineKeyboardButton(text[24], callback_data="back_categories")
    ]

    main_menu = [
        InlineKeyboardButton(text[16], callback_data="main_menu")
    ]

    return InlineKeyboardMarkup(keyboard=[
        quantity_btn, card, backs, main_menu
    ], row_width=1)



def show_card_buttons(data: dict, lang):
    text = send_text(lang)
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        btn = InlineKeyboardButton(f"❌ {product_name}", callback_data=f"remove|{product_id}")
        markup.add(btn)

    back = InlineKeyboardButton(text[24], callback_data="back_categories")
    clear = InlineKeyboardButton(text[25], callback_data="clear_card")
    order = InlineKeyboardButton(text[26], callback_data="submit")

    markup.row(clear, order)
    markup.row(back)

    return markup


def send_location_for_foot(locations_info, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    text = send_text(lang)
    for location_info in locations_info:
        btn = InlineKeyboardButton(location_info[0], callback_data=f'address|{location_info[1]}')
        markup.add(btn)
    btn_back = InlineKeyboardButton(text[11], callback_data='b1')
    markup.add(btn_back)
    return markup