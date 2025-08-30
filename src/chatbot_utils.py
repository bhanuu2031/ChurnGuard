from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def detect_churn_intent(text):
    churn_keywords = [
        'cancel','unsubscribe','terminate','quit',
        'dissatisfied','unhappy','frustrated','disappointed',
        'competitor','switch','looking elsewhere','poor service','bad experience'
    ]
    text_lower = text.lower()
    score = sum(1 for kw in churn_keywords if kw in text_lower)
    if score >= 3:
        return "high_churn_risk"
    elif score >= 1:
        return "moderate_churn_risk"
    return "low_churn_risk"

def generate_ai_response(user_message, churn_probability=None):
    text = user_message.lower()

    # --- FAQ-style responses ---
    if "customer churn" in text or "what is churn" in text:
        return """📉 Customer churn means when customers stop using a company's product 
or service. It’s an important metric because high churn means the business is losing customers. 
Reducing churn helps improve revenue and customer loyalty."""
    
    if "how to reduce churn" in text or "prevent churn" in text:
        return """✅ To reduce churn, companies often:
- Provide excellent customer support
- Offer loyalty programs
- Collect and act on customer feedback
- Improve onboarding and user experience
- Provide discounts to at-risk customers"""

    if "hello" in text or "hi" in text or "hey" in text:
        return "👋 Hi there! How can I help you today?"

    # --- Risk / Sentiment based responses ---
    intent = detect_churn_intent(user_message)
    sentiment = analyze_sentiment(user_message)

    if intent == "high_churn_risk":
        return """🚨 It seems you’re unhappy. Let me connect you with a specialist 
to resolve this ASAP. We also have some exclusive offers for you."""
    elif sentiment < -0.3:
        return "😟 I sense frustration. Can you tell me the main issue so I can help fix it?"
    else:
        return "😊 Thanks for reaching out! How can I assist you today?"
