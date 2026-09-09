import sqlite3
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

print("? Starting Text Chunking & Vector Ingestion Loop...")

# 1. Connect to Local SQL Warehouse
conn = sqlite3.connect("providence_clinical.db")
df = pd.read_sql_query("SELECT patient_id, department, doctor_notes FROM patient_admissions", conn)
conn.close()
print(f"?? Successfully extracted {len(df)} clinical notes from SQLite.")

# 2. Define Semantic Chunking Layout
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,
    length_function=len
)

documents = []
metadatas = []
ids = []

# 3. Process Text and Map Relational Metadata Links
for idx, row in df.iterrows():
    chunks = text_splitter.split_text(row['doctor_notes'])
    for chunk_idx, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            "patient_id": row['patient_id'],
            "department": row['department']
        })
        ids.append(f"{row['patient_id']}_chunk_{chunk_idx}")

# 4. Initialize Local, Free Vector Store (ChromaDB)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="clinical_notes_collection",
    embedding_function=default_ef
)

# 5. Bulk Upload Chunks into Vector Database
collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("? Ingestion Complete! Vectorized and indexed semantic chunks into local 'chroma_db' folder.")
