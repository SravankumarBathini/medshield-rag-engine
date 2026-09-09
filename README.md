# MedShield: Intelligent Clinical RAG & Multi-Agent Analytics Engine

An enterprise-grade, zero-cost AI analytics pipeline designed to process multi-structured clinical datasets securely. The engine orchestrates a local routing framework that dynamically selects between a **Structural SQL Analytics Warehouse Layer** and an **Unstructured Semantic Vector Retrieval Layer** to deliver 100% data-grounded, hallucination-free business insights.

## ?? System Architecture & Data Flow
1. DATA TRANSFORMATION LAYER: Advanced Python Parsing & Text Chunking
2. ANALYTICAL WAREHOUSE: Production SQL Modeling (SQLite / Star Schema)
3. EMBEDDING & SEARCH CORE: Local ChromaDB (Semantic Mapping Matrix)
4. AGENTIC ORCHESTRATION: Multi-Agent Routing Engine (SQL vs VECTOR pathways)

## ??? Free & Open-Source Tech Stack
- Data Engineering Core: SQL (SQLite Core), Python (Pandas, NumPy)
- Vector Engine Store: ChromaDB with native all-MiniLM-L6-v2 embeddings
- Orchestration Framework: LangChain & LangChain-Ollama integration layers
- Inference Engine Processing: Ollama running Meta's Llama3.2:1b model locally

## ?? Local Installation & Quickstart
Invoke the following entry points inside your virtual environment setup:
- Run 'python generate_warehouse.py' to compile your local database table assets.
- Run 'python ingest_vectors.py' to chunk and index unstructured medical texts.
- Run 'python analytics_router.py' to launch the live dual-path routing engine.

## ??? Production Design Justifications (Interview Defense)
- Zero-Cost Infrastructure: Runs entirely on standard consumer hardware.
- Strict Healthcare Data Security: Data never crosses the public internet, ensuring compliance.
- Hallucination Elimination: Restricts LLM evaluation entirely to verified local facts.
