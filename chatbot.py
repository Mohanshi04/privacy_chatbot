import os
import tempfile
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from cryptography.fernet import Fernet
from rich.console import Console
from rich.prompt import Prompt

# Terminal UI
console = Console()

# Encryption key generation & loading
KEY_FILE = "filekey.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()
fernet = Fernet(key)

# Load and encrypt file
def encrypt_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(file_path, "wb") as f:
        f.write(encrypted)

def decrypt_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(file_path, "wb") as f:
        f.write(decrypted)

# Document processing
def process_document(file_path):
    decrypt_file(file_path)
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    encrypt_file(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory="./chroma_db")
    vectorstore.persist()
    return vectorstore

# Setup LLM
def setup_qa_chain():
    llm = Ollama(model="llama3")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Terminal chat
def start_chat(qa_chain):
    console.print("[bold green]Chatbot ready! Type your question or 'exit' to quit.[/bold green]")
    while True:
        query = Prompt.ask("[bold cyan]You[/bold cyan]")
        if query.lower() in ("exit", "quit"):
            break
        answer = qa_chain.run(query)
        console.print(f"[bold yellow]Bot:[/bold yellow] {answer}")

if __name__ == "__main__":
    console.print("[bold magenta]Welcome to the Local Privacy Chatbot[/bold magenta]")
    pdf_path = Prompt.ask("Enter path to your PDF file for Q&A")
    if not os.path.exists(pdf_path):
        console.print("[bold red]File not found! Exiting...[/bold red]")
        exit(1)
    encrypt_file(pdf_path)
    vectorstore = process_document(pdf_path)
    qa_chain = setup_qa_chain()
    start_chat(qa_chain)