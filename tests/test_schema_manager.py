# test for schema_manager

import pytest
import pandas as pd
import sqlite3
from modules.csv_loader import load_csv, insert_data
from modules.schema_manager import infer_schema, create_table, get_all_tables, schemas_match

# some sample data
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [30, 25],
        "salary": [80000.0, 60000.0] # float
    })

@pytest.fixture
def in_memory_db():
    return sqlite3.connect(":memory:")

# infer types
def test_infer_schema(sample_df):
    schema = infer_schema(sample_df)
    assert schema["name"] == "TEXT"
    assert schema["age"] == "INTEGER"
    assert schema["salary"] == "REAL"

# create table
def test_create_table(in_memory_db, sample_df):
    create_table(in_memory_db, "people", sample_df)
    cursor = in_memory_db.cursor()
    cursor.execute("PRAGMA table_info(people)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert "id" in columns
    assert "name" in columns
    assert "age" in columns

# create and get tables
def test_get_all_tables(in_memory_db):
    in_memory_db.execute("CREATE TABLE foo (id INTEGER)")
    in_memory_db.execute("CREATE TABLE bar (id INTEGER)")
    tables = get_all_tables(in_memory_db)
    assert "foo" in tables
    assert "bar" in tables

# schema match
def test_schemas_match(in_memory_db, sample_df):
    create_table(in_memory_db, "people", sample_df)
    assert schemas_match(in_memory_db, "people", sample_df) == True

    mismatched_df = pd.DataFrame({"completely_different": ["x"]})
    assert schemas_match(in_memory_db, "people", mismatched_df) == False

