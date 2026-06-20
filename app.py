import os
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

txt_path = "textbook.txt"

if os.path.exists(txt_path):
    print("📚 Found your Stone Age textbook! Reading it now...")
    loader = TextLoader(txt_path, encoding="utf-8")
    documents = loader.load()

    # Bypassing Ollama server errors entirely using local huggingface embeddings
    print("✨ Initializing textbook reader module...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("🧠 Training Socratiq on the Stone Age chapters...")
    db = Chroma.from_documents(documents, embeddings, persist_directory="./socratiq_db")
    print("✅ Success! Socratiq database is ready.")
else:
    print("❌ Please make sure 'textbook.txt' is saved in this folder!")