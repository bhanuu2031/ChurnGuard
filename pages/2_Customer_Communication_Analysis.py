import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from src.chatbot_utils import analyze_sentiment, detect_churn_intent

def render_page():
    st.markdown('<div class="main-header"><h2>💬 Customer Communication Analysis</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Analyze Single Message")
        customer_id = st.text_input("Customer ID", value="CUST_001")
        text = st.text_area("Enter customer message:")

        if st.button("Analyze", use_container_width=True):
            if text.strip():
                sentiment = analyze_sentiment(text)
                intent = detect_churn_intent(text)

                # Save into DB
                conn = sqlite3.connect("database/churn_predictions.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO customer_communications
                    (customer_id, communication_text, sentiment_score, communication_type)
                    VALUES (?, ?, ?, ?)
                """, (customer_id, text, sentiment, "manual_entry"))
                conn.commit(); conn.close()

                # Show results
                st.metric("Sentiment Score", round(sentiment, 2))
                st.metric("Churn Intent", intent.replace("_"," ").title())

    with col2:
        st.subheader("📊 Communication History")
        conn = sqlite3.connect("database/churn_predictions.db")
        try:
            df = pd.read_sql_query("SELECT * FROM customer_communications ORDER BY timestamp DESC LIMIT 10", conn)
            if not df.empty:
                st.dataframe(df[['customer_id','communication_text','sentiment_score','communication_type','timestamp']])

                # Sentiment trend
                fig = px.line(df, x="timestamp", y="sentiment_score", color="customer_id",
                              title="Sentiment Trend Over Time")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No communication data yet.")
        except Exception as e:
            st.error(f"DB error: {e}")
        finally:
            conn.close()

render_page()
