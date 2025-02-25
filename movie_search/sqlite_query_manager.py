from sqlite_db_connector import SqliteDBConnector
from queries.sqlite_queries import SqliteQueries


class SqliteQueryHandler(SqliteDBConnector):
    def __init__(self, sqlite_dbconfig):
        super().__init__(sqlite_dbconfig)

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