import pandas as pd
import sqlite3

conn = sqlite3.connect('game_analytics.db')
df_p = pd.read_sql("SELECT player_id, signup_date FROM players", conn)
df_s = pd.read_sql("SELECT * FROM sessions", conn)
conn.close()
df_p['signup_date'] = pd.to_datetime(df_p['signup_date'])
df_s['session_at'] = pd.to_datetime(df_s['session_at'])

df_joined = df_s.merge(df_p, on='player_id')
df_joined['days_since_signup'] = (df_joined['session_at'] - df_joined['signup_date']).dt.days

first_3_days = df_joined[df_joined['days_since_signup'] <= 3]
features = first_3_days.groupby('player_id').agg(
    sessions_3d=('session_at', 'count'),
    avg_dur_3d=('duration_mins', 'mean')
).reset_index()

retained_ids = df_joined[df_joined['days_since_signup'] >= 7]['player_id'].unique()
features['retention_label'] = features['player_id'].isin(retained_ids).astype(int)

print(features.head())