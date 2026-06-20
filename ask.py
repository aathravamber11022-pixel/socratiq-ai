from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

# 1. Connect to the textbook database you just built
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./socratiq_db", embedding_function=embeddings)

# 2. Connect to your local AI engine (Llama 3.2)
llm = OllamaLLM(model="llama3.2")

# 3. What were microliths and during which period were they used?
question = "What were microliths and during which period were they used?"

print(f"❓ Question: {question}")
print("🔍 Searching your textbook database for the answer...\n")

# Pull the exact relevant text out of your textbook database
docs = db.similarity_search(question, k=1)
context = docs[0].page_content

# Give the textbook text to the AI and ask it to explain it to you
prompt = f"""You are a helpful Socratic history tutor. Answer the question using ONLY the provided textbook context.

Context:
{context}

Question: {question}
"""

response = llm.invoke(prompt)

print("🤖 Socratiq Tutor Says:")
print(response)