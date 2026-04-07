# test for llm_adapter
import pytest
import sqlite3
from unittest.mock import MagicMock, patch # to hide secret api keys
from modules.llm_adapter import translate_to_sql, build_prompt

@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    conn.commit()
    return conn

@patch("modules.llm_adapter.client")
def test_translation_string(mock_client, in_memory_db):
    mock_client.messages.create.return_value = MagicMock(content=[MagicMock(text="SELECT * FROM users")])
    res = translate_to_sql(in_memory_db, "show all users")
    assert res == "SELECT * FROM users"

def test_build_prompt(in_memory_db):
    prompt = build_prompt(in_memory_db, "show all users")
    assert "show all users" in prompt
    assert "age" in prompt
