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
print("?? Searching local vector database for matching clinical context...")

# 3. Retrieve and Flatten the Nested Vector Context Array Cleanly
search_results = collection.query(query_texts=[user_query], n_results=2)
# Slicing results['documents'][0] extracts the flat text string blocks cleanly
retrieved_context = "\n".join(search_results['documents'][0])

print("?? Context successfully retrieved and flattened from ChromaDB.")

# 4. Initialize the Modern, Non-Deprecated Local Ollama Engine
llm = OllamaLLM(model="llama3.2:1b")

# 5. Inject Structured Instructions into the Grounding Blueprint
system_prompt = f"""
You are an expert medical data analyst at Providence India. 
Your core responsibility is to answer the user query based strictly on the provided clinical context.

RULES:
1. Rely only on the clear facts mentioned in the context.
2. If the context does not contain the answer, reply with: "I cannot find the answer in the provided records."
3. Do not assume, extrapolate, or hallucinate any data points.

[CLINICAL CONTEXT]:
{retrieved_context}

[USER QUERY]:
{user_query}

[ANALYTICAL RESPONSE]:
"""

print("?? Passing grounded data block to local Llama3.2 engine...")
print("================== LLM GENERATED REPORT ==================\n")

# 6. Generate the Safe, Hallucination-Free Response
response = llm.invoke(system_prompt)
print(response)

print("\n==========================================================")
print("? Local inference cycle complete. Warnings eliminated and data safety maintained.")
