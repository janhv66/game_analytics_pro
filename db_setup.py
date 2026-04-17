import sqlite3
import pandas as pd
conn = sqlite3.connect('game_analytics.db')
def load_csv_to_sql(file_name, table_name):
    df = pd.read_csv(file_name)
    df.to_sql(table_name, conn, if_exists = 'replace', index = False)
    print(f"Table '{table_name}' created successfully!")
load_csv_to_sql('players.csv', 'players')
load_csv_to_sql('sessions.csv', 'sessions')
load_csv_to_sql('transactions.csv', 'transactions')
load_csv_to_sql('events.csv', 'events')
conn.close()