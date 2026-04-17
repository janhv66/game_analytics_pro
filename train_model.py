import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- STEP 1: PREPARE THE DATA (The missing piece) ---
conn = sqlite3.connect('game_analytics.db')
df_p = pd.read_sql("SELECT player_id, signup_date FROM players", conn)
df_s = pd.read_sql("SELECT * FROM sessions", conn)
conn.close()

df_p['signup_date'] = pd.to_datetime(df_p['signup_date'])
df_s['session_at'] = pd.to_datetime(df_s['session_at'])

# Create Features (Behavior in first 3 days)
df_joined = df_s.merge(df_p, on='player_id')
df_joined['days_since_signup'] = (df_joined['session_at'] - df_joined['signup_date']).dt.days

# Feature calculation
first_3_days = df_joined[df_joined['days_since_signup'] <= 3]
features = first_3_days.groupby('player_id').agg(
    sessions_3d=('session_at', 'count'),
    avg_dur_3d=('duration_mins', 'mean')
).reset_index()

# Create Label (Did they play on Day 7 or later?)
retained_ids = df_joined[df_joined['days_since_signup'] >= 7]['player_id'].unique()
features['retention_label'] = features['player_id'].isin(retained_ids).astype(int)

# --- STEP 2: TRAIN THE MODEL ---
# X = The Evidence, y = The Result
X = features[['sessions_3d', 'avg_dur_3d']]
y = features['retention_label']

# Split 80% for learning, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the "Brain"
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, y_pred))

# --- STEP 3: SAVE ---
joblib.dump(model, 'churn_model.pkl')
print("Model saved as churn_model.pkl")

# Check which feature was more important
importances = model.feature_importances_
for i, feat in enumerate(X.columns):
    print(f"Feature: {feat}, Importance: {importances[i]:.2f}")