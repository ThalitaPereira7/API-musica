from typing import Optional

from pydantic import BaseModel

class Musica(BaseModel):
    id: Optional[int] = None
    titulo: str
    cantor: str
    genero: str
    ano: int
    foto: str
    
    
        