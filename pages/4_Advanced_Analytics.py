import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

def render_page():
    st.markdown('<div class="main-header"><h2>📈 Advanced Churn Analytics</h2></div>', unsafe_allow_html=True)

    # Connect to DB
    conn = sqlite3.connect("database/churn_predictions.db")

    # --- Metrics ---
    try:
        df_pred = pd.read_sql_query("SELECT * FROM predictions", conn)
        df_comm = pd.read_sql_query("SELECT * FROM customer_communications", conn)

        # Calculate churn rate
        if not df_pred.empty:
            churn_rate = (df_pred["prediction"].sum() / len(df_pred)) * 100
            at_risk_customers = (df_pred["probability"] > 0.7).sum()
        else:
            churn_rate = 0
            at_risk_customers = 0

        # Avg sentiment
        if not df_comm.empty:
            avg_sentiment = df_comm["sentiment_score"].mean()
        else:
            avg_sentiment = 0.0

    except Exception as e:
        st.error(f"DB Error: {e}")
        churn_rate, avg_sentiment, at_risk_customers = 0, 0, 0
    finally:
        conn.close()

    # --- Show Metrics ---
    st.subheader("🎯 Key Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("📉 Churn Rate", f"{churn_rate:.1f}%", "vs last update")
    c2.metric("😊 Avg. Sentiment", f"{avg_sentiment:.2f}", "")
    c3.metric("⚠️ At-Risk Customers", f"{at_risk_customers}", "")

    # --- Churn Rate Trend ---
    st.subheader("📊 Churn Rate Trend")
    if not df_pred.empty:
        df_pred["timestamp"] = pd.to_datetime(df_pred["timestamp"])
        df_pred["week"] = df_pred["timestamp"].dt.to_period("W").apply(lambda r: r.start_time)
        churn_trend = df_pred.groupby("week")["prediction"].mean().reset_index()
        churn_trend.rename(columns={"prediction":"churn_rate"}, inplace=True)

        fig = px.line(churn_trend, x="week", y="churn_rate", title="Churn Rate Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No churn prediction history yet.")

    # --- Sentiment Trend ---
    st.subheader("💬 Sentiment Trend")
    if not df_comm.empty:
        df_comm["timestamp"] = pd.to_datetime(df_comm["timestamp"])
        sentiment_trend = df_comm.groupby(df_comm["timestamp"].dt.to_period("W"))["sentiment_score"].mean().reset_index()
        sentiment_trend["week"] = sentiment_trend["timestamp"].apply(lambda r: r.start_time)

        fig2 = px.line(sentiment_trend, x="week", y="sentiment_score", title="Avg Sentiment Over Time")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No communication sentiment data yet.")

    # --- AI Insights ---
    st.subheader("🤖 AI Insights")
    if churn_rate > 30:
        st.error("🚨 High churn detected! Immediate retention strategies needed.")
    elif churn_rate > 15:
        st.warning("⚠ Moderate churn rate. Consider proactive engagement.")
    else:
        st.success("✅ Low churn rate. Focus on customer loyalty & upselling.")

    if avg_sentiment < -0.2:
        st.error("😠 Customer sentiment is very negative! Service issues likely.")
    elif avg_sentiment < 0.1:
        st.warning("😐 Customer sentiment is neutral. Room for improvement.")
    else:
        st.success("😊 Customer sentiment is positive overall.")

render_page()
