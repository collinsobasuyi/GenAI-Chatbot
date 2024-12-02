import streamlit as st
from openai import OpenAI

# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=open_api_key)

# Initialize or load chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize selected practitioner
if "selected_practitioner" not in st.session_state:
    st.session_state.selected_practitioner = None

# Define practitioners
practitioners = {
    "Dr. Smith": {
        "name": "Dr. Sarah Smith",
        "specialty": "Clinical Psychologist",
        "style": "You are calm, empathetic, and focus on practical advice for managing stress and anxiety."
    },
    "Dr. Lee": {
        "name": "Dr. James Lee",
        "specialty": "Psychiatrist",
        "style": "You are warm and supportive, offering insights into the connection between emotions and mental health."
    },
    "Dr. Patel": {
        "name": "Dr. Anika Patel",
        "specialty": "Cognitive Behavioral Therapist",
        "style": "You are analytical and goal-oriented, focusing on strategies to overcome negative thought patterns."
    },
    "Dr. Jackson": {
        "name": "Dr. Michael Jackson",
        "specialty": "Mindfulness and Wellness Coach",
        "style": "You are nurturing and optimistic, guiding users to embrace mindfulness and self-compassion."
    },
}

# App title
st.title("Mental Health Practitioner: AI Chatbot 🤖")
st.subheader("Choose your preferred practitioner and start chatting.")

# User selects a practitioner
if not st.session_state.selected_practitioner:
    st.markdown("### Select a Practitioner")
    for key, details in practitioners.items():
        if st.button(f"Chat with {details['name']}"):
            st.session_state.selected_practitioner = key
            st.success(f"You are now chatting with {details['name']}.")

# Chat functionality
if st.session_state.selected_practitioner:
    practitioner = practitioners[st.session_state.selected_practitioner]
    st.markdown(f"### You are chatting with {practitioner['name']} ({practitioner['specialty']})")

    # Input and send button
    user_message = st.text_input("You:", key="user_message", placeholder="Type your message here...")

    if st.button("Send"):
        if user_message.strip() != "":
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_message})

            # Generate AI response
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"{practitioner['style']}"},
                    ] + st.session_state.chat_history,
                    max_tokens=400,
                    temperature=0.7,
                )
                ai_response = response.choices[0].message.content.strip()

                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error generating AI response: {e}")

    # Display chat history
    st.markdown("### Chat History")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**{practitioner['name']}:** {message['content']}")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
