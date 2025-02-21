import sqlite3


connector = sqlite3.connect("my_sqlite.db")
cursor = connector.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS popular_queries(
    id integer primary key autoincrement,
    query text,
    count integer
    )
    """
)

connector.commit()

cursor.close()
connector.close()