import dotenv
from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor

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

TOKEN = os.getenv('TOKEN')