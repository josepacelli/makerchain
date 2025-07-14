import os
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA, StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

DB_FAISS_PATH = "vectorstore/db_faiss"
LOGS_DIR = "logs"

class QAEngine:
    def __init__(self):
        self.llm = ChatOllama(model="mistral")
        self.embeddings = OllamaEmbeddings(model="mistral")
        self.db = FAISS.load_local(DB_FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)
        self.retriever = self.db.as_retriever()

        pt_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Responda em português de forma clara e objetiva.\n\n"
                "Contexto: {context}\n"
                "Pergunta: {question}\n"
                "Resposta:"
            )
        )

        llm_chain = LLMChain(llm=self.llm, prompt=pt_prompt)

        stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="context"
        )

        self.qa = RetrievalQA(
            retriever=self.retriever,
            combine_documents_chain=stuff_chain,
            return_source_documents=False
        )

class QAHandler:
    def __init__(self, qa_chain):
        self.qa = qa_chain
        self.history = []
        os.makedirs(LOGS_DIR, exist_ok=True)

    def salvar_prompt_e_resposta(self, pergunta: str, prompt_final: str, resposta: str):
        with open(os.path.join(LOGS_DIR, "prompts_log.txt"), "a", encoding="utf-8") as f:
            f.write("Pergunta do usuário:\n")
            f.write(pergunta + "\n\n")
            f.write("Prompt final enviado ao LLM:\n")
            f.write(prompt_final + "\n\n")
            f.write("Resposta gerada:\n")
            f.write(resposta + "\n")
            f.write("="*40 + "\n")

    def ask(self, question: str) -> str:
        # Monta contexto simples do histórico (últimas 3 interações)
        context = ""
        for turn in self.history[-3:]:
            context += f"Pergunta: {turn['pergunta']}\nResposta: {turn['resposta']}\n\n"

        prompt_with_context = f"Considere este histórico de perguntas e respostas:\n{context}Pergunta atual: {question}"

        response = self.qa.run(prompt_with_context)

        self.history.append({"pergunta": question, "resposta": response})

        if len(self.history) > 10:
            self.history.pop(0)

        self.salvar_prompt_e_resposta(question, prompt_with_context, response)

        return response
