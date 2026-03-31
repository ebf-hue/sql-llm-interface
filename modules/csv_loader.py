# csv_loader.py

import pandas as pd
import sqlite3

# load the csv with given file name/path, return the df
def load_csv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

# execute queries to insert each row of data from the df
def insert_data(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        placeholders = ", ".join(["?"] * len(row))
        columns = ", ".join(row.index.tolist())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()
