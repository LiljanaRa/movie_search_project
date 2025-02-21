import telebot
from telebot import types
import dotenv
from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor
from movie_search.query_manager import QueryHandler


path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=path)
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(token=TOKEN)
dbconfig = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'charset': os.getenv('CHARSET'),
    'cursorclass': DictCursor
 }
sqlite_dbconfig = "my_sqlite.db"
query_handler = QueryHandler(dbconfig, sqlite_dbconfig)

def main(chat_id):
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton("Поиск по заданному слову", callback_data="keyword")
    but2 = types.InlineKeyboardButton("Поиск по жанру и году", callback_data="category")
    markup.row(but1, but2)
    but3 = types.InlineKeyboardButton("Вывести самые популярные запросы", callback_data="popular queries")
    markup.row(but3)
    bot.send_message(chat_id, "Выбери действие:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я твой личный помощник в поиске фильмов.')
    main(message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Обрати внимание на кнопки")
    main(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "keyword":
        mes = bot.send_message(call.message.chat.id, "Введи слово для поиска: ")
        bot.register_next_step_handler(mes, search_by_keyword)
    elif call.data == "category":
        send_categories(call.message.chat.id)
    elif call.data == "popular queries":
        send_popular_queries(call.message.chat.id)
    elif call.data.startswith("category_"):
        category = call.data[9:]
        mes = bot.send_message(call.message.chat.id, f"Введи год:")
        bot.register_next_step_handler(mes, lambda message: search_by_category(message, category))

def search_by_keyword(message):
    keyword = message.text
    try:
        result = query_handler.get_all_by_keyword(keyword)
        if result:
            response = "\n\n".join([f"Название фильма: {row.get('title')}\nОписание: {row.get('description')}" for row in result])
        else:
            response = "По твоему запросу ничего не найдено. Попробуй еще раз!"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error {e}")
    main(message.chat.id)

def send_categories(chat_id):
    categories = query_handler.get_all_categories()
    if categories:
        markup = types.InlineKeyboardMarkup()
        for row in categories:
            markup.add(types.InlineKeyboardButton(row.get('name'), callback_data=f"category_{row.get('name')}"))
        bot.send_message(chat_id, "Выбери жанр:", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Такого жанра нет в списке.")

def search_by_category(message, category):
    year = message.text
    try:
        result = query_handler.get_all_by_category(category, year)
        if not result:
            response = "По твоему запросу ничего не найдено. Попробуй еще раз!"
        else:
            response = "\n\n".join([f"Название фильма: {row.get('title')}\nОписание: {row.get('description')}" for row in result])
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error {e}")
    main(message.chat.id)

def send_popular_queries(chat_id):
    try:
        queries = query_handler.get_popular_queries()
        if queries:
            response = "\n".join(f"{query}  искали  {count} раз(а)" for query, count in queries)
        else:
            response = "Популярных запросов пока нет"
        bot.send_message(chat_id, response)
    except pymysql.Error as e:
        bot.send_message(chat_id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Error {e}")
    main(chat_id)

bot.infinity_polling(none_stop=True)
