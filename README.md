# sql-llm-interface
Project for EC530, introduction to software principles.
Link to video: ![Google Drive Link](https://drive.google.com/file/d/1YuVhNndVXp2somHVij_BTUFd07Ys11rV/view?usp=sharing)

## System Overview
This project contains a modular system built in Python for querying databases with natural language. Users can load input data from a CSV file and either input SQL queries or ask questions in natural language, which an LLM will translate into SQL. Queries are automatically validated before execution

## Setup: Running from CLI
After acquiring the project files, run the following three commands:
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python3 modules/cli.py
```
Users can enter "load" to load input csv data, "tables" to list existing tables, "query" to input an SQL query, or "ask" to input natural language questions.

## Running Tests
To run all tests using pytest, run the following command:
```bash
pytest tests/
```
Tests are automatically run through GitHub actions on every push.

## Design Notes
The CLI does not have direct database access. Additionally, LLM output is validated before any query is executed. No real API key or database is needed to run tests, as they mock the LLM and data. Schema matching compares incoming data to decide between appending or creating.

## Code Flow Diagram
![Diagram showing the flow of code logic.](llm-sql-adapter-flow.png)

#### Elena Berrios eberrios@bu.edu
