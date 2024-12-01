import streamlit as st
from openai import OpenAI

# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=open_api_key)

# Initialize or load chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add custom CSS for chat UI
st.markdown(
    """
    <style>
    .user-bubble {
        background-color: #DCF8C6;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 60%;
        float: right;
        clear: both;
    }
    .ai-bubble {
        background-color: #FFFFFF;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 60%;
        float: left;
        clear: both;
        border: 1px solid #ddd;
    }
    .message-container {
        width: 100%;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("Mental Health Chatbot")

# Input message
user_message = st.text_input("Type your message:", key="user_message")

if st.button("Send"):
    if user_message:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        # Generate AI response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a kind and empathetic mental health practitioner."},
                ] + st.session_state.chat_history,
                max_tokens=400,
                temperature=0.7,
            )
            ai_response = response.choices[0].message.content.strip()

            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"Error generating AI response: {e}")

# Display chat history with styling
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="message-container"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="message-container"><div class="ai-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
