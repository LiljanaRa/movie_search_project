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
        user_input = input("\nSelect an option:\n\nTo search for a movie by keyword, enter: 1"'\n'
                           "To search for a movie by genre and year, enter: 2\n"
                           "To display the most popular queries, enter: 3\n"
                           "To exit, enter: exit\n")

        if user_input == "exit":
            print("See you next time.")
            break
        elif user_input == "1":
            try:
                keyword = input("Enter a word for search: ").capitalize()
                print("\nSearch result: ", "\n")
                if not query_handler.get_all_by_keyword(keyword):
                    print("Nothing was found for your query. Try again!")
                else:
                    print("\n".join([f"Movie title: {row.get('title')}\nDescription: "
                                 f"{row.get('description')}\n" for row
                                 in query_handler.get_all_by_keyword(keyword)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "2":
            try:
                print("List of genres: ")
                [print(row.get('name')) for row in query_handler.get_all_categories()]
                category = input("Select a genre to search: ")
                year = input("Enter the year to search: ")
                print("\nSearch result: ", "\n")
                if not query_handler.get_all_by_category(category, year):
                    print("Nothing was found for your query. Try again!")
                else:
                    print("\n".join([f"Movie title: {row.get('title')}\nDescription: "
                                 f"{row.get('description')}\n" for row
                                 in query_handler.get_all_by_category(category, year)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "3":
            try:
                print("The most popular queries: \n")
                for query, count in query_handler.get_popular_queries():
                    print(f"{query} was searched {count} times")
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        else:
            print("Incorrect data was entered.")




if __name__ == "__main__":
     main(dbconfig, sqlite_dbconfig)

