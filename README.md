# 🎮 Game Analytics Pro: End-to-End Player Intelligence

A full-stack data engineering and machine learning pipeline designed to track player behavior, analyze monetization health, and predict user churn for a live-service game.

<img src="https://github.com/user-attachments/assets/523066a3-d55b-49df-b0f2-02b7f156b576" width="100%" alt="Dashboard Screenshot">

## 🚀 Overview
This project simulates a professional gaming analytics environment. It transforms raw player event data into actionable business intelligence through a SQL-backed dashboard and a Random Forest predictive model.

## 🧠 Key Features
* **Automated ETL Pipeline:** Generates synthetic player data and manages a relational SQLite database.
* **Behavioral Segmentation:** Groups players into 'Casual', 'Regular', and 'Hardcore' segments based on session frequency.
* **Cohort Analysis:** Visualizes 7-day retention heatmaps to identify "Day 1" drop-off points.
* **Churn Prediction (AI):** A Random Forest model (73% accuracy) that identifies "At-Risk" whales by analyzing early-game session depth.
* **Interactive What-If Simulator:** Allows product managers to simulate how session length increases impact retention.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Data:** Pandas, NumPy, SQLite
* **ML:** Scikit-Learn (Random Forest), Joblib
* **UI:** Streamlit, Plotly Express

## 📈 Key Insights Found
1.  **Retention Driver:** Session duration was found to be 1.7x more important than session frequency for long-term retention.
2.  **Monetization:** 10% of the player base (Whales) accounts for nearly 70% of total revenue.
3.  **Onboarding Friction:** Level 2 showed the highest drop-off rate, suggesting a difficulty spike.

## ⚙️ Setup & Installation
1. Clone the repo: `git clone https://github.com/janhv66/game-analytics-pro.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize and run: `python main.py`
4. Launch Dashboard: `streamlit run dashboard.py`
