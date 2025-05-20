Quizzify – AI-powered PDF-to-Quiz Builder 📚➜❓
Quizzify is a Streamlit application that turns any set of PDF documents into an interactive multiple-choice quiz in just a few clicks.

How It Works
Ingest PDFs with task3.py (DocumentProcessor)

Embed text using Google Vertex AI via task4.py (EmbeddingClient)

Index chunks in a local Chroma vector store with task5.py (ChromaCollectionCreator)

Generate questions through retrieval-augmented generation in task8.py (QuizGenerator)

Run the Streamlit UI in task10.py, which handles quiz flow & scoring

✨ Features
Drag-and-drop multi-PDF ingestion

On-device vector search with ChromaDB – no external DB required

Retrieval-augmented question generation (up to 10 questions per topic)

Session-state navigation, instant correctness feedback & explanations

Modular, testable codebase
