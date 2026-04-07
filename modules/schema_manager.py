# schema_manager.py

import sqlite3
import pandas as pd

# to translate between pandas types and sql types
PANDAS_TO_SQL = {
    "int64": "INTEGER",
    "float64": "REAL",
    "object": "TEXT",
    "bool": "INTEGER",
    "datetime64[ns]": "TEXT",
}

# translate the data type using the structure above
def infer_schema(df: pd.DataFrame) -> dict:
    return {col: PANDAS_TO_SQL.get(str(dtype), "TEXT") for col, dtype in df.dtypes.items()}

# query with pragma to get the existing table's column info (names/types)
def get_table_schema(conn: sqlite3.Connection, table_name: str) -> dict:
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    return {row[1]: row[2] for row in rows}

# get all the existing tables from this db
def get_all_tables(conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]

# check if the inferred schema matches the existing one to append, or if not to create
def schemas_match(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> bool:
    existing = get_table_schema(conn, table_name)
    inferred = infer_schema(df)
    existing_normalized = {k.lower(): v.upper() for k, v in existing.items() if k != "id"}
    inferred_normalized = {k.lower(): v.upper() for k, v in inferred.items()}
    return existing_normalized == inferred_normalized

# create a new table and add the primary key "id"
def create_table(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame):
    schema = infer_schema(df)
    schema = {col: dtype for col, dtype in schema.items() if col.lower() != "id"} # filter duplicate id column
    columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
    conn.cursor().execute(sql)
    conn.commit()


















