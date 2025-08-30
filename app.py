import streamlit as st
from src.db_utils import init_enhanced_db, show_history_sidebar

# Initialize DB
init_enhanced_db()

# Page Config
st.set_page_config(page_title="ChurnGuard – AI-Powered Customer Retention System", page_icon="🤖", layout="wide")

# Custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== Hero Section =====
st.markdown("""
<div style="background: linear-gradient(90deg, #667eea, #764ba2); padding: 2rem; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <h1 style="font-size: 2.5rem;">🤖ChurnGuard – AI-Powered Customer Retention System</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Developed churn analytics platform combining ML, NLP sentiment detection, and AI chatbot interventions.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Welcome to ChurnGuard- A smart churn prediction system")

# ===== Feature Cards =====
st.markdown("#### 🌟 Key Features")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background:#1e1e2f; padding:1.2rem; border-radius:12px; margin-bottom:1rem; border-left: 5px solid #4CAF50;">
        <h4>📊 Predict Customer Churn</h4>
        <p>Use ML models to predict churn risk with advanced features and SHAP explainability.</p>
    </div>
    <div style="background:#1e1e2f; padding:1.2rem; border-radius:12px; border-left: 5px solid #ff9800;">
        <h4>💬 Analyze Communications</h4>
        <p>Perform sentiment + churn intent analysis on emails, tickets, and chats.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#1e1e2f; padding:1.2rem; border-radius:12px; margin-bottom:1rem; border-left: 5px solid #2196F3;">
        <h4>🤖 AI Chatbot</h4>
        <p>Engage customers with proactive chatbot interventions and reduce churn risk.</p>
    </div>
    <div style="background:#1e1e2f; padding:1.2rem; border-radius:12px; border-left: 5px solid #9c27b0;">
        <h4>📈 Advanced Analytics</h4>
        <p>Track churn trends, sentiment shifts, and customer risk distribution in real time.</p>
    </div>
    """, unsafe_allow_html=True)

# ===== CTA Section =====
st.markdown("""
---
<div style="text-align:center; margin-top:2rem;">
    <h3>👉 Use the <b>sidebar</b> to start exploring features!</h3>
    <p style="color: #bbb;">Made with ❤️ using Streamlit, ML & NLP</p>
    <p style="color: #bbb;">Built by : Bhanu Srivastava, bhannuu2031@gmail.com </p>
</div>
""", unsafe_allow_html=True)

# Sidebar recent activity
show_history_sidebar(st)
