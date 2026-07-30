# GenAI Mini-RAG Telegram Bot

A lightweight Retrieval-Augmented Generation (RAG) Telegram chatbot built with Python.

The bot answers employee-policy questions using a small local knowledge base, semantic retrieval, SQLite storage, and a local Llama 3.2 model through Ollama.

## Project Overview

This project demonstrates an end-to-end Mini-RAG pipeline:

User Question
    ↓
Telegram Bot
    ↓
Sentence Transformer Embedding
    ↓
SQLite Knowledge Base
    ↓
Semantic Similarity Retrieval
    ↓
Relevant Context
    ↓
Llama 3.2 via Ollama
    ↓
Grounded Answer
    ↓
Telegram

The system is designed to answer only questions supported by the knowledge base. Questions outside the knowledge base are rejected using a similarity threshold.

## Features

- Telegram chatbot interface
- `/start` command
- `/help` command
- `/ask <question>` command
- Natural-language questions without `/ask`
- 4 Markdown knowledge documents
- Markdown section-based chunking
- Local embeddings using `all-MiniLM-L6-v2`
- 384-dimensional sentence embeddings
- SQLite-based local storage
- Semantic similarity retrieval
- Top-k retrieval
- Relevance threshold to reduce unsupported answers
- Local Llama 3.2 3B model through Ollama
- Source document shown with answers
- CLI demo for testing the RAG engine without Telegram

## Knowledge Base

The project contains four sample company-policy documents:

- `leave_policy.md`
- `benefits.md`
- `work_from_home.md`
- `faq.md`

The documents are divided into 18 searchable chunks.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Telegram | python-telegram-bot |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Size | 384 |
| Database | SQLite |
| LLM Runtime | Ollama |
| LLM | Llama 3.2 3B |
| Configuration | python-dotenv |

## Project Structure

```text
genai-rag-telegram-bot/
│
├── app.py
├── rag.py
├── retrieval.py
├── database.py
├── ingest.py
├── embeddings.py
├── llm.py
├── demo.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── leave_policy.md
│   ├── benefits.md
│   ├── work_from_home.md
│   └── faq.md
│
└── rag.db