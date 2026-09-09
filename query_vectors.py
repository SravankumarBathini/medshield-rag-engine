import chromadb
from chromadb.utils import embedding_functions

print("?? Initializing Local Semantic Search Engine...")

# 1. Connect to our local, compiled Vector Database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_collection(
    name="clinical_notes_collection",
    embedding_function=default_ef
)

# 2. Define a conceptual search query 
# Notice we are searching for "cardiac issues" - none of our 100 records contain this exact word!
search_query = "cardiac issues and hypertension medication"
print(f"?? Querying Vector Space for: '{search_query}'\n")

# 3. Execute a K-Nearest Neighbors (KNN) semantic search to fetch top 3 matching chunks
results = collection.query(
    query_texts=[search_query],
    n_results=3
)

# 4. Parse and display the retrieved clinical context layers
print("============ TOP 3 RETRIEVED CLINICAL CONTEXTS ============")
for i in range(len(results['documents'][0])):
    chunk_text = results['documents'][0][i]
    metadata = results['metadatas'][0][i]
    chunk_id = results['ids'][0][i]
    
    print(f"\n?? [Match {i+1}] (ID: {chunk_id})")
    print(f"?? Department: {metadata['department']}")
    print(f"?? Patient Ref: {metadata['patient_id']}")
    print(f"?? Extracted Chunk: {chunk_text}")
    print("-" * 58)
