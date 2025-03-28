from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional
from model import Musica

app = FastAPI()

musicas = {
    1:{
        "titulo": "Valentine",
        "cantor": "Laufey",
        "genero": "jazz moderno",
        "ano": 2022,
        "foto": "https://imagedelivery.net/7yy6dErF9hbNfcqoZCcxBA/b7b23f69-a320-443a-a29f-19bbcf170c00/public"
    },
    
    2:{
        "titulo": "Odeio Despedidas",
        "cantor": "Lagum",
        "genero": "reggae pop",
        "ano": 2022,
        "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTk8yNEoTWBdXz8zzTtglYOXGv1euSbQGMnBA&s"
        
    }
}

@app.get("/")
async def raiz():
    return {"msg": "Deu Certo!"}


@app.get("/musicas", description="Retorna todas as musicas da lista", summary="Retorna todos as musicas")
async def get_musicas():
    return musicas

@app.get("/musicas/{musica_id}")
async def get_musicas(musica_id: int):
    try:
        musica = musicas[musica_id]
        return musica
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe esta musica{musica_id}")
    
@app.post("/musicas", status_code=status.HTTP_201_CREATED)
async def post_musica(musica: Optional[Musica] = None):
    next_id = len(musicas) + 1
    musicas[next_id] = musica
    del musica.id
    return musica


if  __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)