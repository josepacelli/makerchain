from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

DB_FAISS_PATH = "vectorstore/db_faiss"

def load_qa_chain():
    llm = ChatOllama(model="mistral")
    embeddings = OllamaEmbeddings(model="mistral")
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    # Prompt para instruir o modelo a responder sempre em português
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "Use as informações a seguir para responder à pergunta do usuário. "
            "Responda sempre em português, de forma clara e objetiva.\n\n"
            "Contexto:\n{context}\n\n"
            "Pergunta: {question}\n"
            "Resposta:"
        )
    )

    chain_type_kwargs = {"prompt": prompt}

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=False
    )
    
    return qa
