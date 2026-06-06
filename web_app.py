import streamlit as st
from groq import Groq

# 1. Page Configuration (Sets the browser tab title and top-left icon)
st.set_page_config(
    page_title="Socratiq AI",
    page_icon="🤖",
    layout="wide"
)

# 2. Custom CSS styling for smooth rounded edges and premium look
st.markdown("""
    <style>
    /* Smooth rounded edges for chat bubbles */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    /* Smooth rounded corners for the text input box */
    div[data-baseweb="textarea"], div[data-baseweb="input"] {
        border-radius: 20px !important;
    }
    /* Styling for the upgrade button in sidebar */
    .upgrade-btn {
        background-color: #FF4B4B;
        color: white;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_html=True)

# 3. Initialize Groq Client securely using the secret key nickname
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Groq API Key not found in Streamlit Secrets. Please check your dashboard configuration.")
    st.stop()

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Building the Premium Left Sidebar
with st.sidebar:
    st.title("🤖 Socratiq AI")
    
    # New Chat Button (Resets the chat history seamlessly)
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.write("---")
    
    # Library / Previous Chats Section
    st.subheader("📚 Library")
    st.caption("🕒 Recent History")
    # You can add static titles here for show, or let it update dynamically later
    st.markdown("• *Welcome to Socratiq AI*")
    st.markdown("• *AI Assistant Dashboard*")
    
    st.write("---")
    
    # Premium Upgrade Block
    st.markdown('<div class="upgrade-btn">🚀 Upgrade to Premium</div>', unsafe_html=True)
    
    st.write("---")
    
    # Account / Email Login layout placeholder
    st.caption("👤 Account Profile")
    email_input = st.text_input("Login Email", placeholder="user@example.com")
    if email_input:
        st.success(block=False, icon="✅", body="Logged in!")

# 5. Main Chat Window Layout
st.title("Chat with Socratiq AI")
st.caption("Powered by Groq Cloud Engine | High-Speed AI Inference")

# Display previous messages from session state with smooth container styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user chat input
if prompt := st.chat_input("Ask Socratiq AI anything..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from Groq using llama3-8b model (or replace with your specific model name)
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Request streaming completion from Groq
            completion = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=False # Change to True later if you want typewriter streaming
            )
            
            full_response = completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            
        # Add assistant response to session chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"An error occurred while connecting to Groq: {e}")
