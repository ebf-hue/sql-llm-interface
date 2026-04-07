# sql_validator.py

import sqlite3
from modules.schema_manager import get_all_tables, get_table_schema

# helper functions
def is_select_query(sql: str) -> bool:
    return sql.strip().upper().startswith("SELECT")
def extract_tables(sql: str, known_tables: list) -> list:
    sql_upper = sql.upper()
    return [t for t in known_tables if t.upper() in sql_upper]

# return the bool and also info string
def validate_query(conn: sqlite3.Connection, sql: str) -> tuple[bool, str]:
    if not is_select_query(sql):
        return False, "Only SELECT queries are allowed."

    known_tables = get_all_tables(conn)
    referenced_tables = extract_tables(sql, known_tables)

    if not referenced_tables:
        return False, "Query references no known tables."

    for table in referenced_tables:
        known_columns = list(get_table_schema(conn, table).keys())
        for col in known_columns:
            pass  # column validation can be expanded here

    return True, "Query is valid."
