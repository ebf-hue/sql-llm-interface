# cli.py

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlite_setup import get_connection
from csv_loader import load_csv, insert_data
from schema_manager import get_all_tables, schemas_match, create_table
from query_service import execute_query
from llm_adapter import translate_to_sql

DB_PATH = "data/database.db"

def main():
    conn = get_connection(DB_PATH)
    print("Welcome to the SQL-LLM Interface! Commands: load, query, ask, tables, exit")

    while True:
        command = input("\n> ").strip().lower()

        if command == "exit":
            break

        elif command == "tables":
            print(get_all_tables(conn))

        elif command == "load":
            filepath = input("CSV filepath: ").strip()
            df = load_csv(filepath)
            table_name = input("table name: ").strip()
            tables = get_all_tables(conn)
            if table_name in tables:
                if schemas_match(conn, table_name, df):
                    insert_data(conn, table_name, df)
                    print("data appended.")
                else:
                    print("schema mismatch.")
            else:
                create_table(conn, table_name, df)
                insert_data(conn, table_name, df)
                print("table created and data loaded.")

        elif command == "query":
            sql = input("SQL: ").strip()
            success, message, results = execute_query(conn, sql)
            print(message if not success else results)

        elif command == "ask":
            user_query = input("question: ").strip()
            sql = translate_to_sql(conn, user_query)
            print(f"generated SQL: {sql}")
            success, message, results = execute_query(conn, sql)
            print(message if not success else results)

        else:
            print("Oops, unknown command. Use load, query, ask, tables, or exit.")

if __name__ == "__main__":
    main()



