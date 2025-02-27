import pymysql
import sqlite3
from abc import ABC, abstractmethod


class DBConnector(ABC):

    @abstractmethod
    def set_connection(self):
        pass

    @abstractmethod
    def set_cursor(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_cursor(self):
        pass

    @abstractmethod
    def close(self):
        pass


class SakilaDBConnector(DBConnector):
    def __init__(self, dbconfig: dict):
        self._dbconfig = dbconfig
        self._connection = self.set_connection()
        self._cursor = self.set_cursor()

    def set_connection(self):
        connection = pymysql.connect(**self._dbconfig)
        return connection

    def set_cursor(self):
        cursor = self._connection.cursor()
        return cursor

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor

    def close(self):
        if self._connection.open:
            self._cursor.close()
            self._connection.close()


class SqliteDBConnector(DBConnector):
    def __init__(self, sqlite_dbconfig: str):
        self._sqlite_dbconfig = sqlite_dbconfig
        self._sqlite_connection = self.set_connection()
        self._sqlite_cursor = self.set_cursor()

    def set_connection(self):
        sql_connection = sqlite3.connect(self._sqlite_dbconfig, check_same_thread=False)
        return sql_connection

    def set_cursor(self):
        sql_cursor = self._sqlite_connection.cursor()
        return sql_cursor

    def get_connection(self):
        return self._sqlite_connection

    def get_cursor(self):
        return self._sqlite_cursor

    def close(self):
        if self._sqlite_connection:
            self._sqlite_cursor.close()
            self._sqlite_connection.close()
