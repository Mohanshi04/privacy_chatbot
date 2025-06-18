# 🛡️ Local Privacy Chatbot (Ollama + Python)

This chatbot allows you to query documents **entirely offline** using open-source language models via **Ollama**, while preserving **data privacy**.

## ✅ Features

- Local LLM inference using [Ollama](https://ollama.com)
- PDF document Q&A with **no external API**
- Terminal-based UI using `rich`
- File encryption with AES
- Vector DB with **ChromaDB**
- Fast response via local embeddings

## 💻 Requirements

- Python 3.8+
- Ollama installed with LLMs like `llama3`, `nomic-embed-text`
- pip install -r requirements.txt

## 🚀 Usage

```bash
python chatbot.py
```

When prompted, enter the **path to a PDF file**. Ask questions from the document in natural language.