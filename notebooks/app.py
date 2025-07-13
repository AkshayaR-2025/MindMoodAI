import streamlit as st
import joblib
import numpy as np
import random
import matplotlib.pyplot as plt

# Load vectorizer and models
tfidf_vectorizer = joblib.load('vectorizer.pkl')
models = {
    "Random Forest 🌲": joblib.load("best_model.pkl")
    # Add others if you saved more models!
}

# Emojis for emotions
emotion_emojis = {
    "joy": "😊",
    "sadness": "😢",
    "anger": "😠",
    "fear": "😨"
}

# Emotion descriptions
emotion_desc = {
    "joy": "Feeling happy, grateful, or content 🌞",
    "sadness": "Feeling down or emotionally low 💧",
    "anger": "Feeling frustrated or upset 🔥",
    "fear": "Feeling anxious or nervous 😰"
}

# Random quotes
quotes = [
    "Your emotions are valid 💖",
    "You are growing, keep going 🌱",
    "It's okay to feel. You're human 🫶🏻",
    "Healing starts with understanding 🌿"
]

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #ffe6e6, #fff0f5, #f0f8ff);
    }

    .main {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 style='text-align: center; color: #800080;'>🧠 MindMood AI – Journal Emotion Classifier</h1>", unsafe_allow_html=True)
st.markdown("<center>✨ Journal your feelings. Let AI read your mind ✨</center><br>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 💫 Choose Your Model")
selected_model = st.sidebar.selectbox("Select a model:", list(models.keys()))
st.sidebar.markdown("### 🌼 Motivation of the Moment")
st.sidebar.info(random.choice(quotes))

# Journal input
journal_text = st.text_area("📓 Enter your journal entry here:")

if st.button("🔍 Analyze My Mood"):
    if journal_text.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        vector_input = tfidf_vectorizer.transform([journal_text])
        model = models[selected_model]

        # Prediction
        prediction = model.predict(vector_input)[0]
        emoji = emotion_emojis.get(prediction, "")
        desc = emotion_desc.get(prediction, "No description available.")

        # Display result
        st.markdown(f"""
            <div style='
                background-color:#fff0f5;
                padding:20px;
                border-radius:15px;
                font-size:22px;
                text-align:center;
                color:#800080;
                box-shadow:2px 2px 10px #ddd'>
                🎯 <b>Predicted Emotion:</b> <i>{prediction.capitalize()}</i> {emoji}
            </div>
            <br>
        """, unsafe_allow_html=True)

        st.markdown(f"📝 *Description*: {desc}")

        # Pie chart
        try:
            probs = model.predict_proba(vector_input)[0]
            labels = model.classes_

            colors = ['#ffd6d6', '#e0bbf6', '#fff7b3', '#b3e0ff']
            fig, ax = plt.subplots()
            ax.pie(probs, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
            st.pyplot(fig)
        except:
            st.info("ℹ️ Pie chart not available for this model.")

# Footer
st.markdown("<hr><center>🧠 Built with 💖 by Akshaya</center>", unsafe_allow_html=True)