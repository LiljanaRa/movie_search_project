class SqliteQueries():
    GET_COUNT = """
        SELECT count 
        FROM popular_queries
        WHERE query = ?
    """
    UPDATE_COUNT = """
        UPDATE popular_queries
        SET count = count + 1
        WHERE query = ?
    """
    INSERT_INTO_TABLE = """
        INSERT INTO popular_queries (query, count)
        VALUES (?, 1)
    """
    GET_ALL = """
        SELECT query, count
        FROM popular_queries
        ORDER BY count DESC
        LIMIT 10
    """




