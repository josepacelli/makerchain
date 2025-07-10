import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings

DATA_DIR = r"C:\Users\gilso\OneDrive\Área de Trabalho\git\makerchain\data"
DB_FAISS_PATH = "vectorstore/db_faiss"

# Carregando os documentos
loaders = []
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        path = os.path.join(root, file)
        if file.endswith(".pdf"):
            loaders.append(PyPDFLoader(path))
        elif file.endswith(".py") or file.endswith(".ino"):
            loaders.append(PythonLoader(path))
        elif file.endswith(".md") or file.endswith(".txt"):
            loaders.append(TextLoader(path))

docs = []
for loader in loaders:
    docs.extend(loader.load())

# 🔹 Aplica o chunking aqui
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Tamanho ideal do chunk (ajustável)
    chunk_overlap=100  # Sobreposição para manter o contexto
)
split_docs = text_splitter.split_documents(docs)

# Embeddings e vetorstore
embeddings = OllamaEmbeddings(model="llama3")
vectorstore = FAISS.from_documents(split_docs, embeddings)
vectorstore.save_local(DB_FAISS_PATH)

print("[OK] Base vetorial criada e salva em:", DB_FAISS_PATH)
