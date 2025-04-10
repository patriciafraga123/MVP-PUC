# Arquivo de inicialização do pacote schemas.
# Torna o diretório 'schemas' um pacote Python.

from schemas.comentario import ComentarioSchema
from schemas.filme import FilmeSchema, FilmeBuscaSchema, FilmeViewSchema, \
                            ListagemFilmesSchema, FilmeDelSchema, FilmeUpdateSchema, \
                            apresenta_filme, apresenta_filmes
from schemas.error import ErrorSchema