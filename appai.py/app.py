import streamlit as st
from groq import Groq
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="ELM AI",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS for Dynamic UI & Animations ---
st.markdown("""
    <style>
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* Chat Bubble Styling */
    .user-message {
        background-color: #2b313f;
        color: #ffffff;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        animation: fadeIn 0.5s ease;
    }
    .ai-message {
        background-color: #1f2937;
        color: #00ff9d; /* ELM Green Accent */
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom:10px;
        border-left: 3px solid #00ff9d;
        animation: slideUp 0.5s ease;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* Branding */
    .elm-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff9d;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Branding Header ---
st.markdown('<div class="elm-title">🌱 ELM</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">Your Personal Intelligent Assistant</p>',
            unsafe_allow_html=True)

# --- 4. API Key Management (Secure) ---
# Check if key exists in Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

# --- 5. Chat Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History with Custom HTML
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)

# --- 6. Input Area ---
if prompt := st.chat_input("Ask ELM anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # System Prompt for Personalization
            system_prompt = "You are ELM, a professional AI assistant. Be concise, helpful, and solve real-world problems."

            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
                stream=True,  # Enables typing effect
            )

            # Streaming Response (Typing Effect)
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"ELM encountered an error: {e}")

# --- 7. Footer ---
st.markdown("---")
st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #555;">Powered by ELM AI © 2024</p>',
            unsafe_allow_html=True)