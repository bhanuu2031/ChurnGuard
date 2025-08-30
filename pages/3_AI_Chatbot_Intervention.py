import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from src.chatbot_utils import generate_ai_response, detect_churn_intent, analyze_sentiment
import time

def render_page():
    st.markdown('<div class="main-header"><h2>🤖 AI Chatbot Intervention</h2></div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display history
    for chat in st.session_state.chat_history:
        if chat['sender'] == 'user':
            st.markdown(f"<div class='chat-bubble-user'>{chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-ai'>{chat['message']}</div>", unsafe_allow_html=True)

    # Input
    user_msg = st.text_input("💬 Type your message here:", key="chat_input")

    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("Send", use_container_width=True):
            if user_msg:
                # Add user message to history
                st.session_state.chat_history.append({"sender":"user","message":user_msg})

                # Placeholder for AI streaming reply
                ai_placeholder = st.empty()
                ai_text = ""

                # Generate AI response (simulate streaming word by word)
                full_response = generate_ai_response(user_msg)  # your existing rule-based response
                for word in full_response.split():
                    ai_text += word + " "
                    ai_placeholder.markdown(f"<div class='chat-bubble-ai'>{ai_text}</div>", unsafe_allow_html=True)
                    time.sleep(0.05)  # simulate streaming delay

                # Save final AI reply
                st.session_state.chat_history.append({"sender":"ai","message":full_response})

                # Save to DB
                conn = sqlite3.connect("database/churn_predictions.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO chatbot_interactions 
                    (customer_id, user_message, bot_response, intent, sentiment_score)
                    VALUES (?, ?, ?, ?, ?)
                """, ("DEMO_CUST", user_msg, full_response,
                      detect_churn_intent(user_msg),
                      analyze_sentiment(user_msg)))
                conn.commit(); conn.close()

                st.rerun()

    with c2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Analytics
    st.subheader("📊 Chat Analytics")
    conn = sqlite3.connect("database/churn_predictions.db")
    try:
        df = pd.read_sql_query("SELECT intent, COUNT(*) as count FROM chatbot_interactions GROUP BY intent", conn)
        if not df.empty:
            fig = px.pie(df, values="count", names="intent", title="Intent Distribution")
            st.plotly_chart(fig)
    except: pass
    finally: conn.close()

render_page()
