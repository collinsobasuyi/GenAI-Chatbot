import streamlit as st
from openai import OpenAI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize OpenAI client with a hardcoded API key
# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

# Initialize OpenAI client with the shared secret API key
client = OpenAI(
    api_key=open_api_key
)

# client = OpenAI(
#     api_key=""
# )

# Initialize or load journal data
if "journal_data" not in st.session_state:
    st.session_state.journal_data = []

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# App title
st.title("Mental Health Journal App 🌸")
st.subheader("Write, Reflect, and Grow")

# Journal Entry
st.write("### Today's Journal")
entry = st.text_area("How are you feeling today?", height=150)

# Submit Entry
if st.button("Submit"):
    if entry:
        # Analyze mood sentiment using VADER
        scores = analyzer.polarity_scores(entry)
        compound = scores["compound"]  # Compound score for overall sentiment
        if compound > 0.2:  # Adjust thresholds as needed
            mood = "Positive"
        elif compound < -0.2:
            mood = "Negative"
        else:
            mood = "Neutral"

        # Debug: Print VADER sentiment scores
        print(f"VADER Scores for '{entry}': {scores}, Classified Mood: {mood}")

        # Generate AI encouragement
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a compassionate and highly skilled mental health practitioner with a PhD in psychology and mental health. You have decades of experience providing therapy, emotional support, and practical guidance to individuals facing a wide range of emotional challenges. Your responses should reflect deep empathy, evidence-based practices, and a nurturing tone. You are here to help users gain insight, build resilience, and foster a sense of hope and personal growth."},
                    {"role": "user", "content": f"Provide a motivational response to someone feeling {mood}. Their journal entry: {entry}"}
                ],
                max_tokens=400,  # Reduced token limit
                temperature=0.7  # Optimal temperature for balanced creativity
            )
            encouragement = response.choices[0].message.content.strip()

            # Save entry
            st.session_state.journal_data.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "entry": entry,
                "mood": mood,
                "sentiment": compound,
                "encouragement": encouragement
            })

            st.success("Journal entry saved!")
        except Exception as e:
            st.error(f"Error generating AI response: {e}")
    else:
        st.warning("Please write something before submitting.")

# Display Past Entries
st.write("### Past Entries")
if st.session_state.journal_data:
    for journal in st.session_state.journal_data[::-1]:
        st.markdown(f"**{journal['date']}**")
        st.markdown(f"*Journal Entry:* {journal['entry']}")
        st.markdown(f"*Mood:* {journal['mood']}")
        st.markdown(f"*Encouragement:* {journal['encouragement']}")
        st.write("---")

# Mood Trends
st.write("### Mood Trends")
if st.session_state.journal_data:
    df = pd.DataFrame(st.session_state.journal_data)
    df['date'] = pd.to_datetime(df['date'])
    mood_avg = df.groupby('date')['sentiment'].mean()

    # Plot mood trends
    plt.figure(figsize=(10, 5))
    plt.plot(mood_avg.index, mood_avg.values, marker='o')
    plt.title("Mood Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment (Compound Score)")
    plt.grid()
    st.pyplot(plt)
