import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
def get_data():
    conn = sqlite3.connect('game_analytics.db')
    df_p = pd.read_sql("SELECT * FROM players", conn)
    df_s = pd.read_sql("SELECT * FROM sessions", conn)
    df_t = pd.read_sql("SELECT * FROM transactions", conn)
    df_ev = pd.read_sql("SELECT * FROM events", conn)
    conn.close()
    return df_p, df_s, df_t, df_ev
players, sessions, transactions, df_ev = get_data()

integrity_check = transactions.merge(players[['player_id', 'signup_date']], on='player_id')
bad_data = integrity_check[integrity_check['tx_at'] < integrity_check['signup_date']]

if not bad_data.empty:
    st.sidebar.warning(f"⚠️ Audit Alert: {len(bad_data)} transactions found with dates before signup. These have been excluded from analysis.")
    transactions = transactions[~transactions.index.isin(bad_data.index)]
st.set_page_config(page_title = "Game Analytics Pro", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #31333F;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("Game Performance Dashboard")
st.markdown("Analyzing Player Engagement and Monetization")
st.sidebar.header("Global Filters")
all_countries = players['country'].unique()
selected_countries = st.sidebar.multiselect("Select Countries", all_countries, default=all_countries)



players = players[players['country'].isin(selected_countries)]
players['signup_date'] = pd.to_datetime(players['signup_date'])
sessions = sessions[sessions['player_id'].isin(players['player_id'])]
transactions = transactions[transactions['player_id'].isin(players['player_id'])]

start_date = players['signup_date'].min().date()
end_date = players['signup_date'].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(start_date, end_date),
    min_value=start_date,
    max_value=end_date
)
if len(date_range) == 2:
    sel_start, sel_end = date_range
    sel_start = pd.to_datetime(sel_start)
    sel_end = pd.to_datetime(sel_end)
    
    players = players[(players['signup_date'] >= sel_start) & (players['signup_date'] <= sel_end)]
    sessions['session_at'] = pd.to_datetime(sessions['session_at'])
    sessions = sessions[(sessions['session_at'] >= sel_start) & (sessions['session_at'] <= sel_end)]
    
    transactions['tx_at'] = pd.to_datetime(transactions['tx_at'])
    transactions = transactions[(transactions['tx_at'] >= sel_start) & (transactions['tx_at'] <= sel_end)]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Players", len(players))
with col2:
    total_rev = transactions['amount'].sum()
    st.metric("Total Revenue", f"${total_rev:,.2f}")
with col3:
    avg_dur = sessions['duration_mins'].mean()
    st.metric("Avg. Session (Mins)", f"{avg_dur:.1f}")


tab1, tab2, tab3 = st.tabs(["Growth & Retention", "Monetization", "Gameplay & Funnels"])

with tab1:
    # Move your DAU and Heatmap code here
    st.subheader("User Retention (Cohort Analysis)")

    df_retention = sessions.merge(players[['player_id', 'signup_date']], on = 'player_id')

    df_retention['signup_date'] = pd.to_datetime(df_retention['signup_date'])
    df_retention['session_at'] = pd.to_datetime(df_retention['session_at'])

    df_retention['days_since_signup'] = (df_retention['session_at'] - df_retention['signup_date']).dt.days
    df_7d = df_retention[df_retention['days_since_signup'] <= 7]
    cohort_data = df_7d.groupby(['signup_date', 'days_since_signup'])['player_id'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index='signup_date', columns='days_since_signup', values='player_id')
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    fig_heat = px.imshow(retention_matrix, 
                        labels=dict(x="Days Since Signup", y="Signup Date", color="Retention %"),
                        aspect="auto",
                        color_continuous_scale='Blues')
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Daily Active Users (DAU)")

    dau_data = sessions.copy()
    dau_data['session_at'] = pd.to_datetime(dau_data['session_at']).dt.date
    dau_chart = dau_data.groupby('session_at')['player_id'].nunique().reset_index()

    fig_line = px.line(dau_chart, x='session_at', y='player_id', 
                    title="Daily Active Users Over Time",
                    markers=True)
    st.plotly_chart(fig_line, use_container_width=True)


