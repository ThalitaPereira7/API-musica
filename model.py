from typing import Optional, List
from pydantic import BaseModel

class Musica(BaseModel):
    id: Optional[int] = None
    titulo: str
    cantor: str
    genero: str
    ano: int
    foto: str
    notas: Optional[List[int]] = []
    media: Optional[float] = None

class AtualizacaoMusica(BaseModel):
    titulo: Optional[str] = None
    cantor: Optional[str] = None
    genero: Optional[str] = None
    ano: Optional[int] = None
    foto: Optional[str] = None
