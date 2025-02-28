class SakilaQueries:
    GET_ALL_BY_KEYWORD = """
        SELECT title, description
        FROM film
        WHERE description
        LIKE %s
        OR title
        LIKE %s
        LIMIT 10
    """
    GET_ALL_CATEGORIES = """
        SELECT name
        FROM category
    """
    GET_YEARS_BY_CATEGORY = """
        SELECT DISTINCT release_year
        FROM film f
        JOIN film_category fc 
        ON f.film_id = fc.film_id
        JOIN category c 
        ON fc.category_id = c.category_id
        WHERE name = %s 
        ORDER BY release_year DESC
        """
    GET_ALL_BY_CATEGORY ="""
        SELECT title, description
        FROM film f
        JOIN film_category fc 
        ON f.film_id = fc.film_id
        JOIN category c 
        ON fc.category_id = c.category_id
        WHERE name
        LIKE %s
        AND release_year
        LIKE %s
        LIMIT 10
    """


