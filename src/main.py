from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from src.qa_enginer import QAEngine, QAHandler

# Inicializa o app FastAPI
app = FastAPI(title="MakerChain Web")

# Middleware para sessão (para manter histórico entre requisições)
app.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_aqui")

# Templates Jinja2
templates = Jinja2Templates(directory="src/templates")

# Inicializa motor MCP com histórico/contexto
qa_engine = QAEngine()
qa_handler = QAHandler(qa_engine.qa)

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    """Renderiza a interface principal com histórico."""
    history = request.session.get("history", [])
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": "",
        "history": history
    })

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, pergunta: str = Form(...)):
    """Recebe a pergunta, gera resposta via MCP, salva no histórico."""
    try:
        resposta = qa_handler.ask(pergunta)
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        resposta = "Erro interno. Tente novamente."

    # Atualiza histórico na sessão
    history = request.session.get("history", [])
    history.append({"pergunta": pergunta, "resposta": resposta})
    if len(history) > 10:
        history.pop(0)
    request.session["history"] = history

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": resposta,
        "pergunta": pergunta,
        "history": history
    })

@app.post("/clear", response_class=RedirectResponse)
async def clear_history(request: Request):
    """Limpa o histórico da sessão."""
    request.session["history"] = []
    return RedirectResponse("/", status_code=303)
