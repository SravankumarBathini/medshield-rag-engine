import sqlite3
import chromadb
from chromadb.utils import embedding_functions
from langchain_ollama import OllamaLLM

print("?? Initializing Guarded MedShield Routing Engine...")

# 1. Initialize Our Free Local LLM Core
llm = OllamaLLM(model="llama3.2:1b")

# 2. Define the Routing Logic Function (Agent A: The Router)
def route_user_query(query_text):
    routing_prompt = f"""
    You are an advanced query router for a healthcare data system. 
    Analyze the incoming user question and classify it into exactly one of two categories: 'SQL' or 'VECTOR'.

    CRITERIA:
    - Choose 'SQL' if the question requires mathematical calculations, totals, counting patients, averaging costs, or filtering structured fields like dates and departments.
    - Choose 'VECTOR' if the question asks about medical details, symptoms, clinical notes, doctor descriptions, or specific medications prescribed.

    Output only the single word 'SQL' or 'VECTOR'. Do not add any punctuation, letters, or explanation.

    Question: {query_text}
    Category:
    """
    decision = llm.invoke(routing_prompt).strip().upper()
    return "SQL" if "SQL" in decision else "VECTOR"

# 3. Define the Guarded SQL Execution Tool
def execute_sql_analytics(query_text):
    print("?? Routing to SQL Analytics Warehouse...")
    
    sql_generation_prompt = f"""
    Context: The table is named 'patient_admissions' and has these columns:
    - patient_id (TEXT)
    - admission_date (TEXT)
    - discharge_date (TEXT)
    - department (TEXT)
    - billing_amount (REAL)
    - doctor_notes (TEXT)

    CRITICAL RULES:
    1. Always use parentheses for aggregate functions: SUM(billing_amount), AVG(billing_amount), COUNT(patient_id).
    2. Return ONLY the raw SQL query text. No code blocks, no backticks, no explanations.

    EXAMPLES:
    Question: What is the total billing for Cardiology?
    SQL Query: SELECT SUM(billing_amount) FROM patient_admissions WHERE department = 'Cardiology'

    Question: Count patients in Neurology
    SQL Query: SELECT COUNT(patient_id) FROM patient_admissions WHERE department = 'Neurology'

    Question: {query_text}
    SQL Query:
    """
    
    generated_sql = llm.invoke(sql_generation_prompt).strip()
    generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
    
    print(f"?? Guarded Generated SQL: {generated_sql}")
    
    try:
        conn = sqlite3.connect("providence_clinical.db")
        cursor = conn.cursor()
        cursor.execute(generated_sql)
        results = cursor.fetchall()
        conn.close()
        
        # Defensive Data Unpacking for SQL results (extracting value from nested tuple safely)
        if results and results[0][0] is not None:
            raw_value = float(results[0][0])
            formatted_val = f"INR {raw_value:,.2f}"
            return f"?? Calculation Result: {formatted_val}"
        return f"Database Result: {results}"
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

# 4. Define the Unstructured Vector Retrieval Tool with List-Flattening Guards
def execute_vector_retrieval(query_text):
    print("?? Routing to Semantic Vector Store...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    default_ef = embedding_functions.DefaultEmbeddingFunction()
    collection = chroma_client.get_collection(name="clinical_notes_collection", embedding_function=default_ef)
    
    search_results = collection.query(query_texts=[query_text], n_results=1)
    
    # Code Guard: Extract the first row [0] to flatten the inner array lists securely
    retrieved_chunks = search_results['documents'][0]
    retrieved_context = "\n".join(retrieved_chunks)
    
    context_prompt = f"""
    Context: {retrieved_context}
    Question: {query_text}
    Instruction: Answer using only the context block. Be short and direct.
    Answer:
    """
    return llm.invoke(context_prompt)

# 5. Core Operational Controller Loop
test_query = "What is the total billing amount accumulated for the Oncology department?"
print(f"\n?? Incoming Clinical Inquiry: '{test_query}'")

target_route = route_user_query(test_query)
print(f"?? Router Agent Decision: Diverting payload to --> [{target_route} LAYER]")

if target_route == "SQL":
    final_output = execute_sql_analytics(test_query)
else:
    final_output = execute_vector_retrieval(test_query)

print("\n==================== ENGINE REPORT ====================")
print(final_output)
print("=======================================================")
