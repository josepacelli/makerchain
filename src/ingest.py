import os
import sys
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings

# Configurações
DATA_DIR = r"C:\Users\gilso\OneDrive\Área de Trabalho\git\makerchain\data"
DB_FAISS_PATH = "vectorstore/db_faiss"

# Escolha o tipo de splitter: "recursive" ou "semantic"
SPLITTER_TYPE = "semantic"  # ou "recursive"

# Carregando documentos
def load_documents(data_dir):
    loaders = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".pdf"):
                loaders.append(PyPDFLoader(path))
            elif file.endswith(".py") or file.endswith(".ino") or file.endswith(".c") or file.endswith(".cpp"):
                loaders.append(PythonLoader(path))
            elif file.endswith(".md") or file.endswith(".txt"):
                loaders.append(TextLoader(path))
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs

# Função para aplicar o splitter
def split_documents(docs, splitter_type, embeddings_model): # Adicionado embeddings_model como argumento
    if splitter_type == "recursive":
        print("[INFO] Usando RecursiveCharacterTextSplitter...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    elif splitter_type == "semantic":
        print("[INFO] Usando SemanticChunker com o modelo de embeddings do LangChain")
        # O SemanticChunker recebe um objeto de embeddings do LangChain
        splitter = SemanticChunker(embeddings=embeddings_model)
    else:
        raise ValueError(f"Splitter '{splitter_type}' não é suportado.")
    
    return splitter.split_documents(docs)

def main():
    print(f"[INFO] Iniciando ingestão com splitter: {SPLITTER_TYPE}")
    docs = load_documents(DATA_DIR)

    # Inicializa o modelo de embeddings UMA VEZ e o passa para a função split_documents
    embeddings = OllamaEmbeddings(model="llama3")
    
    split_docs = split_documents(docs, SPLITTER_TYPE, embeddings) # Passa o modelo de embeddings

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(DB_FAISS_PATH)

    print("[OK] Base vetorial criada e salva em:", DB_FAISS_PATH)

if __name__ == "__main__":
    main()