import streamlit as st
from groq import Groq

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="ELM AI",
    page_icon="🟣",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS (Safe & Stable Purple Theme) ---
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
        text-shadow: 0 0 20px rgba(176, 38, 255, 0.5);
    }
    
    .elm-subtitle {
        text-align: center;
        color: #c4b5fd;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }
    
    /* Chat Input Styling */
    .stChatInputContainer {
        background-color: rgba(48, 43, 99, 0.6);
        border-radius: 15px;
        border: 1px solid #7c3aed;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b21a8;
        font-size: 0.8rem;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Branding Header ---
st.markdown('<div class="elm-title">🟣 ELM</div>', unsafe_allow_html=True)
st.markdown('<div class="elm-subtitle">Intelligent Assistant • Powered by Groq</div>', unsafe_allow_html=True)

# --- 4. Secure API Key Check ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("🔒 **Security Alert:** API Key not found in Streamlit Secrets.")
    st.info("Please add `GROQ_API_KEY` to your app settings in Streamlit Cloud.")
    st.stop()

# Initialize Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize client: {e}")
    st.stop()

# --- 5. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History (Using native st.chat_message for stability)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. Chat Logic ---
if prompt := st.chat_input("Ask ELM anything..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("ELM is thinking..."):
            try:
                # System Prompt for Personality
                system_prompt = """
                You are ELM, a sophisticated AI assistant. 
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
                
                # Write stream to chat bubble
                response = st.write_stream(stream)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"⚠️ ELM Error: {str(e)}")

# --- 7. Footer ---
st.markdown('<div class="footer">© 2024 ELM AI Systems</div>', unsafe_allow_html=True)
