import chromadb
from chromadb.utils import embedding_functions
from langchain_ollama import OllamaLLM

print("?? Booting MedShield Modern Grounded RAG Pipeline...")

# 1. Connect to Local Vector Database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_collection(name="clinical_notes_collection", embedding_function=default_ef)

# 2. Define the Operational Query
user_query = "What medication was prescribed to the patient presenting with acute chest pain?"
print(f"? User Query: {user_query}")

# 3. Retrieve and explicitly extract the first list of documents
search_results = collection.query(query_texts=[user_query], n_results=2)
# Extract the first sub-list of document strings cleanly
retrieved_chunks = search_results['documents'][0]
retrieved_context = "\n".join(retrieved_chunks)

print("?? Context successfully retrieved and flattened from ChromaDB.")

# 4. Initialize the Local Ollama Engine
llm = OllamaLLM(model="llama3.2:1b")

# 5. Deploy an Optimized, Punchy Prompt for 1B Models
system_prompt = f"""
Context: {retrieved_context}
Question: {user_query}

Instruction: Answer the question using only the context provided above. Be short and direct.
Answer:
"""

print("?? Passing grounded data block to local Llama3.2 engine...")
print("================== LLM GENERATED REPORT ==================\n")

# 6. Generate the Clean Response
response = llm.invoke(system_prompt)
print(response)

print("\n==========================================================")
print("? Local inference cycle complete. Array formatting and prompt optimized.")
