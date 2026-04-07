# tests for sql_validator

import pytest
import sqlite3
from modules.sql_validator import validate_query

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.commit()
    return conn

# select
def test_valid_select(in_memory_db):
    success, msg = validate_query(in_memory_db, "SELECT * FROM users")
    assert success == True

# other
def test_not_select(in_memory_db):
    success, msg = validate_query(in_memory_db, "DROP TABLE users")
    assert success == False

# nonexistent table
def test_unknown_table(in_memory_db):
    success, msg = validate_query(in_memory_db, "SELECT * FROM rats")
    assert success == False
