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