# import psycopg2
# from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD


import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_user_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id INT PRIMARY KEY,
            user_full_name VARCHAR(30),
            phone_number VARCHAR(18),
            birth_date DATE,
            language VARCHAR(3),
            admin VARCHAR(5)
        )'''
        self.execute(sql, commit=True)

    # @staticmethod
    # def format_args(sql, parameters: dict):
    #     sql += " AND ".join([
    #         f"{item} = ?" for item in parameters
    #     ])
    #     return sql, tuple(parameters.values())

    def select_telegram_id_all_users(self):
        sql = '''SELECT telegram_id FROM users'''
        return self.execute(sql, fetchall=True)

    def drop_table_users(self):
        sql = '''DROP TABLE users'''
        self.execute(sql, commit=True)

    def check_user_info(self, telegram_id):
        sql = '''SELECT user_full_name, phone_number, birth_date FROM users
        WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def insert_telegram_id(self, telegram_id):
        sql = """
        INSERT INTO users(telegram_id) VALUES(?)
        """
        self.execute(sql, parameters=(telegram_id,), commit=True)

    def select_user(self, telegram_id):
        sql = '''SELECT phone_number, language FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)
        # return self.execute(sql, telegram_id, fetchone=True)

    def update_lang(self, lang, telegram_id):
        sql = '''UPDATE users SET language = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(lang, telegram_id), commit=True)
        # self.execute(sql, lang, telegram_id, commit=True)

    def save_contact(self, contact, telegram_id):
        sql = '''UPDATE users SET phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(contact, telegram_id), commit=True)
        # self.execute(sql, contact, telegram_id, commit=True)

    def select_lang(self, telegram_id):
        sql = '''SELECT language FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def select_name(self, telegram_id):
        sql = '''SELECT user_full_name FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def select_birth_date(self, telegram_id):
        sql = '''SELECT birth_date FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def save_name(self, username, telegram_id):
        sql = '''UPDATE users SET user_full_name = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(username, telegram_id,), commit=True)

    def save_birth_date(self, b_date, telegram_id):
        sql = '''UPDATE users SET birth_date = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(b_date, telegram_id), commit=True)

    def create_table_location(self):
        sql = '''CREATE TABLE IF NOT EXISTS location(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        info TEXT,
        lat FLOAT,
        long FLOAT,
        telegram_id INTEGER REFERENCES users(telegram_id)
        )'''
        self.execute(sql, commit=True)

    def drop_table_location(self):
        sql = '''DROP TABLE location'''
        self.execute(sql, commit=True)

    def insert_lat_long(self, lat, long, telegram_id, info):
        sql = '''INSERT INTO location(lat, long, telegram_id, info) VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters=(lat, long, telegram_id, info), commit=True)

    def select_lat_long(self, telegram_id):
        sql = '''SELECT long, lat, info FROM location WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchall=True)

    def select_info_in_location(self, telegram_id):
        sql = '''SELECT info FROM location WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchall=True)

    def select_by_text(self, text):
        sql = '''SELECT lat, long FROM location WHERE info = ?'''
        return self.execute(sql, parameters=(text,), fetchone=True)

    def create_categories_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category VARCHAR(200) UNIQUE,
            lang VARCHAR(3)
        )'''
        self.execute(sql, commit=True)

    def delete_categories(self):
        sql = '''DROP TABLE categories'''
        self.execute(sql, commit=True)

    def insert_category(self, name, lang):
        sql = '''INSERT INTO categories(category, lang) VALUES (?, ?)'''
        self.execute(sql, parameters=(name, lang), commit=True)

    def select_categories(self, lang):
        sql = '''SELECT id, category FROM categories WHERE lang = ?'''
        return self.execute(sql, parameters=(lang,), fetchall=True)

    def delete_category(self, category):
        sql = '''DELETE FROM categories WHERE category = ?'''
        self.execute(sql, parameters=(category,), commit=True)

    def select_category_id(self, category):
        sql = '''SELECT id FROM categories WHERE category = ?'''
        return self.execute(sql, parameters=(category,), fetchone=True)

    def create_products_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(200) UNIQUE,
            image TEXT,
            content TEXT,
            price INT NULL,
            lang VARCHAR(3),
            category_id INTEGER REFERENCES categories(id)
        )'''
        self.execute(sql, commit=True)

    def delete_products(self):
        sql = '''DROP TABLE products'''
        self.execute(sql, commit=True)

    def add_product(self, product_name, image, content, price, lang, category_id):
        sql = '''INSERT iNTO products(product_name, image, content, price, lang, category_id)
        VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters=(product_name, image, content, price, lang, category_id), commit=True)

    def select_all_products(self, lang):
        sql = '''SELECT product_name FROM products WHERE lang = ?'''
        return self.execute(sql, parameters=(lang,), fetchall=True)

    def delete_product(self, product):
        sql = '''DELETE FROM products WHERE product_name = ?'''
        self.execute(sql, parameters=(product,), commit=True)

    def count_products_by_category_id(self, category_id):
        sql = '''SELECT count(product_id) FROM products WHERE category_id = ?'''
        return self.execute(sql, parameters=(category_id,), fetchone=True)[0]

    # def select_products_by_pagination(self, category_id, offset, limit):
    #     sql = '''SELECT product_name, product_id FROM products WHERE category_id = ? and (select count(product_id) from products) = ?
    #     and (select count(product_id) from products) = ?'''
    #     return self.execute(sql, parameters=(category_id, offset, limit), fetchall=True)

    # def select_products_by_pagination(self, category_id, offset, limit):
    #     sql = '''SELECT product_name, product_id FROM products WHERE category_id = ? and ((select count(product_id) from products) > ?
    #     and (select count(product_id) from products) < ?)'''
    #     return self.execute(sql, parameters=(category_id, offset, limit), fetchall=True)

    def select_products_by_pagination(self, category_id, offset, limit):
        sql = '''SELECT product_name, product_id FROM products WHERE category_id = ?
        LIMIT ?, ?'''
        return self.execute(sql, parameters=(category_id, offset, limit), fetchall=True)

    def get_product_by_id(self, product_id):
        sql = '''SELECT product_name, image, content, price, category_id
        FROM products WHERE product_id = ?'''
        return self.execute(sql, parameters=(product_id,), fetchone=True)





    def create_table_photo(self):
        sql = '''CREATE TABLE IF NOT EXISTS photos(
            id INTEGER PRiMARY KEY AUTOINCREMENT,
            photo TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_photo(self, photo):
        sql = '''INSERT INTO photos(photo) VALUES (?)'''
        self.execute(sql, parameters=(photo,), commit=True)

    def select_photo(self):
        sql = '''SELECT photo FROM photos'''
        return self.execute(sql, fetchall=True)


    # def select_products_by_category_id(self, category_id):
    #     sql = '''SELECT product_name, product_id FROM products WHERE category_id = ?'''
    #     return self.execute(sql, parameters=(category_id,), fetchall=True)



    def create_table_photos_for_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS photos_for_categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )'''
        self.execute(sql, commit=True)

    def insert_photos_for_categories(self, photo, category_id):
        sql = '''INSERT INTO photos_for_categories(photo, category_id) VALUES (?, ?)'''
        self.execute(sql, parameters=(photo, category_id), commit=True)

    def select_photo_for_category(self, category_id):
        sql = '''SELECT photo FROM photos_for_categories WHERE category_id = ?'''
        self.execute(sql, parameters=(category_id,), fetchone=True)




    def create_table_location_for_auto_burger(self):
        sql = '''CREATE TABLE IF NOT EXISTS location_burger(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            info TEXT,
            lat FLOAT,
            long FLOAT,
            name_address TEXT,
            phone_number VARCHAR(25),
            lang VARCHAR(3)
        )'''
        self.execute(sql, commit=True)

    def drop_table_location_burger(self):
        sql = '''DROP TABLE location_burger'''
        self.execute(sql, commit=True)

    def insert_loc_auto_burger(self, info, lat, long, name_address, phone_number, lang):
        sql = '''INSERT INTO location_burger(info, lat, long, name_address, phone_number, lang)
        VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters=(info, lat, long, name_address, phone_number, lang), commit=True)

    def select_location_info_for_auto_burger(self, lang):
        sql = '''SELECT name_address, id FROM location_burger WHERE lang = ?'''
        return self.execute(sql, parameters=(lang,), fetchall=True)

    def delete_location_for_auto_burger_by_name_address(self, name_address):
        sql = '''DELETE FROM location_burger WHERE name_address = ?'''
        self.execute(sql, parameters=(name_address,), commit=True)

    # def delete_table_location_for_auto_burger_by_info(self):
    #     sql = '''DROP TABLE IF EXISTS location_burger'''
    #     self.execute(sql, commit=True)

    # def select_location_info_for_auto_burger(self):
    #     sql = '''SELECT info FROM location_burger'''
    #     return self.execute(sql, fetchall=True)





    def create_table_order(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            date VARCHAR(23),
            telegram_id int
        )'''
        self.execute(sql, commit=True)

    def create_table_order_item(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS orderitem(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_quantity INTEGER,
            product_price BIGINT,
            product_total_price BIGINT,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE
        )'''
        self.execute(sql, commit=True)

    def delete_table_orders(self):
        sql = '''DROP TABLE orders'''
        self.execute(sql, commit=True)


    def create_order(self, customer_name, date_now, telegram_id):
        sql = '''
        INSERT INTO orders(customer_name, date, telegram_id)
        VALUES (?, ?, ?)
        '''
        self.execute(sql, parameters=(customer_name, date_now, telegram_id), commit=True)

    def select_order(self, telegram_id):
        sql = '''SELECT id FROM orders WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(telegram_id,), fetchall=True)

    def delete_table_order_item(self):
        sql = '''DROP TABLE orderitem'''
        self.execute(sql, commit=True)

    def create_order_item(self, product_name, product_quantity, product_price, product_total_price, order_id):
        sql = '''
        INSERT INTO orderitem(product_name, product_quantity, product_price, product_total_price, order_id)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.execute(sql, parameters=(product_name, product_quantity, product_price, product_total_price, order_id), commit=True)



    def create_table_for_feedback(self):
        sql = '''CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number VARCHAR(18)
        )'''
        self.execute(sql, commit=True)

    def insert_phone_from_feedback(self, phone_number):
        sql = '''INSERT INTO feedback(phone_number)
        VALUES (?)'''
        self.execute(sql, parameters=(phone_number,), commit=True)

    def select_phone_nums_from_feedback(self):
        sql = '''SELECT phone_number FROM feedback'''
        return self.execute(sql, fetchall=True)

    def delete_phone_num_from_feedback(self, phone_number):
        sql = '''DELETE FROM feedback WHERE phone_number = ?'''
        self.execute(sql, parameters=(phone_number,), commit=True)



    def create_table_photo_main(self):
        sql = '''CREATE TABLE IF NOT EXISTS photo_main(
            id INTEGER NOT NULL UNIQUE,
            photo TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_id_to_photo_main(self):
        sql = '''INSERT INTO photo_main(id)
        VALUES (1)
        ON CONFLICT DO NOTHING'''
        self.execute(sql, commit=True)

    def update_photo_for_id_from_photo_main(self, photo):
        sql = '''UPDATE photo_main SET photo = ? WHERE id = 1'''
        self.execute(sql, parameters=(photo,), commit=True)

    def select_photo_from_photo_main(self):
        sql = '''SELECT photo FROM photo_main WHERE id = 1'''
        return self.execute(sql, fetchone=True)[0]




    # def create_table_test_order(self):
    #     sql = '''CREATE TABLE IF NOT EXISTS test_orders(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         product_name TEXT,
    #         telegram_id INT
    #     )'''
    #     self.execute(sql, commit=True)
    #
    # def insert_test_orders(self, product_name, telegram_id):
    #     sql = '''INSERT INTO test_orders(product_name, telegram_id) VALUES (?, ?)'''
    #     self.execute(sql, parameters=(product_name, telegram_id), commit=True)

























# class DataBase:
#     def __init__(self):
#         self.database = psycopg2.connect(
#             database=DB_NAME,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             host=DB_HOST #AGARDA PORT BO'LSA PORTNI QO'SHING
#         )
#     '''MANAGER ORQALI SQL SAVOLLARNI ISHLATING!'''
#     def manager(self, sql, *args,
#                 fetchone:bool=False,
#                 fetchall:bool=False,
#                 fetchmany:bool=False,
#                 commit:bool=False):
#         with self.database as db:
#             with db.cursor() as cursor:
#                 cursor.execute(sql, args)
#                 if commit:
#                     result = db.commit()
#                 elif fetchone:
#                     result = cursor.fetchone()
#                 elif fetchall:
#                     result = cursor.fetchall()
#                 elif fetchmany:
#                     result = cursor.fetchmany()
#             return result
#
#     def create_user_table(self):
#         sql = '''CREATE TABLE IF NOT EXISTS users(
#             telegram_id BIGINT PRIMARY KEY,
#             user_full_name VARCHAR(30),
#             phone_number VARCHAR(18),
#             birth_date DATE,
#             language VARCHAR(3)
#         )'''
#         self.manager(sql, commit=True)
#
#     def insert_telegram_id(self, telegram_id):
#         sql = '''INSERT INTO users(telegram_id)
#         VALUES (%s)
#         ON CONFLICT DO NOTHING'''
#         self.manager(sql, (telegram_id,), commit=True)
#
#     def select_user(self, telegram_id):
#         sql = '''SELECT phone_number, language FROM users WHERE telegram_id = %s'''
#         return self.manager(sql, telegram_id, fetchone=True)
#
#     def update_lang(self, lang, telegram_id):
#         sql = '''UPDATE users SET language = %s WHERE telegram_id = %s'''
#         self.manager(sql, lang, telegram_id, commit=True)
#
#     def save_contact(self, contact, telegram_id):
#         sql = '''UPDATE users SET phone_number = %s WHERE telegram_id = %s'''
#         self.manager(sql, contact, telegram_id, commit=True)
#
#     def select_lang(self, telegram_id):
#         sql = '''SELECT language FROM users WHERE telegram_id = %s'''
#         return self.manager(sql, telegram_id, fetchone=True)
#
#     def select_name(self, telegram_id):
#         sql = '''SELECT user_full_name FROM users WHERE telegram_id = %s'''
#         return self.manager(sql, telegram_id, fetchone=True)
#
#     def select_birth_date(self, telegram_id):
#         sql = '''SELECT birth_date FROM users WHERE telegram_id = %s'''
#         return self.manager(sql, telegram_id, fetchone=True)
#
#     def save_name(self, username, telegram_id):
#         sql = '''UPDATE users SET user_full_name = %s WHERE telegram_id = %s'''
#         self.manager(sql, username, telegram_id, commit=True)
#
#     def save_birth_date(self, b_date, telegram_id):
#         sql = '''UPDATE users SET birth_date = %s WHERE telegram_id = %s'''
#         self.manager(sql, b_date, telegram_id, commit=True)
