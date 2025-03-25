import sqlite3
import pandas as pd

def get_data():
    DB_NAME = 'data.db'
    QUERY = 'SELECT * FROM industrias'
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(QUERY,conn)
    return df
