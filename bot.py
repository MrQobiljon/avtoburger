'''
BOTNI ISHGA TUSHIRISH
'''
from middlewares import SimpleMiddleware
from data.loader import bot, db

import handlers

# db.delete_categories()
# db.delete_products()
# db.drop_table_users()
# db.drop_table_location()
# db.delete_table_location_for_auto_burger_by_info()
# db.delete_table_orders()
# db.delete_table_order_item()
# db.drop_table_location_burger()

db.create_user_table()
db.create_categories_table()
db.create_products_table()
db.create_table_location()
db.create_table_location_for_auto_burger()
db.create_table_photo()
db.create_table_photos_for_categories()
db.create_table_order()
db.create_table_order_item()
db.create_table_for_feedback()
db.create_table_photo_main()
db.insert_id_to_photo_main()


# add_category
# delete_category
# add_product
# delete_product
# add_address
# delete_address
# add_photo



bot.setup_middleware(SimpleMiddleware(1)) # bu botga qayta qayta yozmaslik uchun limit(sekundda) kiritiladi

if __name__ == '__main__':
    bot.infinity_polling()