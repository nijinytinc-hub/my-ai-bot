import streamlit as st
from groq import Groq
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="ELM AI",
    page_icon="🟣",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS (Purple Theme & Animations) ---
st.markdown("""
    <style>
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Background - Deep Purple Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Chat Input Container */
    .stChatInputContainer {
        background-color: rgba(48, 43, 99, 0.5);
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #b026ff;
        box-shadow: 0 0 15px rgba(176, 38, 255, 0.3);
    }
    
    /* Chat Bubbles - User */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(76, 29, 149, 0.4);
        border-radius: 15px 15px 0 15px;
        border-left: 4px solid #7c3aed;
    }
    
    /* Chat Bubbles - AI (ELM) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(139, 92, 246, 0.2);
        border-radius: 15px 15px 15px 0;
        border-right: 4px solid #b026ff;
        box-shadow: 0 0 10px rgba(176, 38, 255, 0.2);
    }
    
    /* Text Colors */
    .stChatMessage {
        color: #e9d5ff !important;
    }
    
    /* ELM Title Animation */
    .elm-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #d8b4fe, #b026ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        animation: glow 3s infinite alternate;
        text-shadow: 0 0 20px rgba(176, 38, 255, 0.5);
    }
    
    .elm-subtitle {
        text-align: center;
        color: #c4b5fd;
        margin-bottom: 30px;
        font-size: 1.1rem;
        animation: fadeIn 2s ease;
    }
    
    /* Animations */
    @keyframes glow {
        from { text-shadow: 0 0 10px rgba(176, 38, 255, 0.5); }
        to { text-shadow: 0 0 25px rgba(176, 38, 255, 0.9); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Message Animation */
    div[data-testid="stChatMessage"] {
        animation: slideUp 0.4s ease forwards;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #7c3aed, #b026ff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Branding Header ---
st.markdown('<div class="elm-title">🟣 ELM</div>', unsafe_allow_html=True)
st.markdown('<div class="elm-subtitle">Intelligent Assistant • Powered by Groq</div>', unsafe_allow_html=True)

# --- 4. Secure API Key Check ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔒 **Security Alert:** API Key not found in Streamlit Secrets.")
    st.info("Please add `GROQ_API_KEY` to your app settings.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 5. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. Chat Logic ---
if prompt := st.chat_input("Ask ELM anything..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("ELM is thinking..."):
            try:
                # System Prompt for Personality
                system_prompt = """
                You are ELM, a sophisticated AI assistant. 
                Your theme is purple and dynamic. 
                Be concise, helpful, and solve real-world problems.
                Use formatting (bold, lists) to make answers clear.
                """
                
                # Stream the response
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # ✅ Updated Model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ],
                    stream=True,
                )
                
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"⚠️ ELM Error: {str(e)}")

# --- 7. Footer ---
st.markdown("---")
st.markdown('<p style="text-align: center; color: #6b21a8; font-size: 0.8rem;">© 2024 ELM AI Systems</p>', unsafe_allow_html=True)
