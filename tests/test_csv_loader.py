# test for csv_loader

import pytest
import pandas as pd
import sqlite3
from modules.csv_loader import load_csv, insert_data

# some sample data
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [30, 25],
        "city": ["Boston", "New York"]
    })

# test db to insert into
@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, city TEXT)")
    conn.commit()
    return conn

# load the csv and check size
def test_load_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")
    df = load_csv(str(csv_file))
    assert len(df) == 2
    assert "name" in df.columns

# insert the data into the test db and check size
def test_insert_data(in_memory_db, sample_df):
    insert_data(in_memory_db, "people", sample_df)
    cursor = in_memory_db.cursor()
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()
    assert len(rows) == 2
