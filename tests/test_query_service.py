# tests for query_service

import pytest
import sqlite3
from modules.query_service import execute_query

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
    conn.commit()
    return conn

# valid query results
def test_valid_query_results(in_memory_db):
    success, msg, res = execute_query(in_memory_db, "SELECT * FROM users")
    assert success == True
    assert len(res) == 1

# invalid query
def test_invalid_query(in_memory_db):
    success, msg, res = execute_query(in_memory_db, "DROP TABLE users")
    assert success == False
    assert results == []

# invalid table
def test_unknown_table(in_memory_db):
    success, msg, res = execute_query(in_memory_db, "SELECT * FROM rats")
    assert success == False
