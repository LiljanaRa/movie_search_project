import telebot
from telebot import types
from movie_search.sakila_query_manager import SakilaQueryHandler
from movie_search.sqlite_query_manager import SqliteQueryHandler
from db_config import *


bot = telebot.TeleBot(token=TOKEN)
sqlite_query_handler = SqliteQueryHandler(sqlite_dbconfig)
sakila_query_handler = SakilaQueryHandler(dbconfig, sqlite_query_handler)

def main(chat_id):
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton("Search by given word", callback_data="keyword")
    but2 = types.InlineKeyboardButton("Search by genre and year", callback_data="category")
    markup.row(but1, but2)
    but3 = types.InlineKeyboardButton("Display the most popular queries", callback_data="popular queries")
    markup.row(but3)
    bot.send_message(chat_id, "Select an option:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi! I'm your personal movie search assistant.")
    main(message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Please check the buttons")
    main(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "keyword":
        mes = bot.send_message(call.message.chat.id, "Enter a word to search: ")
        bot.register_next_step_handler(mes, search_by_keyword)
    elif call.data == "category":
        send_categories(call.message.chat.id)
    elif call.data.startswith("category_"):
        category = call.data[9:]
        get_years_by_category(call.message.chat.id, category)
    elif call.data.startswith("year_"):
        search_by_category(call)
    elif call.data == "popular queries":
        send_popular_queries(call.message.chat.id)

def search_by_keyword(message):
    keyword = message.text
    try:
        result = sakila_query_handler.get_all_by_keyword(keyword)
        if result:
            response = "Search result:\n\n"+"\n\n".join([f"Movie title: {row.get('title')}\nDescription: "
                                    f"{row.get('description')}" for row in result])
        else:
            response = "Nothing was found for your query. Try again!"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error {e}")
    main(message.chat.id)

def send_categories(chat_id):
    categories = sakila_query_handler.get_all_categories()
    if categories:
        markup = types.InlineKeyboardMarkup()
        for row in categories:
            markup.add(types.InlineKeyboardButton(row.get('name'), callback_data=f"category_{row.get('name')}"))
        bot.send_message(chat_id, "Select a genre:", reply_markup=markup)

def get_years_by_category(chat_id, category):
    years = sakila_query_handler.get_years_by_category(category)
    markup = types.InlineKeyboardMarkup()
    for year in years:
        markup.add(types.InlineKeyboardButton(year.get('release_year'), callback_data=f"year_{category}_{year.get('release_year')}"))
    bot.send_message(chat_id, f"Select a year for the genre: {category}\n\n", reply_markup=markup)

def search_by_category(call):
    _, category, year = call.data.split("_")
    try:
        result = sakila_query_handler.get_all_by_category(category, year)
        if not result:
            response = "Nothing was found for your query. Try again!"
        else:
            response = "Search result:\n\n"+"\n\n".join([f"Movie title: {row.get('title')}\nDescription: {row.get('description')}" for row in result])
        bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
    except pymysql.Error as e:
        bot.send_message(call.message.chat.id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error {e}")
    main(call.message.chat.id)

def send_popular_queries(chat_id):
    try:
        queries = sqlite_query_handler.get_popular_queries()
        if queries:
            response = "The most popular queries:\n\n"+"\n".join(f"{query}  was searched  {count} times" for query, count in queries)
        else:
            response = "No popular queries yet"
        bot.send_message(chat_id, response)
    except pymysql.Error as e:
        bot.send_message(chat_id, f"SQLError {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Error {e}")
    main(chat_id)


bot.infinity_polling(none_stop=True)
