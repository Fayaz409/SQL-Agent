import sqlite3
import pandas as pd

def list_tables() -> list:
    """
    List the tables available in the SQLite database.
    """
    conn = sqlite3.connect("customers.db")
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    conn.close()
    return tables["name"].tolist()

def get_table(table_name: str) -> dict:
    """
    Get the schema and the number of rows in the given table.
    """
    conn = sqlite3.connect("customers.db")
    # Get schema information using PRAGMA
    schema_query = f"PRAGMA table_info({table_name});"
    schema_df = pd.read_sql(schema_query, conn)
    
    # Get row count
    count_query = f"SELECT COUNT(*) as row_count FROM {table_name};"
    count_df = pd.read_sql(count_query, conn)
    row_count = count_df["row_count"].iloc[0]
    conn.close()
    return {
        "schema": schema_df.to_dict(orient="records"),
        "row_count": row_count,
    }

def sql_query(query: str) -> list:
    """
    Run a SQL query against the SQLite database and return the results.
    """
    conn = sqlite3.connect("customers.db")
    try:
        df = pd.read_sql(query, conn)
        result = df.to_dict(orient="records")
    except Exception as e:
        result = f"Error: {str(e)}"
    finally:
        conn.close()
    return result
