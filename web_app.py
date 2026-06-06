import streamlit as st
from groq import Groq

# 1. Page Configuration (Sets the browser tab title and top-left icon)
st.set_page_config(
    page_title="Socratiq AI",
    page_icon="🤖",
    layout="wide"
)

# 2. Native CSS styling using st.html (Completely safe from TypeErrors)
st.html("""
    <style>
    /* Smooth rounded edges for chat bubbles */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    /* Smooth rounded corners for text inputs */
    div[data-baseweb="textarea"], div[data-baseweb="input"] {
        border-radius: 20px !important;
    }
    </style>
""")

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
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.write("---")
    
    # Library / Previous Chats Section
    st.subheader("📚 Library")
    st.caption("🕒 Recent History")
    st.markdown("• *Welcome to Socratiq AI*")
    st.markdown("• *AI Assistant Dashboard*")
    
    st.write("---")
    
    # Premium Upgrade Button (Using a beautiful native button instead of crashing HTML!)
    if st.button("🚀 Upgrade to Premium", use_container_width=True, type="primary"):
        st.toast("Premium features coming soon!")
    
    st.write("---")
    
    # Account / Email Login layout placeholder
    st.caption("👤 Account Profile")
    email_input = st.text_input("Login Email", placeholder="user@example.com")
    if email_input:
        st.success("Logged in!", icon="✅")

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

    # Generate response from Groq using llama3-8b model
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Request completion from Groq
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=False
            )
            
            full_response = completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            
        # Add assistant response to session chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"An error occurred while connecting to Groq: {e}")
