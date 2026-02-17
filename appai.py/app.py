import streamlit as st
from groq import Groq

# --- Page Config ---
st.set_page_config(page_title="My AI Problem Solver", page_icon="🤖")
st.title("🤖 AI Problem Solver")

# --- Sidebar for Settings ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    # We use st.secrets for the API key when deployed, but allow input for local testing
    api_key = st.text_input("Enter Groq API Key", type="password")
    user_name = st.text_input("Your Name", "Visitor")
    user_goal = st.text_area("What do you want to solve?", "General questions")

    st.markdown("---")
    st.info("💡 Powered by Groq & Streamlit (Free Tier)")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Ask me anything..."):
    if not api_key:
        st.warning("Please enter your Groq API Key in the sidebar to start!")
        st.stop()

    # 1. Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Prepare Personalized System Prompt
    system_instruction = f"""
    You are a helpful AI assistant. 
    User Name: {user_name}
    User Goal: {user_goal}
    Task: Answer questions personally and help solve real-world problems based on their goal.
    Keep answers clear and actionable.
    """

    # 3. Get response from Groq API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Free, fast model
                    messages=[
                        {"role": "system", "content": system_instruction},
                        *st.session_state.messages
                    ]
                )
                ai_reply = response.choices[0].message.content
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"Error: {e}")