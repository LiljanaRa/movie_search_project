from db_connector import DBConnector
from queries.sakila_queries import FilmQueries
from queries.sqlite_queries import SqliteQueries

class QueryHandler(DBConnector):
    def __init__(self, dbconfig, sqlite_dbconfig):
        super().__init__(dbconfig, sqlite_dbconfig)

    def get_all_by_keyword(self, keyword):
        cursor = self.get_cursor()
        cursor.execute(FilmQueries.GET_ALL_BY_KEYWORD, (f"%{keyword}%", f"%{keyword}%"))
        record = cursor.fetchall()
        if not record:
            return None
        else:
            self.query_log_word("По слову", keyword)
            return record

    def get_all_categories(self):
        cursor = self.get_cursor()
        cursor.execute(FilmQueries.GET_ALL_CATEGORIES)
        category_list = cursor.fetchall()
        return category_list

    def get_all_by_category(self, category, year):
        cursor = self.get_cursor()
        cursor.execute(FilmQueries.GET_ALL_BY_CATEGORY, (f"%{category}%", f"%{year}%"))
        if len(year) == 4:
            result = cursor.fetchall()
            if not result:
                return None
            else:
                self.query_log_category_year("По жанру и году", category, year)
                return result

    def query_log(self, query: str):
        cursor = self.get_sqlite_cursor()
        cursor.execute(SqliteQueries.GET_COUNT, (query,))
        result = cursor.fetchone()
        if not result:
            cursor.execute(SqliteQueries.INSERT_INTO_TABLE, (query,))
        else:
            cursor.execute(SqliteQueries.UPDATE_COUNT, (query,))

        self._sqlite_connection.commit()

    def query_log_word(self, type: str, category: str):
        query = f"{type}: {category}"
        self.query_log(query)

    def query_log_category_year(self, type: str, category: str, year: int):
        query = f"{type}: {category} {year}"
        self.query_log(query)

    def get_popular_queries(self):
        cursor = self.get_sqlite_cursor()
        cursor.execute(SqliteQueries.GET_ALL)
        result = cursor.fetchall()
        return result




