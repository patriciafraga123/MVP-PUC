# Define os modelos (schemas) relacionados aos dados de filmes populaares ,
# utilizados para validação e documentação da API.

from pydantic import BaseModel
from typing import Optional

class FilmePopSchema(BaseModel):
    filme_pop_id: int
    nome_filme_pop: str
    img_pop: str
    nota_pop: float
    adorei_pop: Optional[str] = " "  
    watchlist_pop: Optional[str] = "Não"  

class FilmeUpdateSchema(BaseModel):
    filme_pop_id: int  
    adorei_pop: Optional[str] = None
    watchlist_pop: Optional[str] = None

