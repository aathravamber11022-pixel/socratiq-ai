import streamlit as st
from duckduckgo_search import DDGS  # Direct, foolproof open-source import
from langchain_groq import ChatGroq

# 1. Premium App Settings
st.set_page_config(
    page_title="Socratiq AI", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Premium Custom CSS (Dark Theme, Glassmorphism)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f111a 0%, #151926 100%);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .premium-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .premium-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: rgba(79, 70, 229, 0.1) !important;
        border: 1px solid rgba(79, 70, 229, 0.25) !important;
        border-radius: 16px !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
    }
    .stChatInput textarea {
        background-color: #1e2235 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="premium-title">Socratiq AI</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Next-generation cloud-powered intelligence engine.</div>', unsafe_allow_html=True)

# 3. Enter your free API Key here
# TODO: Replace the text below with your actual gsk_ key from console.groq.com
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

@st.cache_resource
def load_ai():
    # Connects to Groq's high-speed, currently supported Llama 3.1 model
    return ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)

# 4. App Core Execution Loop
if GROQ_API_KEY == "PASTE_YOUR_GSK_KEY_HERE":
    st.info("⚠️ Please paste your free Groq API key into line 55 of the code to activate the engine!")
else:
    try:
        llm = load_ai()
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_question := st.chat_input("Query anything across the web..."):
            with st.chat_message("user"):
                st.markdown(user_question)
            st.session_state.messages.append({"role": "user", "content": user_question})

            with st.spinner("⚡ Fetching live web telemetry..."):
                try:
                    # Direct query to DuckDuckGo search library
                    with DDGS() as ddgs:
                        search_results = [r for r in ddgs.text(user_question, max_results=3)]
                    web_results = " ".join([res['body'] for res in search_results])
                except Exception:
                    web_results = "No live web telemetry retrieved."
                
                # Directives to infuse the authentic, scannable, adaptive personality
                prompt = f"""You are Socratiq AI, an authentic, adaptive AI collaborator with a touch of wit. 
                Your goal is to address the user's true intent with insightful, clear, and concise responses. 
                Balance empathy with candor: be supportive and grounded, but direct. Style your tone, energy, and humor to match the user.

                STRICT RESPONSE RULES:
                1. NEVER use robotic filler or intros (e.g., "Based on the search results...", "As an AI..."). Dive directly into the answer.
                2. Use the Formatting Toolkit: Create a clear, scannable, organized response using Markdown. Use Headings (##, ###), Horizontal Rules (---), Judicious Bolding, and Bullet Points to avoid dense walls of text. 
                3. Prioritize clarity at a glance. Keep it concise, engaging, and genuinely helpful—like a brilliant peer, not a rigid lecturer.

                Live Internet Telemetry:
                {web_results}
                
                User Question: {user_question}
                """
                
                response = llm.invoke(prompt)

            with st.chat_message("assistant"):
                st.markdown(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response.content})

    except Exception as e:
        st.error(f"Engine connection error: {e}")
