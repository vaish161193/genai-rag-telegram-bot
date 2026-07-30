\# GenAI Mini-RAG Telegram Bot



A lightweight Retrieval-Augmented Generation (RAG) Telegram bot built with Python.



\## Project Overview



This project implements a Telegram chatbot that retrieves relevant information

from a small local knowledge base and uses an LLM to generate an answer.



\## Architecture



Telegram User

&#x20;   ↓

Telegram Bot

&#x20;   ↓

Query

&#x20;   ↓

Embedding Model

&#x20;   ↓

SQLite Knowledge Base

&#x20;   ↓

Top-K Relevant Chunks

&#x20;   ↓

LLM

&#x20;   ↓

Generated Answer

&#x20;   ↓

Telegram User



\## Planned Features



\- `/start` - Start the bot

\- `/help` - Show available commands

\- `/ask <query>` - Ask a question using RAG

\- Retrieve relevant document chunks

\- Generate answers using an LLM

\- Show source snippets



\## Technology Stack



\- Python

\- Telegram Bot API

\- python-telegram-bot

\- Sentence Transformers

\- SQLite

\- Large Language Model



\## Project Status



🚧 Currently under development.



\## Author



Vaishnavi Muralidharan

