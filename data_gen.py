import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
NUM_PLAYERS = 1000
COUNTRIES = ['USA', 'India', 'Brazil', 'Germany', 'UK', 'Canada']
START_DATE = datetime.now() - timedelta(days = 30)
player_data = []
for i in range(NUM_PLAYERS):
    p_id = f"P{i:03d}"
    days_to_add = random.randint(0, 30)
    signup_date = START_DATE + timedelta(days = days_to_add)
    country = random.choice(COUNTRIES)
    player_data.append([p_id, signup_date, country])
df_players = pd.DataFrame(player_data, columns = ['player_id', 'signup_date', 'country'])
df_players.to_csv('players.csv', index = False)

session_data = []
for index, row in df_players.iterrows():
    p_id = row['player_id']
    signup_date = row['signup_date']
    num_sessions = random.randint(1, 15)
    for _ in range(num_sessions):
        days_since_signup = (datetime.now() - signup_date).days
        if days_since_signup > 0:
            random_day = random.randint(0, days_since_signup)
            session_start = signup_date + timedelta(days = random_day)
            duration = random.randint(5, 60)
            session_data.append([p_id, session_start, duration])
df_sessions = pd.DataFrame(session_data, columns = ['player_id', 'session_at', 'duration_mins'])
df_sessions.to_csv('sessions.csv', index = False)
transaction_data = []
items = {
    'Skins' : 9.99,
    'Battle Pass' : 14.99,
    'Extra Lives' : 0.99,
    'Gems Pack' : 4.99
}
spenders = df_players.sample(frac = 0.05)['player_id'].tolist()
for p_id in spenders:
    signup_date = df_players[df_players['player_id'] == p_id]['signup_date'].iloc[0]
    for _ in range(random.randint(1, 3)):
        item_name = random.choice(list(items.keys()))
        price = items[item_name]
        days_since_signup = (datetime.now() - signup_date).days
        if days_since_signup > 0:
            tx_date = signup_date + timedelta(days = random.randint(0, days_since_signup))
            transaction_data.append([p_id, tx_date, item_name, price])
df_transactions = pd.DataFrame(transaction_data, columns = ['player_id', 'tx_at', 'item_id', 'amount'])
df_transactions.to_csv('transactions.csv', index = False)
event_data = []
for p_id in df_players['player_id']:
    current_level = 1
    max_levels = 5
    while current_level <= max_levels:
        if random.random() < 0.80:
            event_data.append([p_id, f"Level {current_level} Complete"])
            current_level += 1
        else:
            event_data.append([p_id, f"Dropped at Level {current_level}"])
            break
df_events = pd.DataFrame(event_data, columns=['player_id', 'event_name'])
df_events.to_csv('events.csv', index=False)