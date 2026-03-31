# llm_adapter.py

# lets use claude (anthropic)

import os
from anthropic import Anthropic
from dotenv import load_dotenv
from schema_manager import get_all_tables, get_table_schema

load_dotenv()

client = Anthropic()

def build_prompt(conn, user_query: str) -> str:
    tables = get_all_tables(conn)
    schema_lines = []
    for table in tables:
        schema = get_table_schema(conn, table)
        cols = ", ".join([f"{col} ({dtype})" for col, dtype in schema.items()])
        schema_lines.append(f"- {table} ({cols})")
    schema_str = "\n".join(schema_lines)

    return f"""You are an assistant that converts natural language to SQLite SQL queries.
The user's database has the following tables:
{schema_str}

User query: "{user_query}"

Respond with ONLY the SQL query; no explanation, no markdown, no backticks."""

def translate_to_sql(conn, user_query: str) -> str:
    prompt = build_prompt(conn, user_query)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()
