# MedShield: Intelligent Clinical RAG & Multi-Agent Analytics Engine

An enterprise-grade, zero-cost AI analytics pipeline designed to process multi-structured clinical datasets securely. The engine orchestrates a local routing framework that dynamically selects between a Structural SQL Analytics Warehouse Layer and an Unstructured Semantic Vector Retrieval Layer to deliver 100% data-grounded, hallucination-free business insights.

---

## System Architecture & Data Flow

[ Unstructured Raw Patient Data ]  (PDFs, Lab JSONs, EHR Texts)
               │
               ▼
   [ 1. DATA TRANSFORMATION LAYER ] ──► Advanced Python Parsing & Text Chunking
               │
               ▼
   [ 2. ANALYTICAL WAREHOUSE ]      ──► Production SQL Modeling (SQLite / Star Schema)
               │
               ▼
   [ 3. EMBEDDING & SEARCH CORE ]   ──► Local ChromaDB (Semantic Mapping Matrix)
               │
               ▼
   [ 4. AGENTIC ORCHESTRATION ]     ──► Multi-Agent Routing Engine:
                                         ├── Route A: SQL Query Generation (Metrics/Totals)
                                         └── Route B: Grounded RAG Extraction (Symptoms/Meds)
               │
               ▼
[ Secure Dashboard / LLM Response ] ──► Verified, Hallucination-Free Clinical Insights

---

## Free & Open-Source Tech Stack
* Data Engineering Core: SQL (SQLite Core), Python (Pandas, NumPy)
* Vector Engine Store: ChromaDB running locally with native all-MiniLM-L6-v2 embeddings
* Orchestration Framework: LangChain & LangChain-Ollama integration layers
* Inference Engine Processing: Ollama running Meta Llama 3.2 1b foundation model locally

---

## Local Installation & Quickstart

### 1. Initialize Environment
Navigate inside the project repository, set up your isolated virtual environment sandbox, and install the core dependencies:
```bash
pip install pandas numpy chromadb langchain-ollama langchain-text-splitters
```

### 2. Pipeline Ingestion & Runtime Execution
* Run 'python generate_warehouse.py' to compile your local database table assets.
* Run 'python ingest_vectors.py' to chunk and index unstructured medical texts.
* Run 'python analytics_router.py' to launch the live dual-path routing engine.

---

## Production Design Justifications (Interview Defense)
* Zero-Cost Infrastructure: Avoids reliance on expensive external subscription APIs. The entire database, embedding matrix, and text generation cycles run locally on standard consumer-grade hardware.
* Strict Healthcare Data Security: Sensitive clinical files, medical histories, and notes never cross the public internet, maintaining complete data privacy compliance within local firewalled network borders.
* Hallucination Elimination: Leverages strict few-shot contextual grounding constraints. The LLM is restricted to reading only the context retrieved by our system, dropping factual errors to near zero.
