from fastapi import FastAPI, HTTPException, status, Request
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Configurar a API com um título para o front e as docs
app = FastAPI(
    title="API de Músicas",
    description="Front-end e API para músicas",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Banco de dados simulado
musicas = {
    1: {
        "titulo": "Valentine",
        "cantor": "Laufey",
        "genero": "jazz moderno",
        "ano": 2022,
        "foto": "https://imagedelivery.net/7yy6dErF9hbNfcqoZCcxBA/b7b23f69-a320-443a-a29f-19bbcf170c00/public",
    },
    2: {
        "titulo": "Odeio Despedidas",
        "cantor": "Lagum",
        "genero": "reggae pop",
        "ano": 2022,
        "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTk8yNEoTWBdXz8zzTtglYOXGv1euSbQGMnBA&s",
    },
}

# Rota do front-end (rota principal)
@app.get("/")
async def front(request: Request, busca: Optional[str] = None):
    if busca:
        resultado = {id: m for id, m in musicas.items() if busca.lower() in m["titulo"].lower()}
    else:
        resultado = musicas
    return templates.TemplateResponse("index.html", {"request": request, "musicas": resultado})

# Rotas da API
@app.get("/api/musicas")
async def get_musicas():
    return musicas


@app.get("/api/musicas/{musica_id}")
async def get_musica(musica_id: int):
    try:
        return musicas[musica_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Não existe esta música {musica_id}")


@app.post("/api/musicas", status_code=status.HTTP_201_CREATED)
async def post_musica(musica: dict):
    next_id = len(musicas) + 1
    musicas[next_id] = musica
    return musica


@app.delete("/api/musicas/{musica_id}")
async def delete_musica(musica_id: int):
    try:
        del musicas[musica_id]
        return {"msg": f"Música com ID {musica_id} deletada com sucesso."}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Não existe música com o ID {musica_id}")


@app.put("/api/musicas/{musica_id}")
async def put_musica(musica_id: int, musica: dict):
    if musica_id not in musicas:
        raise HTTPException(status_code=404, detail=f"Música com ID {musica_id} não encontrada.")
    musicas[musica_id] = musica
    return musicas[musica_id]


@app.get("/editar/{musica_id}")
async def editar_musica(request: Request, musica_id: int):
    """
    Renderiza a página de edição de uma música específica.
    """
    musica = musicas.get(musica_id)
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada.")
    return templates.TemplateResponse("editar.html", {"request": request, "musica_id": musica_id, "musica": musica})


@app.post("/editar/{musica_id}")
async def salvar_edicao(request: Request, musica_id: int):
    """
    Atualiza as informações da música com base no formulário enviado.
    """
    form = await request.form()

    # Verifica se a música existe
    if musica_id not in musicas:
        raise HTTPException(status_code=404, detail="Música não encontrada.")

    # Atualiza os dados da música com os valores do formulário
    musicas[musica_id].update(
        {
            "titulo": form["titulo"],
            "cantor": form["cantor"],
            "genero": form["genero"],
            "ano": int(form["ano"]),
            "foto": form["foto"],
        }
    )

    # Redireciona para a página inicial após salvar
    return RedirectResponse("/", status_code=303)

@app.get("/adicionar")
async def adicionar_musica(request: Request):
    """
    Exibe a página para adicionar uma nova música.
    """
    return templates.TemplateResponse("adicionar.html", {"request": request})


@app.post("/adicionar")
async def salvar_musica(request: Request):
    """
    Salva uma nova música no banco de dados.
    """
    form = await request.form()

    # Criar o próximo ID automaticamente
    next_id = max(musicas.keys()) + 1 if musicas else 1

    # Adicionar a nova música ao banco de dados
    musicas[next_id] = {
        "titulo": form["titulo"],
        "cantor": form["cantor"],
        "genero": form["genero"],
        "ano": int(form["ano"]),
        "foto": form["foto"],
    }

    # Redirecionar para a página inicial
    return RedirectResponse("/", status_code=303)



@app.post("/deletar/{musica_id}")
async def deletar_musica(musica_id: int):
    """
    Exclui uma música com base no ID fornecido.
    """
    if musica_id not in musicas:
        raise HTTPException(status_code=404, detail="Música não encontrada.")

    del musicas[musica_id]
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
