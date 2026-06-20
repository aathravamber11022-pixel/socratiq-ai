import streamlit as st
from groq import Groq
import os

# 1. Page Config
st.set_page_config(page_title="Socratiq AI", page_icon="🤖", layout="wide")

# 2. CSS for clean layout
st.markdown("""
    <style>
    [data-testid="stHeader"] { visibility: hidden !important; }
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        background-color: #2b2b2b !important;
        border: 1px solid #444 !important;
    }
    [data-testid="stChatInput"]::after {
        content: "🎙️  ➤";
        position: absolute;
        right: 25px;
        top: 15px;
        color: #888888;
        font-size: 20px;
        pointer-events: none;
    }
    [data-testid="stChatInput"] button {
        opacity: 0 !important;
        right: 15px !important;
        z-index: 10 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Setup Logic
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Groq API Key not found in settings!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar with File Uploader
with st.sidebar:
    st.title("🤖 Socratiq AI")
    st.write("---")
    uploaded_file = st.file_uploader("Upload Image or Document", type=['png', 'jpg', 'jpeg', 'pdf', 'txt'])
    st.write("---")
    if st.button("➕ New Session"):
        st.session_state.messages = []
        st.rerun()

# 5. UI
st.markdown("<h1 style='text-align: center;'>Socratiq AI</h1>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("Ask Socratiq AI..."):
    # If a file was uploaded, attach its name to the prompt
    if uploaded_file:
        prompt = f"[File Attached: {uploaded_file.name}] \n\n {prompt}"
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
