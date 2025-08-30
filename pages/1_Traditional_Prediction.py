import streamlit as st
import pandas as pd
import joblib
from src.preprocessing import load_and_preprocess
from src.db_utils import save_prediction
from src.chatbot_utils import analyze_sentiment, detect_churn_intent
from src.visualization import plot_shap_waterfall

# Load models once
@st.cache_resource
def load_models():
    model = joblib.load("models/churn_model.pkl")
    metrics = joblib.load("models/metrics.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")
    return model, metrics, feature_columns

model, metrics, feature_columns = load_models()

def render_page():
    st.markdown('<div class="main-header"><h2>📊 Traditional Churn Prediction</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Customer Information")
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Has Partner?", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No phone service", "No", "Yes"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        )
        tenure = st.slider("Tenure (months)", 0, 72, 24)
        monthly_charges = st.slider("Monthly Charges", 0.0, 150.0, 70.0)
        total_charges = st.slider("Total Charges", 0.0, 10000.0, 2500.0)

        st.subheader("💬 Recent Communication (Optional)")
        recent_communication = st.text_area("Enter recent messages/support tickets:")
        customer_id = st.text_input("Customer ID", value="CUST_001")

    with col2:
        st.subheader("⚡ Risk Insights")
        risk_factors = []
        if contract == "Month-to-month": risk_factors.append("Short-term contract")
        if monthly_charges > 80: risk_factors.append("High monthly charges")
        if tenure < 12: risk_factors.append("New customer")
        if tech_support == "No": risk_factors.append("No tech support")

        if risk_factors:
            st.warning("⚠️ Potential Risk Factors Detected:")
            for f in risk_factors: st.write("•", f)
        else:
            st.success("✅ Low traditional risk profile")

    input_dict = {
        "gender": [gender],
        "SeniorCitizen": [1 if senior == "Yes" else 0],
        "Partner": [partner],
        "Dependents": [dependents],
        "PhoneService": [phone_service],
        "MultipleLines": [multiple_lines],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "OnlineBackup": [online_backup],
        "DeviceProtection": [device_protection],
        "TechSupport": [tech_support],
        "StreamingTV": [streaming_tv],
        "StreamingMovies": [streaming_movies],
        "Contract": [contract],
        "PaperlessBilling": [paperless_billing],
        "PaymentMethod": [payment_method],
        "tenure": [tenure],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
    }

    df_input = pd.DataFrame(input_dict)
    df_encoded = load_and_preprocess(None, custom_df=df_input)
    df_encoded = df_encoded.reindex(columns=feature_columns, fill_value=0)

    if st.button("🔮 Predict Churn Risk", use_container_width=True):
        pred = model.predict(df_encoded)[0]
        proba = model.predict_proba(df_encoded)[0][1]

        # NLP adjustment
        nlp_risk_adj = 0
        if recent_communication.strip():
            sentiment = analyze_sentiment(recent_communication)
            intent = detect_churn_intent(recent_communication)
            if intent == "high_churn_risk": nlp_risk_adj = 0.3
            elif intent == "moderate_churn_risk": nlp_risk_adj = 0.15
            if sentiment < -0.3: nlp_risk_adj += 0.1

        final_proba = min(0.99, proba + nlp_risk_adj)
        save_prediction(input_dict, int(pred), float(final_proba))

        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
        if final_proba > 0.7:
            st.error(f"🚨 HIGH CHURN RISK ({final_proba:.2f})")
        elif final_proba > 0.4:
            st.warning(f"⚠️ MODERATE CHURN RISK ({final_proba:.2f})")
        else:
            st.success(f"✅ LOW CHURN RISK ({final_proba:.2f})")
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("🔍 Feature Contributions (SHAP)")
        plot_shap_waterfall(model, df_encoded, st)

render_page()
