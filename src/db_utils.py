import sqlite3
from src.config import DB_NAME
import pandas as pd

def init_db():
    """Create base predictions table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT,
            prediction INTEGER,
            probability REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def init_enhanced_db():
    """Create enhanced tables for communications and chatbot logs."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_communications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            communication_text TEXT,
            sentiment_score REAL,
            communication_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            intent TEXT,
            sentiment_score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_prediction(input_dict, prediction, probability):
    """Save prediction results."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (input_data, prediction, probability)
        VALUES (?, ?, ?)
    ''', (str(input_dict), prediction, probability))
    conn.commit()
    conn.close()

def show_history_sidebar(st):
    """Show history in sidebar."""
    st.sidebar.header("📊 Recent Activity")
    conn = sqlite3.connect(DB_NAME)

    if st.sidebar.button("Show Prediction History"):
        df_history = pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 5", conn)
        st.sidebar.dataframe(df_history)

    if st.sidebar.button("Show Communication Analysis"):
        try:
            df_comm = pd.read_sql_query("""
                SELECT customer_id, sentiment_score, communication_type, timestamp 
                FROM customer_communications ORDER BY timestamp DESC LIMIT 5
            """, conn)
            st.sidebar.dataframe(df_comm)
        except:
            st.sidebar.info("No communication data available yet.")
    conn.close()
