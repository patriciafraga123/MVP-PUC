from pydantic import BaseModel, ValidationError
from typing import Optional, List
from model.filme import Filme

from schemas import ComentarioSchema

class FilmeSchema(BaseModel):
    """ Define como um novo filme a ser inserido deve ser representado
    """
    nome_filme: str = "Filme Padrão"
    genero: str = "Ação"
    nota_imdb: Optional[float] = 0
    ja_assisti: str
    minha_nota: Optional[int] = None

class FilmeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do filme.
    """
    nome_filme: str = "Teste"


class ListagemFilmesSchema(BaseModel):
    """ Define como uma listagem de filme será retornada.
    """
    filmes:List[FilmeSchema]


def apresenta_filmes(filmes: List[Filme]):
    """ Retorna uma representação do filme seguindo o schema definido em
        FilmeViewSchema.
    """
    result = []
    for filme in filmes:
        result.append({
            "nome_filme": filme.nome_filme,
            "genero": filme.genero,
            "nota_imdb": filme.nota_imdb,
            "ja_assisti": filme.ja_assisti,
            "minha_nota": filme.minha_nota
        })

    return {"filmes": result}


class FilmeViewSchema(BaseModel):
    """ Define como um filme será retornado: filme + comentários.
    """
    id: int = 1
    nome_filme: str = "Filme Padrão"
    genero: str = "Ação"
    nota_imdb: float=0
    ja_assisti: str ='Não'
    minha_nota: int=0
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


class FilmeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome_filme: str

def apresenta_filme(filme: Filme):
    """ Retorna uma representação do filme seguindo o schema definido em
        FilmeViewSchema.
    """
    return {
        "id": filme.id,
        "nome_filme": filme.nome_filme,
        "genero": filme.genero,
        "nota_imdb": filme.nota_imdb,
        "ja_assisti": filme.ja_assisti,
        "minha_nota": filme.minha_nota,
        "total_comentarios": len(filme.comentarios),
        "comentarios": [{"texto": c.texto} for c in filme.comentarios]


    }

## @@@ Novo codigo para API de update

class FilmeUpdateSchema(BaseModel):
    """ Define como um filme deve ser atualizado. Apenas campos relevantes são incluídos. """
    nome_filme: str  # Nome do filme que será atualizado (obrigatório para a busca)
    ja_assisti: str  # 'Sim' ou 'Não' (opcional)
    minha_nota: Optional[int]  # Nota do usuário (opcional)
