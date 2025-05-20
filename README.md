# Quizzify – AI-powered PDF-to-Quiz Builder 📚➜❓

Quizzify is a **Streamlit** application that transforms any collection of PDFs into an interactive multiple-choice quiz in just a few clicks.

---

## ✨ Features
- **Drag-and-drop** multi-PDF ingestion  
- **On-device** vector search with **ChromaDB** – no external DB required  
- **Retrieval-augmented** question generation (up to 10 questions per topic)  
- Quiz navigation with instant feedback & explanations  
- Modular, testable codebase

---

## 🛠️ How It Works
1. **Ingest PDFs** → `task3.py` (**DocumentProcessor**)  
2. **Embed text** → `task4.py` (**EmbeddingClient**, Google Vertex AI)  
3. **Index chunks** → `task5.py` (**ChromaCollectionCreator**)  
4. **Generate questions** → `task8.py` (**QuizGenerator**, RAG + Gemini-Pro)  
5. **Run UI & scoring** → `task10.py` (**Streamlit app**)  

---

## 📁 Repository Structure
```text
.
├── task3.py   # DocumentProcessor – PDF upload & parsing
├── task4.py   # EmbeddingClient – Vertex AI text embeddings
├── task5.py   # ChromaCollectionCreator – vector-store builder
├── task8.py   # QuizGenerator – RAG + Gemini-Pro
├── task9.py   # QuizManager – helpers for navigation & state
├── task10.py  # Main Streamlit app (end-to-end workflow)
├── requirements.txt
└── README.md
