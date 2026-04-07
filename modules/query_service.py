# query_service.py

import sqlite3
from modules.sql_validator import validate_query

# actually execute a query, using validate_query and returning if it was successful
def execute_query(conn: sqlite3.Connection, sql: str) -> tuple[bool, str, list]:
    is_valid, message = validate_query(conn, sql)

    if not is_valid:
        return False, message, []

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        return True, "OK", results
    except Exception as e:
        return False, str(e), []
