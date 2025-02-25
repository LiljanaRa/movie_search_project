from db_config import *
from movie_search.sakila_query_manager import SakilaQueryHandler
from sqlite_query_manager import SqliteQueryHandler


def main():
    sqlite_query_handler = SqliteQueryHandler(sqlite_dbconfig)
    sakila_query_handler = SakilaQueryHandler(dbconfig, sqlite_query_handler)

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
                keyword = input("Enter a word for search: ")
                print("\nSearch result: ", "\n")
                if not sakila_query_handler.get_all_by_keyword(keyword):
                    print("Nothing was found for your query. Try again!")
                else:
                    print("\n".join([f"Movie title: {row.get('title')}\nDescription: "
                                 f"{row.get('description')}\n" for row
                                 in sakila_query_handler.get_all_by_keyword(keyword)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "2":
            try:
                print("List of genres: ")
                [print(row.get('name')) for row in sakila_query_handler.get_all_categories()]
                category = input("Select a genre to search: ")
                year = input("Enter the year to search: ")
                print("\nSearch result: ", "\n")
                if not sakila_query_handler.get_all_by_category(category, year):
                    print("Nothing was found for your query. Try again!")
                else:
                    print("\n".join([f"Movie title: {row.get('title')}\nDescription: "
                                 f"{row.get('description')}\n" for row
                                 in sakila_query_handler.get_all_by_category(category, year)]))
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        elif user_input == "3":
            try:
                print("The most popular queries: \n")
                for query, count in sqlite_query_handler.get_popular_queries():
                    print(f"{query} was searched {count} times")
            except pymysql.Error as e:
                print("SQLError", e)
            except Exception as e:
                print("Error", e)
        else:
            print("Incorrect data was entered.")




if __name__ == "__main__":
     main()

