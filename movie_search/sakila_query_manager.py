from db_connector import SakilaDBConnector
from queries.sakila_queries import SakilaQueries
from movie_search.sqlite_query_manager import SqliteQueryHandler


class SakilaQueryHandler(SakilaDBConnector):
    def __init__(self, dbconfig, sqlite_query_handler: SqliteQueryHandler):
        super().__init__(dbconfig)
        self.sqlite_query_handler = sqlite_query_handler

    def get_all_by_keyword(self, keyword):
        cursor = self.get_cursor()
        cursor.execute(SakilaQueries.GET_ALL_BY_KEYWORD, (f"%{keyword}%", f"%{keyword}%"))
        record = cursor.fetchall()
        if not record:
            return None
        else:
            self.sqlite_query_handler.query_log_word("By the keyword", keyword)
            return record

    def get_all_categories(self):
        cursor = self.get_cursor()
        cursor.execute(SakilaQueries.GET_ALL_CATEGORIES)
        category_list = cursor.fetchall()
        return category_list

    def get_all_by_category(self, category, year):
        cursor = self.get_cursor()
        cursor.execute(SakilaQueries.GET_ALL_BY_CATEGORY, (f"%{category}%", f"%{year}%"))
        if len(year) == 4:
            result = cursor.fetchall()
            if not result:
                return None
            else:
                self.sqlite_query_handler.query_log_category_year("By genre and year", category, year)
                return result


