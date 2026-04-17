import sqlite3
import pandas as pd
conn = sqlite3.connect('game_analytics.db')
query = """
SELECT
    p.country,
    SUM(t.amount) as total_revenue
FROM players p
JOIN transactions t ON p.player_id = t.player_id
GROUP BY p.country
ORDER BY total_revenue DESC;
"""
df_result = pd.read_sql_query(query, conn)
print(df_result)
conn.close()