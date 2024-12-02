import streamlit as st
from openai import OpenAI

# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

# Initialize OpenAI client with the shared secret API key
client = OpenAI(api_key=open_api_key)

# Initialize or load chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize user_message in session state
if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# Practitioners definition
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

# Helper function to process user input
def handle_user_input():
    # Safely retrieve and process the user message
    user_message = st.session_state.get("user_message", "").strip()
    if user_message:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        # Clear the text box
        st.session_state["user_message"] = ""

        # Generate AI Response
        try:
            practitioner = practitioners[st.session_state["selected_practitioner"]]
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": practitioner["style"]},
                ] + st.session_state.chat_history,
                max_tokens=400,
                temperature=0.7,
            )
            ai_response = response.choices[0].message.content.strip()

            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"Error generating AI response: {e}")

# Sidebar for selecting a practitioner
st.sidebar.title("Select a Practitioner")
st.session_state["selected_practitioner"] = st.sidebar.radio(
    "Choose a mental health practitioner",
    list(practitioners.keys()),
)

# App Header
practitioner = practitioners[st.session_state["selected_practitioner"]]
st.title(f"Chat with {practitioner['name']}")
st.subheader(f"{practitioner['specialty']}")

# Chat Container
st.markdown('<div class="chat-container scrollable-container">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input Box and Send Button
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.text_input(
    "",
    key="user_message",
    placeholder="Type your message here...",
    label_visibility="collapsed",
)
send_button = st.button("Send", key="send_button", help="Send your message")
st.markdown('</div>', unsafe_allow_html=True)

# Handle Send Action
if send_button:
    handle_user_input()

# Scroll to the Latest Message
st.markdown(
    """
    <script>
    var chatContainer = document.querySelector(".scrollable-container");
    chatContainer.scrollTop = chatContainer.scrollHeight;
    </script>
    """,
    unsafe_allow_html=True,
)

# Clear Chat Button
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")
