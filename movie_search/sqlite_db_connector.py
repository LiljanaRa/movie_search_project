import sqlite3


class SqliteDBConnector():
    def __init__(self, sqlite_dbconfig: str):
        self._sqlite_dbconfig = sqlite_dbconfig
        self._sqlite_connection = self._set_sqlite_connection()
        self._sqlite_cursor = self._set_sqlite_cursor()

    def _set_sqlite_connection(self):
        sql_connection = sqlite3.connect(self._sqlite_dbconfig, check_same_thread=False)
        return sql_connection

    def _set_sqlite_cursor(self):
        sql_cursor = self._sqlite_connection.cursor()
        return sql_cursor

    def get_sqlite_connection(self):
        return self._sqlite_connection

    def get_sqlite_cursor(self):
        return self._sqlite_cursor

    def close(self):
        if self._sqlite_connection:
            self._sqlite_cursor.close()
            self._sqlite_connection.close()