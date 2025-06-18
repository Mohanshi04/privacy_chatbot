# 🧰 Installation Guide for Local Privacy Chatbot

## 1. Clone or Download Project

```bash
git clone <your_repo_link>
cd privacy_chatbot
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Install Ollama

Download and install Ollama from https://ollama.com/download  
Then run:

```bash
ollama run llama3
ollama run nomic-embed-text
```

## 4. Run the Chatbot

```bash
python chatbot.py
```