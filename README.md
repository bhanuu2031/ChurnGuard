# 🤖 ChurnGuard – AI-Powered Customer Retention System

ChurnGuard is an **AI-driven customer churn prediction and intervention system** that combines **Machine Learning, NLP, and Chatbots** to help businesses identify at-risk customers, analyze communications, and proactively engage to reduce churn.

---

## ✨ Features

- 📊 **Customer Churn Prediction**
  - ML model (84% accuracy, ROC-AUC 0.91) to predict churn risk  
  - SHAP explainability for feature importance  

- 💬 **Communication Analysis**
  - Sentiment analysis using **TextBlob**  
  - Intent detection for churn-related language  
  - Communication history stored in SQLite database  

- 🤖 **AI Chatbot Intervention**
  - Real-time chatbot with streaming responses  
  - Rule-based + sentiment-aware interactions  
  - Stores chat history & insights in database  

- 📈 **Advanced Analytics Dashboard**
  - Churn rate trends over time  
  - Sentiment shifts visualization  
  - At-risk customers tracking with metrics  

---

## 🖥️ Tech Stack

- **Frontend/Dashboard**: [Streamlit](https://streamlit.io/)  
- **Machine Learning**: scikit-learn, joblib, SHAP  
- **NLP**: TextBlob (sentiment & intent analysis)  
- **Database**: SQLite (prediction history, communication logs, chatbot interactions)  
- **Visualization**: Matplotlib, Plotly  

---

## 📂 Project Structure
churn-prediction-app/
│

├── app.py # Home page (Streamlit landing page)

├── requirements.txt # Python dependencies

│
├── pages/ # Multi-page Streamlit app
│ ├── 1_Traditional_Prediction.py
│ ├── 2_Customer_Communication_Analysis.py
│ ├── 3_AI_Chatbot_Intervention.py
│ └── 4_Advanced_Analytics.py
│
├── src/ # Core utilities
│ ├── preprocessing.py
│ ├── db_utils.py
│ ├── chatbot_utils.py
│ ├── visualization.py
│ └── config.py
│
├── models/ # Trained ML models
│ ├── churn_model.pkl
│ ├── metrics.pkl
│ └── feature_columns.pkl
│
├── database/ # SQLite database
│ └── churn_predictions.db
│
└── assets/ # UI assets
├── styles.css
└── logo.png


---

## ⚙️ Installation & Setup
1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/churnguard.git
   cd churnguard
Create a virtual environment & install dependencies
pip install -r requirements.txt

Run the app
streamlit run app.py

Open in your browser: http://localhost:8501

