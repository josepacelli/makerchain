
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from src.qa_engine import load_qa_chain

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta_aqui")

templates = Jinja2Templates(directory="src/templates")
qa = load_qa_chain()

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    history = request.session.get("history", [])
    return templates.TemplateResponse("index.html", {"request": request, "result": "", "history": history})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, pergunta: str = Form(...)):
    try:
        resposta = qa.run(pergunta)
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        resposta = "Erro interno. Tente novamente."
    resposta = qa.run(pergunta)
    history = request.session.get("history", [])
    history.append({"pergunta": pergunta, "resposta": resposta})
    if len(history) > 10:
        history.pop(0)
    request.session["history"] = history
    return templates.TemplateResponse("index.html", {"request": request, "result": resposta, "pergunta": pergunta, "history": history})

history = []

@app.post("/clear", response_class=RedirectResponse)
async def clear_history(request: Request):
    request.session["history"] = []
    return RedirectResponse("/", status_code=303)