with tab2:
    # Move your Revenue charts and Whale table here
    st.subheader("Revenue by Country")
    geo_rev = transactions.merge(players, on = 'player_id')
    geo_rev_grouped = geo_rev.groupby('country')['amount'].sum().reset_index()
    fig = px.bar(geo_rev_grouped, x = 'country', y = 'amount', color = 'amount', title="Where is the money coming from?")
    st.plotly_chart(fig, use_container_width = True)

    st.subheader("Top Spenders (Whales)")

    whale_df = transactions.groupby('player_id')['amount'].sum().reset_index()
    whale_df = whale_df.sort_values(by='amount', ascending=False).head(10)

    whale_details = whale_df.merge(players, on='player_id')

    st.table(whale_details[['player_id', 'country', 'amount']])

    total_revenue = transactions['amount'].sum()
    unique_players = len(players)
    unique_payers = transactions['player_id'].nunique()
    arpu = total_revenue / unique_players if unique_players > 0 else 0
    arppu = total_revenue / unique_payers if unique_payers > 0 else 0
    st.subheader("Efficiency Metrics")
    m_col1, m_col2, m_col3 = st.columns(3)

    m_col1.metric("Conversion Rate", f"{(unique_payers/unique_players)*100:.1f}%")
    m_col2.metric("ARPU", f"${arpu:.2f}")
    m_col3.metric("ARPPU", f"${arppu:.2f}")

with tab3:
    # Move your Funnel and Segment charts here
    st.subheader("Level Progression Funnel")
    funnel_df = df_ev[df_ev['event_name'].str.contains("Complete")]
    funnel_stats = funnel_df.groupby('event_name')['player_id'].nunique().reset_index()
    funnel_stats = funnel_stats.sort_values(by='event_name')
    fig_funnel = px.funnel(funnel_stats, x='player_id', y='event_name',
                        title="Player Drop-off by Level")
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.subheader("User Segments")

    player_stats = sessions.groupby('player_id').agg(
        total_sessions=('player_id', 'count'),
        avg_duration=('duration_mins', 'mean')
    ).reset_index()

    def segment_user(row):
        if row['total_sessions'] > 10:
            return 'Hardcore'
        elif row['total_sessions'] > 3:
            return 'Regular'
        else:
            return 'Casual'

    player_stats['segment'] = player_stats.apply(segment_user, axis=1)

    segment_counts = player_stats['segment'].value_counts().reset_index()
    fig_pie = px.pie(segment_counts, values='count', names='segment', 
                    title="Player Base Distribution",
                    hole=0.4) 
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Revenue by Segment")

    segment_rev = transactions.merge(player_stats[['player_id', 'segment']], on='player_id')
    rev_by_seg = segment_rev.groupby('segment')['amount'].sum().reset_index()

    fig_rev_seg = px.bar(rev_by_seg, x='segment', y='amount', color='segment',
                        title="Total Spend per User Group")
    st.plotly_chart(fig_rev_seg, use_container_width=True)

st.divider()
st.header("Strategic Insights")
top_item = transactions.groupby('item_id')['amount'].sum().idxmax()
total_from_item = transactions.groupby('item_id')['amount'].sum().max()

st.write(f"**Key Finding:** The **{top_item}** is your primary revenue driver, contributing ${total_from_item:,.2f}. Consider bundling this with lower-performing items to boost sales.")
day_1_retention = retention_matrix.iloc[:, 1].mean() * 100
st.write(f"**Retention Note:** Your average Day 1 retention is **{day_1_retention:.1f}%**. If this drops below 30%, investigate the tutorial/onboarding flow.")

import joblib

st.divider()
st.header("Predictive Insights (AI)")

try:
    # 1. Load the trained brain
    trained_model = joblib.load('churn_model.pkl')
    
    # 2. Let's predict for the 'Whales' table we made earlier
    # We need to give the model the same features: sessions_3d and avg_dur_3d
    # (For simplicity, we'll use the stats we already have)
    whale_stats = sessions[sessions['player_id'].isin(whale_details['player_id'])]
    whale_features = whale_stats.groupby('player_id').agg(
        sessions_3d=('player_id', 'count'),
        avg_dur_3d=('duration_mins', 'mean')
    ).reset_index()
    
    # 3. Make the Prediction
    predictions = trained_model.predict(whale_features[['sessions_3d', 'avg_dur_3d']])
    whale_features['Churn_Prediction'] = ["Likely to Stay" if p == 1 else "At Risk" for p in predictions]
    
    st.write("Prediction for your Top Spenders:")
    st.table(whale_features[['player_id', 'Churn_Prediction']])

except:
    st.info("Train the model in train_model.py first to see AI predictions here!")

