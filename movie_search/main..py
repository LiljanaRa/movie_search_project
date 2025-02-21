import dotenv
from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor
from movie_search.query_manager import QueryHandler

path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=path)
dbconfig = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE'),
    'charset': os.getenv('CHARSET'),
    'cursorclass': DictCursor
 }

sqlite_dbconfig = "my_sqlite.db"

def main(dbconfig, sqlite_dbconfig):
    query_handler = QueryHandler(dbconfig, sqlite_dbconfig)
    while True:
        user_input = input("\nВыбери действие:\n\nДля поиска фильма по ключевому слову введи: 1"'\n'
                           "Для поиска фильма по жанру и году введи: 2\n"
                           "Для вывода самых популярных запросов введи: 3\n"
                           "Для выхода введи: exit\n")

        if user_input == "exit":
            print("До скорой встречи!")
            break
        elif user_input == "1":
            try:
                keyword = input("Введи слово для поиска: ")
                print("\nРезультаты поиска: ", "\n")
                if not query_handler.get_all_by_keyword(keyword):
                    print("По твоему запросу ничего не найдено. Попробуй еще раз!")
                else:
                    print("\n".join([f"Название фильма: {row.get('title')}\nОписание: "
                                 f"{row.get('description')}\n" for row
                                 in query_handler.get_all_by_keyword(keyword)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "2":
            try:
                print("Список жанров: ")
                [print(row.get('name')) for row in query_handler.get_all_categories()]
                category = input("Выбери жанр для поиска: ")
                year = input("Введи год для поиска: ")
                print("\nРезультаты поиска: ", "\n")
                if not query_handler.get_all_by_category(category, year):
                    print("По твоему запросу ничего не найдено. Попробуй еще раз!")
                else:
                    print("\n".join([f"Название фильма: {row.get('title')}\nОписание: "
                                 f"{row.get('description')}\n" for row
                                 in query_handler.get_all_by_category(category, year)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "3":
            try:
                print("Самые популярные запросы: \n")
                for query, count in query_handler.get_popular_queries():
                    print(f"{query} искали {count} раз(а)")
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        else:
            print("Введены некорректные данные.")




if __name__ == "__main__":
     main(dbconfig, sqlite_dbconfig)

