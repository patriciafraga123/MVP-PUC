from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, render_template, redirect, request, jsonify
from flask import redirect
from urllib.parse import unquote
from pydantic import ValidationError
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

from model import Session, Filme, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API de Filmes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)



# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
filme_tag = Tag(name="Filme", description="Adição, visualização e remoção de filme à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um filme cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(form: FilmeSchema):

    """Adiciona um novo Filme à base de dados

    Retorna uma representação dos filmes  .
    """
    
    if form.minha_nota == "":
        form.minha_nota = None

    filme = Filme(
        nome_filme=form.nome_filme,
        genero=form.genero,
        nota_imdb =form.nota_imdb,
        ja_assisti = form.ja_assisti,
        minha_nota = form.minha_nota)
    logger.debug(f"Adicionando nome de filme: '{filme.nome_filme}'")
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando filme
        session.add(filme)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado nome de filme: '{filme.nome_filme}'")
        return apresenta_filme(filme), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Filme de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome_filme}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome_filme}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/filmes', tags=[filme_tag],
         responses={"200": ListagemFilmesSchema, "404": ErrorSchema})
def get_filmes():
    """Faz a busca por todos os Filmes cadastrados

    Retorna uma representação da listagem de filmess.
    """
    logger.debug(f"Coletando filmes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filmes = session.query(Filme).all()

    if not filmes:
        # se não há filmes cadastrados
        return {"filmes": []}, 200
    else:
        logger.debug(f"%d filmesrodutos econtrados" % len(filmes))
        # retorna a representação de filme
        print(filmes)
        return apresenta_filmes(filmes), 200


@app.get('/filmes', tags=[filme_tag],
         responses={"200": FilmeViewSchema, "404": ErrorSchema})
def get_filme(query: FilmeBuscaSchema):
    """Faz a busca por um Filme a partir do id do filme

    Retorna uma representação dos filmes .
    """
    filme_id = query.id
    logger.debug(f"Coletando dados sobre filme #{filme_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filme = session.query(Filme).filter(Filme.id == filme_id).first()

    if not filme:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao buscar filme '{filme_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Filme econtrado: '{filme.nome_filme}'")
        # retorna a representação de filme
        return apresenta_filme(filme), 200


@app.delete('/filme', tags=[filme_tag],
            responses={"200": FilmeDelSchema, "404": ErrorSchema})
def del_filme(query: FilmeBuscaSchema):
    """Deleta um Filme a partir do nome de filme informado

    Retorna uma mensagem de confirmação da remoção.
    """
    filme_nome = unquote(unquote(query.nome_filme))
    print(filme_nome)
    logger.debug(f"Deletando dados sobre filme #{filme_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Filme).filter(Filme.nome_filme == filme_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado filme #{filme_nome}")
        return {"message": "Filme removido", "id": filme_nome}
    else:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao deletar filme #'{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

# @@@ Novo Codigo para incluir alteração de dados
@app.put('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema})
def update_filme(form: FilmeUpdateSchema):
    """Modifica as informações de Já Assiti e Nota do Filme na base de dados

    Retorna uma representação dos filmes associados.
    """
    try:
        data = form.dict()

        # Buscar o filme no banco de dados
        session = Session()
        filme = session.query(Filme).filter(Filme.nome_filme == data['nome_filme']).first()
        if not filme:
            return jsonify({"message": "Filme não encontrado!"}), 404

        # Atualizar os campos recebidos
        if 'ja_assisti' in data:
            filme.ja_assisti = data['ja_assisti']
        if 'minha_nota' in data:
            filme.minha_nota = data['minha_nota']

        # Commit das alterações
        session.commit()
        return jsonify({"message": "Filme atualizado com sucesso!", "filme": apresenta_filme(filme)}), 200

    except ValidationError as e:
        return jsonify({"message": "Erro de validação", "detalhes": e.errors()}), 422
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

