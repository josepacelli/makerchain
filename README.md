# 🚀 Makerchain

Makerchain é assistentes inteligente baseado em busca vetorial para suporte em projetos maker localmente, utilizando modelos locais Ollama com Mistral, integrado com FastAPI para uma interface web simples e eficiente.

---

## 📋 Índice

- [✨ Descrição](#-descrição)  
- [⏳ Linha do Tempo de Execução](#-linha-do-tempo-de-execução)  
- [⚙️ Componentes do Projeto](#️-componentes-do-projeto)  
- [🛠 Tecnologias Usadas](#-tecnologias-usadas)  
- [🔍 Alternativas ao FAISS](#-alternativas-ao-faiss)  
- [▶️ Como Rodar](#-como-rodar)  
- [🤝 Contribuições](#-contribuições)  
- [📄 Licença](#-licença)  

---

## ✨ Descrição

Makerchain permite consultas inteligentes em documentos indexados por vetores, combinando o poder do modelo **Mistral** local via Ollama com a eficiência do índice **FAISS**.  
Você pergunta em português e recebe respostas contextuais rápidas — tudo via uma interface web simples, com histórico e opção para limpar! 💬✨

---

## ⏳ Linha do Tempo de Execução

1. 🛠️ **Ingestão dos dados (ingest.py)**  
   - Coleta e processa documentos (PDF, condigo fonte, texto, etc).  
   - Extrai texto dos documentos usando bibliotecas como `unstructured` e `pypdf`.  
   - Divide o texto em pedaços menores (chunks).  
   - Gera embeddings para cada chunk usando `OllamaEmbeddings`.  
   - Armazena os vetores no banco vetorial local `FAISS`.

2. 📚 **Carga do banco vetorial e modelo (load_qa_chain)**  
   - Carrega o banco de dados FAISS com os embeddings.  
   - Inicializa o modelo de linguagem `ChatOllama` (ex: modelo "mistral").  

3. 💬 **Recepção da pergunta via API (FastAPI)**  
   - Usuário envia a pergunta via aplicação web.  
   - Backend recebe e processa a requisição.

4. 🔍 **Processamento da pergunta e recuperação**  
   - O retriever busca os chunks mais relevantes no FAISS.  
   - O LLM gera resposta contextualizada usando os chunks.

5. 📝 **Resposta ao usuário e histórico**  
   - Resposta é enviada para o frontend.  
   - Perguntas e respostas são armazenadas em sessão para histórico.  
   - Usuário pode limpar o histórico via botão.

---

## ⚙️ Componentes do Projeto

| Componente               | Função                                                                                  |
|-------------------------|----------------------------------------------------------------------------------------|
| `src/main.py`           | Servidor FastAPI com rotas, sessão e interface web                                     |
| `src/qa_engine.py`      | Carrega FAISS, embeddings e cadeia de QA usando Ollama + Mistral                       |
| `vectorstore/db_faiss`  | Índice vetorial FAISS local                                                           |
| `src/templates/index.html` | Template HTML com formulário, resultados e histórico                                 |
| `ingest.py`             | Script para processar documentos e criar índice vetorial FAISS                         |

---

## 🛠 Tecnologias Usadas

- **FastAPI** — Framework web rápido e moderno  
- **Uvicorn** — Servidor ASGI para rodar FastAPI  
- **Jinja2** — Templates HTML dinâmicos  
- **LangChain** — Framework para construção de pipelines com LLMs  
- **Langchain-Ollama** — Integração local com modelos Ollama  
- **FAISS** — Biblioteca para indexação e busca vetorial  
- **Python-Multipart** — Suporte a envio de formulários  
- **Starlette Sessions** — Gerenciamento de sessão no FastAPI  


## 🚀 Como rodar

1. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

2. Adicione os documentos, códigos fonte e outros arquivos na pasta `data`.

3. Faça a vetorização dos arquivos usando o script `ingest.py`:
    ```bash
    python3 ingest.py
    ```

4. Execute o servidor FastAPI:
    ```bash
    python -m uvicorn src.main:app --reload
    ```

5. Acesse o sistema pelo navegador:  
   [http://localhost:8000](http://localhost:8000)

6. Interaja com o Makerchain! ✨

---

## Contribuições 💡

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---
