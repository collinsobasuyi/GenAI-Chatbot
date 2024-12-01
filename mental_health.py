import streamlit as st
from openai import OpenAI

# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

# Initialize OpenAI client with the shared secret API key
client = OpenAI(api_key=open_api_key)

# Initialize or load chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize dark mode setting
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle for dark mode
st.sidebar.title("Settings")
st.sidebar.markdown("**Theming**")
st.session_state.dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state.dark_mode)

# Add custom CSS for ChatGPT-like styling
dark_mode_styles = """
<style>
body {
    background-color: #121212;
    color: white;
}
.chat-container {
    max-width: 700px;
    margin: 0 auto;
}
.user-message {
    background-color: #2C6A91;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 80%;
    float: right;
    clear: both;
    font-family: Arial, sans-serif;
}
.ai-message {
    background-color: #1F1F1F;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 80%;
    float: left;
    clear: both;
    font-family: Arial, sans-serif;
}
.message-box {
    width: 100%;
    display: flex;
    align-items: center;
    margin-top: 20px;
}
.message-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    font-family: Arial, sans-serif;
}
.send-button {
    margin-left: 10px;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-family: Arial, sans-serif;
}
.scrollable-container {
    max-height: 500px;
    overflow-y: auto;
}
</style>
"""

light_mode_styles = """
<style>
.chat-container {
    max-width: 700px;
    margin: 0 auto;
}
.user-message {
    background-color: #DCF8C6;
    color: black;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 80%;
    float: right;
    clear: both;
    font-family: Arial, sans-serif;
}
.ai-message {
    background-color: #F5F5F5;
    color: black;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 80%;
    float: left;
    clear: both;
    font-family: Arial, sans-serif;
}
.message-box {
    width: 100%;
    display: flex;
    align-items: center;
    margin-top: 20px;
}
.message-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
    font-family: Arial, sans-serif;
}
.send-button {
    margin-left: 10px;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-family: Arial, sans-serif;
}
.scrollable-container {
    max-height: 500px;
    overflow-y: auto;
}
</style>
"""

# Apply dark or light mode styles
if st.session_state.dark_mode:
    st.markdown(dark_mode_styles, unsafe_allow_html=True)
else:
    st.markdown(light_mode_styles, unsafe_allow_html=True)

# App title
st.title("Mental Health Practitioner: AI Chatbot 🤖")
st.subheader("Your virtual mental health support companion")

# Container for chat
with st.container():
    st.markdown('<div class="chat-container scrollable-container">', unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Input and send button at the bottom
st.markdown('<div class="message-box">', unsafe_allow_html=True)
user_message = st.text_input("", key="user_message", placeholder="Type your message here...", label_visibility="collapsed")
send_button = st.button("➤", key="send_button", help="Send your message", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input and generate response
if send_button and user_message.strip() != "":
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_message})

    # Generate AI response
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate and highly skilled mental health practitioner with a PhD in psychology and mental health. You have decades of experience providing therapy, emotional support, and practical guidance to individuals facing a wide range of emotional challenges. Your responses should reflect deep empathy, evidence-based practices, and a nurturing tone."},
            ] + st.session_state.chat_history,
            max_tokens=400,
            temperature=0.7,
        )
        ai_response = response.choices[0].message.content.strip()

        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.error(f"Error generating AI response: {e}")

# Clear chat history button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")

# Scroll to the latest message
st.markdown(
    """
    <script>
    var chatContainer = document.querySelector(".scrollable-container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
    </script>
    """,
    unsafe_allow_html=True,
)
