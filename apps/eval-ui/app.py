import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Judge Dashboard", layout="wide")
st.title("⚖️ AI Evaluation Leaderboard (2026 Edition)")

def load_data():
    results = []
    # Path to the data we've been saving
    paths = ["data/results/local_run.jsonl", "data/results/prod_run.jsonl"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    results.append(json.loads(line))
    return pd.DataFrame(results)

# --- LOAD & PROCESS ---
df = load_data()

if df.empty:
    st.warning("No evaluation data found. Run some tests in Swagger first!")
else:
    # 1. KPI Top Row
    col1, col2, col3 = st.columns(3)
    avg_score = df['primary_score'].mean()
    total_cost = df['metadata'].apply(lambda x: x.get('eval_cost', 0)).sum()
    
    col1.metric("Avg Faithfulness", f"{avg_score:.2f}")
    col2.metric("Total 'Burn' (USD)", f"${total_cost:.4f}")
    col3.metric("Total Evals", len(df))

    # 2. The Battle Chart: Local vs Cloud
    st.subheader("Model Performance Comparison")
    # Extract engine name from metadata for the chart
    df['engine'] = df['metadata'].apply(lambda x: x.get('engine', 'unknown'))
    
    fig = px.box(df, x="engine", y="primary_score", color="engine",
                 points="all", hover_data=["reason"],
                 title="Faithfulness Distribution by Model")
    st.plotly_chart(fig, use_container_width=True)

    # 3. Raw Data Audit Log
    st.subheader("Detailed Audit Log")
    st.dataframe(df[['call_id', 'engine', 'primary_score', 'reason']], use_container_width=True)